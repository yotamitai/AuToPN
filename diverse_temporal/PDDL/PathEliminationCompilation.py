import sys
import os
from diverse_temporal.PDDL.PDDLInstance import  *
from diverse_temporal.PDDL.PDDLSTypes import *
import re

class PlanSequence():
    def __init__(self, p):
        self.currentIndex = 1
        self.plan = {}
        self.openActions = {}
        self.closedActions = []

        i = 1
        for key, val in p.items():
            m = re.search("(?s)\s*?([A-Z]*?)\-(.*)", str(val))
            if m.group(1) == "START":
                self.InsertNewAction(m.group(2), i)
            elif m.group(1) == "END":
                self.AddEndIndex(m.group(2), i)
            else:
                print ("error")
            i = i + 1


    def InsertNewAction(self, action, startInd):
        if action not in self.closedActions:
            instances = 1
        else:
            instances = self.closedActions.count(action)+1

        self.plan[self.currentIndex] = PlanSequenceAction(action, startInd, instances)
        self.openActions[action] = self.currentIndex
        self.currentIndex = self.currentIndex + 1

    def AddEndIndex(self, action, endInd):
        if action in self.openActions:
            ind = self.openActions[action]
            self.plan[ind].AddEndIndex(endInd)
            self.closedActions.append(action)
            del self.openActions[action]
        else:
            raise ValueError("No such action in plan: " + action + " " + str(endInd))

    def IsActionInPlan(self, action):
        if action in self.closedActions:
            return True
        else:
            return False

    def GetPlanSequence(self):
        return self.plan

    def GetPlanLength(self):
        return self.currentIndex-1



class PlanSequenceAction():
    plan = []

    def __init__(self, action, startInd, uniqeness):
        self.uniqe = uniqeness
        self.plan = [action, startInd]

    def AddEndIndex(self, ind):
        self.plan.append(ind)
        self.plan.append(self.uniqe)

    def GetStartIndex(self):
        return self.plan[1]

    def GetEndIndex(self):
        return self.plan[2]

    def GetUniqueness(self):
        return self.plan[3]

    def GetAction(self):
        return self.plan

    def __str__(self):
        return self.plan[0]


