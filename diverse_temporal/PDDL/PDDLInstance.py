import re
from diverse_temporal.PDDL.PDDLSTypes import *


class PDDLSInstance(PDDLElement):
    elements = {}
    def __init__(self, name):
        PDDLElement.__init__(self, name)
        self.elements["name"] = name

    def AddRequirements(self, req):
        self.elements["requirements"] = req

    def GetRequirements(self):
        return self.elements["requirements"]

    def AddPredicates(self, preds):
        self.elements["predicates"] = preds

    def GetPredicates(self):
        return self.elements["predicates"]

    def AddFunctions(self, funcs):
        if funcs is not None:
            self.elements["functions"] = funcs
        else:
            self.elements["functions"] = {}

    def GetFunctions(self):
        return self.elements["functions"]

    def AddActivities(self, acts):
        self.elements["activities"] = acts

    def GetActivities(self):
        return self.elements["activities"]

    def AddInitState(self, initState):
        self.elements["init"] = initState

    def GetInitState(self):
        return self.elements["init"]

    def AddGoalSet(self, goalSet):
        self.elements["goal"] = goalSet

    def GetGoalSet(self):
        return self.elements["goal"]

    def AddMetric(self, metric):
        self.elements["metric"] = metric

    def GetMetric(self):
        return self.elements["metric"]

    def GenerateDomainFile(self, domainFileName=None):
        # generate name
        domainTxt = "(define (domain " + self.elements["name"] + ")\n"

        # generate requirements
        domainTxt = domainTxt + "(" + self.elements["requirements"] + ")\n\n"

        # generate predicates
        domainTxt = domainTxt + "(:predicates\n"
        for _, pred in self.elements["predicates"].items():
            domainTxt = domainTxt + "\t(" + str(pred) + ")\n"
        domainTxt = domainTxt + ")\n\n"

        # generate functions
        domainTxt = domainTxt + "(:functions\n"
        for _, func in self.elements["functions"].items():
            domainTxt = domainTxt + "\t(" + str(func) + ")\n"
        domainTxt = domainTxt + ")\n\n"

        # generate activities
        for _, activity in self.elements["activities"].items():
            domainTxt = domainTxt + activity.ToPDDL() + "\n"
        domainTxt = domainTxt + ")"

        if domainFileName:
            f = open(domainFileName, 'w')
            f.write(domainTxt)
            f.close()

        return domainTxt


    def GenerateProblemFile(self, problemFileName=None):
        # generate name
        problemTxt = "(define (problem " + self.elements["name"] + "1)\n"
        problemTxt = problemTxt + "\t(:domain " + self.elements["name"] + ")\n"

        # generate init state
        problemTxt = problemTxt + "\t(:init\n"
        for _, initcond in self.elements["init"].items():
            problemTxt = problemTxt + "\t\t(" + initcond.ToPDDL() + ")\n"
        problemTxt = problemTxt + "\t)\n"

        # generate goal set
        problemTxt = problemTxt + "\t(:goal (and\n"
        for _, goalcond in self.elements["goal"].items():
            problemTxt = problemTxt + "\t\t(" + goalcond.ToPDDL() + ")\n"
        problemTxt = problemTxt + "\t\t)\n\t)\n"

        # generate matric
        problemTxt = problemTxt + "(:metric minimize ("
        problemTxt = problemTxt + self.elements["metric"] + ")"
        problemTxt = problemTxt + ")\n)\n"

        if problemFileName:
            f = open(problemFileName, 'w')
            f.write(problemTxt)
            f.close()

        return problemTxt


    def __str__(self):
        return self.name