class CompiledPlanningInstance():
    def __init__(self, inst, plan, UID, map = None):
        self.base = inst
        self.plan = plan
        self.compiled = None
        self.UID = UID
        self.N = plan.GetPlanLength()*2
        self.Map = {}
        self.baseMap = map
        self.delimiter = "_"


    def Compile(self):
        inPi = []
        notInPi = []

        actions = self.base.GetActivities().keys()
        for action in actions:
            if self.plan.IsActionInPlan(action):
                inPi.append(action)
            else:
                notInPi.append(action)

        name = str(self.base)
        name = re.search("(?s)(\S*?)\d*$", name).group(1)

        self.compiled = PDDLSInstance(str(name+str(self.UID)))
        self.compiled.AddRequirements(self.base.GetRequirements())
        self.compiled.AddMetric(self.base.GetMetric())

        S = self.__replicateDic(self.base.GetPredicates())
        A = self.__replicateDic(self.base.GetActivities())
        s0 = self.__replicateDic(self.base.GetInitState())
        G = self.__replicateDic(self.compiled.GetGoalSet())

        # Predicates
        Plist = []
        PlistNot = []
        for i in range(self.N+1):
            newPname = "p" + str(self.UID) + "_" + str(i)
            newPnameNot = "pNot" + str(self.UID) + "_" + str(i)
            Plist.append(newPname)
            PlistNot.append(newPnameNot)
            newP = Predicate(newPname)
            newPnot = Predicate(newPnameNot)
            S[newPname] = newP
            S[newPnameNot] = newPnot
        newPname = "p" + str(self.UID)
        newPnameNot = "pNot" + str(self.UID)
        Plist.append(newPname)
        PlistNot.append(newPnameNot)
        newP = Predicate(newPname)
        newPnot = Predicate(newPnameNot)
        S[newPname] = newP
        S[newPnameNot] = newPnot

        # init state
        s0[Plist[0]] = S[Plist[0]]
        for i in range(1,self.N+2):
            # print(PlistNot[i])
            s0[PlistNot[i]] = S[PlistNot[i]]
        # print (s0)

        # goal set
        G[Plist[self.N+1]] = ConditionalPredicate(S[Plist[self.N+1]], True)

        # actions name_UID|case|repetition
        # not in pi
        A_prime = {}
        for action in notInPi:
            eff = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", True)
            name = str(action) + self.delimiter + str(self.UID) + "01"
            a0 = DurativeAction(name, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:],\
                                A[action].GetEffects()[:])
            a0.AddEffect(eff)
            A_prime[name] = a0
            if self.baseMap:
                self.Map[name] = self.baseMap[str(action)]
            else:
                self.Map[name] = str(action)

        # case 1
        # for action in inPi:
        for key, val in self.plan.GetPlanSequence().items():
            action = str(val)
            dup = val.GetUniqueness()
            name1 = action + self.delimiter + str(self.UID) + "1" + str(dup)
            a1 = DurativeAction(name1, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:], \
                                A[action].GetEffects()[:])
            cond = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", True)
            a1.AddCondition(cond)
            if self.baseMap:
                self.Map[name1] = self.baseMap[str(action)]
            else:
                self.Map[name1] = str(action)
            A_prime[name1] = a1

            # case 2
            name2 = str(action) + self.delimiter + str(self.UID) + "2" + str(dup)
            a2 = DurativeAction(name2, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:], \
                                A[action].GetEffects()[:])
            # cond = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", False)
            cond = TimedConditionalPredicate(S[PlistNot[self.N+1]], "at start", True)
            # condi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", False)
            condi = TimedConditionalPredicate(S[PlistNot[val.GetStartIndex()-1]], "at start", True)
            a2.AddCondition(cond)
            a2.AddCondition(condi)
            eff = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", True)
            effn = TimedConditionalPredicate(S[PlistNot[self.N+1]], "at start", False)
            a2.AddEffect(eff)
            a2.AddEffect(effn)
            if self.baseMap:
                self.Map[name2] = self.baseMap[action]
            else:
                self.Map[name2] = action
            A_prime[name2] = a2


            # case 3
            name3 = str(action) + self.delimiter + str(self.UID) + "3" + str(dup)
            a3 = DurativeAction(name3, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:], \
                                A[action].GetEffects()[:])
            # conds = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", False)
            conds = TimedConditionalPredicate(S[PlistNot[self.N+1]], "at start", True)
            conde = TimedConditionalPredicate(S[Plist[self.N+1]], "at end", True)
            # conden = TimedConditionalPredicate(S[PlistNot[self.N+1]], "at end", False)
            condi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", True)
            a3.AddCondition(conds)
            a3.AddCondition(conde)
            a3.AddCondition(condi)
            effi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", False)
            effin = TimedConditionalPredicate(S[PlistNot[val.GetStartIndex()-1]], "at start", True)
            effinext = TimedConditionalPredicate(S[Plist[val.GetStartIndex()]], "at start", True)
            effinextn = TimedConditionalPredicate(S[PlistNot[val.GetStartIndex()]], "at start", False)
            a3.AddEffect(effi)
            a3.AddEffect(effin)
            a3.AddEffect(effinext)
            a3.AddEffect(effinextn)
            if self.baseMap:
                self.Map[name3] = self.baseMap[action]
            else:
                self.Map[name3] = action
            A_prime[name3] = a3


            # case 4
            name4 = str(action) + self.delimiter + str(self.UID) + "4" + str(dup)
            a4 = DurativeAction(name4, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:], \
                                A[action].GetEffects()[:])
            # conds = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", False)
            conds = TimedConditionalPredicate(S[PlistNot[self.N+1]], "at start", True)
            # conde = TimedConditionalPredicate(S[Plist[self.N+1]], "at end", False)
            conde = TimedConditionalPredicate(S[PlistNot[self.N+1]], "at end", True)
            condi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", True)
            # condj = TimedConditionalPredicate(S[Plist[val.GetEndIndex()-1]], "at end", False)
            condj = TimedConditionalPredicate(S[PlistNot[val.GetEndIndex()-1]], "at end", True)
            a4.AddCondition(conds)
            a4.AddCondition(conde)
            a4.AddCondition(condi)
            a4.AddCondition(condj)
            effi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", False)
            effin = TimedConditionalPredicate(S[PlistNot[val.GetStartIndex()-1]], "at start", True)
            effinext = TimedConditionalPredicate(S[Plist[val.GetStartIndex()]], "at start", True)
            effinextn = TimedConditionalPredicate(S[PlistNot[val.GetStartIndex()]], "at start", False)
            effe = TimedConditionalPredicate(S[Plist[self.N+1]], "at end", True)
            effen = TimedConditionalPredicate(S[PlistNot[self.N+1]], "at end", False)
            a4.AddEffect(effi)
            a4.AddEffect(effin)
            a4.AddEffect(effinext)
            a4.AddEffect(effinextn)
            a4.AddEffect(effe)
            a4.AddEffect(effen)
            if self.baseMap:
                self.Map[name4] = self.baseMap[action]
            else:
                self.Map[name4] = action
            A_prime[name4] = a4


            # case 5
            name5 = str(action) + self.delimiter + str(self.UID) + "5" + str(dup)
            a5 = DurativeAction(name5, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:], \
                                A[action].GetEffects()[:])
            # conds = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", False)
            conds = TimedConditionalPredicate(S[PlistNot[self.N+1]], "at start", True)
            # conde = TimedConditionalPredicate(S[Plist[self.N+1]], "at end", False)
            conde = TimedConditionalPredicate(S[PlistNot[self.N+1]], "at end", True)
            condi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", True)
            condj = TimedConditionalPredicate(S[Plist[val.GetEndIndex()-1]], "at end", True)
            a5.AddCondition(conds)
            a5.AddCondition(conde)
            a5.AddCondition(condi)
            a5.AddCondition(condj)
            effi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", False)
            effin = TimedConditionalPredicate(S[PlistNot[val.GetStartIndex()-1]], "at start", True)
            effinext = TimedConditionalPredicate(S[Plist[val.GetStartIndex()]], "at start", True)
            effinextn = TimedConditionalPredicate(S[PlistNot[val.GetStartIndex()]], "at start", False)
            effj = TimedConditionalPredicate(S[Plist[val.GetEndIndex()-1]], "at end", False)
            effjn = TimedConditionalPredicate(S[PlistNot[val.GetEndIndex()-1]], "at end", True)
            effjnext = TimedConditionalPredicate(S[Plist[val.GetEndIndex()]], "at end", True)
            effjnextn = TimedConditionalPredicate(S[PlistNot[val.GetEndIndex()]], "at end", False)
            a5.AddEffect(effi)
            a5.AddEffect(effin)
            a5.AddEffect(effinext)
            a5.AddEffect(effinextn)
            a5.AddEffect(effj)
            a5.AddEffect(effjn)
            a5.AddEffect(effjnext)
            a5.AddEffect(effjnextn)
            if self.baseMap:
                self.Map[name5] = self.baseMap[action]
            else:
                self.Map[name5] = action
            A_prime[name5] = a5

        # print (self.Map)
        # print (A_prime)

        self.compiled.AddPredicates(S)
        self.compiled.AddActivities(A_prime)
        self.compiled.AddInitState(s0)
        self.compiled.AddGoalSet(G)

        # return self.compiled




    def Compile2(self):
        inPi = []
        notInPi = []

        actions = self.base.GetActivities().keys()
        for action in actions:
            if self.plan.IsActionInPlan(action):
                inPi.append(action)
            else:
                notInPi.append(action)

        name = str(self.base)
        name = re.search("(?s)(\S*?)\d*$", name).group(1)

        self.compiled = PDDLSInstance(str(name+str(self.UID)))
        self.compiled.AddRequirements(self.base.GetRequirements())
        self.compiled.AddMetric(self.base.GetMetric())

        S = self.__replicateDic(self.base.GetPredicates())
        A = self.__replicateDic(self.base.GetActivities())
        s0 = self.__replicateDic(self.base.GetInitState())
        G = self.__replicateDic(self.compiled.GetGoalSet())

        # Predicates
        Plist = []
        PlistNot = []
        for i in range(self.N+2):
            newPname = "p" + str(self.UID) + "_" + str(i)
            Plist.append(newPname)
            newP = Predicate(newPname)
            S[newPname] = newP
        newPname = "p" + str(self.UID)
        Plist.append(newPname)
        newP = Predicate(newPname)
        S[newPname] = newP

        # init state
        s0[Plist[0]] = S[Plist[0]]

        # goal set
        G[Plist[self.N+1]] = ConditionalPredicate(S[Plist[self.N+1]], True)

        # actions name_UID|case|repetition
        # not in pi
        A_prime = {}
        for action in notInPi:
            eff = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", True)
            name = str(action) + "_" + str(self.UID) + "01"
            a0 = DurativeAction(name, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:],\
                                A[action].GetEffects()[:])
            a0.AddEffect(eff)
            A_prime[name] = a0
            if self.baseMap:
                self.Map[name] = self.baseMap[str(action)]
            else:
                self.Map[name] = str(action)

        # case 1
        # for action in inPi:
        for key, val in self.plan.GetPlanSequence().items():
            action = str(val)
            dup = val.GetUniqueness()
            name1 = action + "_" + str(self.UID) + "1" + str(dup)
            a1 = DurativeAction(name1, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:], \
                                A[action].GetEffects()[:])
            cond = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", True)
            a1.AddCondition(cond)
            if self.baseMap:
                self.Map[name1] = self.baseMap[str(action)]
            else:
                self.Map[name1] = str(action)
            A_prime[name1] = a1
            # print (a1.ToPDDL())

            # case 2
            name2 = str(action) + "_" + str(self.UID) + "2" + str(dup)
            a2 = DurativeAction(name2, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:], \
                                A[action].GetEffects()[:])
            cond = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", False)
            condi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", False)
            a2.AddCondition(cond)
            a2.AddCondition(condi)
            eff = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", True)
            a2.AddEffect(eff)
            if self.baseMap:
                self.Map[name2] = self.baseMap[action]
            else:
                self.Map[name2] = action
            A_prime[name2] = a2


            # case 3
            name3 = str(action) + "_" + str(self.UID) + "3" + str(dup)
            a3 = DurativeAction(name3, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:], \
                                A[action].GetEffects()[:])
            conds = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", False)
            conde = TimedConditionalPredicate(S[Plist[self.N+1]], "at end", True)
            condi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", True)
            a3.AddCondition(conds)
            a3.AddCondition(conde)
            a3.AddCondition(condi)
            effi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", False)
            effinext = TimedConditionalPredicate(S[Plist[val.GetStartIndex()]], "at start", True)
            a3.AddEffect(effi)
            a3.AddEffect(effinext)
            if self.baseMap:
                self.Map[name3] = self.baseMap[action]
            else:
                self.Map[name3] = action
            A_prime[name3] = a3


            # case 4
            name4 = str(action) + "_" + str(self.UID) + "4" + str(dup)
            a4 = DurativeAction(name4, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:], \
                                A[action].GetEffects()[:])
            conds = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", False)
            conde = TimedConditionalPredicate(S[Plist[self.N+1]], "at end", False)
            condi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", True)
            condj = TimedConditionalPredicate(S[Plist[val.GetEndIndex()-1]], "at end", False)
            a4.AddCondition(conds)
            a4.AddCondition(conde)
            a4.AddCondition(condi)
            a4.AddCondition(condj)
            effi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", False)
            effinext = TimedConditionalPredicate(S[Plist[val.GetStartIndex()]], "at start", True)
            effe = TimedConditionalPredicate(S[Plist[self.N+1]], "at end", True)
            a4.AddEffect(effi)
            a4.AddEffect(effinext)
            a4.AddEffect(effe)
            if self.baseMap:
                self.Map[name4] = self.baseMap[action]
            else:
                self.Map[name4] = action
            A_prime[name4] = a4


            # case 5
            name5 = str(action) + "_" + str(self.UID) + "5" + str(dup)
            a5 = DurativeAction(name5, A[action].GetParams(), A[action].GetDuration(), A[action].GetConditions()[:], \
                                A[action].GetEffects()[:])
            conds = TimedConditionalPredicate(S[Plist[self.N+1]], "at start", False)
            conde = TimedConditionalPredicate(S[Plist[self.N+1]], "at end", False)
            condi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", True)
            condj = TimedConditionalPredicate(S[Plist[val.GetEndIndex()-1]], "at end", True)
            a5.AddCondition(conds)
            a5.AddCondition(conde)
            a5.AddCondition(condi)
            a5.AddCondition(condj)
            effi = TimedConditionalPredicate(S[Plist[val.GetStartIndex()-1]], "at start", False)
            effinext = TimedConditionalPredicate(S[Plist[val.GetStartIndex()]], "at start", True)
            effj = TimedConditionalPredicate(S[Plist[val.GetEndIndex()-1]], "at end", False)
            effjnext = TimedConditionalPredicate(S[Plist[val.GetEndIndex()]], "at end", True)
            a5.AddEffect(effi)
            a5.AddEffect(effinext)
            a5.AddEffect(effj)
            a5.AddEffect(effjnext)
            if self.baseMap:
                self.Map[name5] = self.baseMap[action]
            else:
                self.Map[name5] = action
            A_prime[name5] = a5

        # print (self.Map)
        # print (A_prime)

        self.compiled.AddPredicates(S)
        self.compiled.AddActivities(A_prime)
        self.compiled.AddInitState(s0)
        self.compiled.AddGoalSet(G)

        # return self.compiled


    def GetCompiledInstance(self):
        return self.compiled

    def GetTansformation(self):
        return self.Map

    def __replicateDic(self, dic):
        newD = {}
        for key, val in dic.items():
            newD[key] = val
        return newD

    def GenerateCompiledDomainFile(self, filename):
        # self.compiled.GenerateDomainFile(isScotty, filename)
        self.compiled.GenerateDomainFile(filename)

    def GenerateCompiledProblemFile(self, filename):
        self.compiled.GenerateProblemFile(filename)







