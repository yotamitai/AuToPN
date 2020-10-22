import sys
import re
from _curses import raw

from diverse_temporal.PDDL.Tree import Node


class Grounder:
    def __init__(self, domain, problem):
        self.domainFile = domain
        self.problemFile = problem
        self.domainTxt = ""
        self.problemTxt = ""
        self.GroundedDomainTxt = ""
        self.GroundedProblemTxt = ""
        self.Types = Node("object")
        self.objects = {}
        self.predicates = []
        self.functions = []
        self.operators = []
        self.init = []
        self.goal = []
        self.delimiter = "--"


    def Ground(self, domain="", problem=""):
        print("Preparing files for grounding ......... ", end='', flush=True)
        self.domainTxt = self.__RemoveComments(open(self.domainFile, "r").read())
        self.domainTxt = self.__RemoveLastBracket(self.domainTxt)
        self.problemTxt = self.__RemoveComments(open(self.problemFile, "r").read())
        m = re.search("(?s)(\(define.*\))\s*(\(:\s*\s*requirements.*?)\)\s*\(:\s*types\s*(.*?)\)\s*(.*)", self.domainTxt)
        # self.GroundedDomainTxt = m.group(1) + "\n\t" + m.group(2) + " :duration-inequalities :negative-preconditions)\n"
        self.GroundedDomainTxt = m.group(1) + "\n\t" + m.group(2) + ")\n"
        restDomain = m.group(4)
        print("DONE", flush=True)

        # Types parsing
        print("Parsing types ......................... ", end='', flush=True)
        typesTxt = m.group(3)
        free_objects = re.search("(?s)(.*\s*\-\s*\S*)?\s*(.*)", typesTxt)
        if free_objects.group(2) != "":
            typesTxt = typesTxt + " - object"

        for typestr in re.findall("(?s)\s*(.*?\-\s*[a-zA-Z_]*)", typesTxt):
            splited = re.search("(?s)\s*(.*?)\s*\-\s*([a-zA-Z_]*)", typestr)
            parent = splited.group(2)
            childs = splited.group(1)
            par = self.Types.GetSubTree(parent)
            if par is None:
                self.Types.AddChild(Node(parent))
            p = self.Types.GetSubTree(parent)
            for child in re.findall("[a-zA-Z_]+", childs):
                p.AddChild(Node(child))
        print("DONE")

        m = re.search("(?s)(\(define.*\))\s*(\(:\s*\s*domain.*?\))\s*\(:\s*objects\s*(.*?)\)(.*)", self.problemTxt)
        self.GroundedProblemTxt = m.group(1) + "\n\t" + m.group(2) + "\n"

        restProblem = m.group(4)

        # TODO: handle constants (for parc printer 2011)
        # extracting constants
        # print("Parsing objects ....................... ", end='')
        # m_const = re.search("(?s)\s*\(:constants\s*")
        # constantsTxt =

        # Object parsing
        print("Parsing objects ....................... ", end='')
        objectsTxt = m.group(3)
        for objlist in re.findall("(?s)\s*(.*?)\s+\-\s+([a-zA-Z_]*)", objectsTxt):
            type = objlist[1]
            preds = re.findall("(\S+)", objlist[0])
            if type not in self.objects:
                self.objects[type] = preds
            else:
                self.objects[type] = self.objects[type] + preds
        print("DONE", flush=True)

        # ########################
        # predicate parsing and grounding
        # ########################
        print("Grounding predicates .................. ", end='', flush=True)
        splited = re.search("(?s)\s*\(:\s*predicates\s*(.*?\))\s*\)\s*(.*)", restDomain)
        unGpreds = splited.group(1)
        unGacts = splited.group(2)
        for unGpred in re.findall("(?s)\((.*?)\)", unGpreds):
            params = re.findall("(?s)\?.*?\s+-\s+\S*", unGpred)
            L = []
            for p in params:
                objs = re.search("(?s)(.*?)\s-\s(\S*)", p)
                t = objs.group(2)
                objs = re.findall("\?\S*", objs.group(1))
                for i in objs:
                    pp = i + " - " + t
                    L.append(pp)

            params = L
            unGpred = re.sub("\-\s+\S+","", unGpred)
            unGpred = re.sub("\s+", " ", unGpred)
            unGpred = unGpred.rstrip()
            Gpreds1 = [unGpred]
            Gpreds2 = []  # edited
            # extract parameters
            if params == []:
                Gpreds2 = Gpreds1
            for param in params:
                pType = re.search("(?s)-\s*(\S+)", param).group(1)
                # print (pType)
                try:
                    T = self.Types.GetDescendant(pType)
                except:
                    raise ValueError(pType, "is causeing problems")
                objs = []
                for type in T:
                    if type in self.objects:
                        objs = objs + self.objects[type]
                for obj in objs:
                    for gpred in Gpreds1:
                        pp = re.search("\?\S+", param).group(0)
                        p = re.sub("\\"+pp, obj, gpred)
                        Gpreds2.append(p)
                Gpreds1 = Gpreds2
                Gpreds2 = []
            self.predicates = self.predicates+Gpreds1
        for i in range( 0,len(self.predicates)):
            self.predicates[i] = re.sub("\s+", "_", self.predicates[i])
        print("DONE", flush=True)

        # ########################
        # function parsing and grounding
        # ########################
        print("Grounding functions ................... ", end='', flush=True)
        splited = re.search("(?s)\s*\(:\s*functions\s*(.*?\))\s*\)\s*(.*)", unGacts)
        if splited is not None:
            unGpreds = splited.group(1)
            unGacts = splited.group(2)
            for unGpred in re.findall("(?s)\((.*?)\)", unGpreds):
                params = re.findall("(?s)\?.*?\s+-\s+\S*", unGpred)
                L = []
                for p in params:
                    objs = re.search("(?s)(.*?)\s-\s(\S*)", p)
                    t = objs.group(2)
                    objs = re.findall("\?\S*", objs.group(1))
                    for i in objs:
                        pp = i + " - " + t
                        L.append(pp)

                params = L
                unGpred = re.sub("\-\s+\S+", "", unGpred)
                unGpred = re.sub("\s+", " ", unGpred)
                unGpred = unGpred.rstrip()
                Gpreds1 = [unGpred]
                Gpreds2 = []  # edited
                # extract parameters
                if params == []:
                    Gpreds2 = Gpreds1
                for param in params:
                    pType = re.search("(?s)-\s*(\S+)", param).group(1)
                    # print (pType)
                    try:
                        T = self.Types.GetDescendant(pType)
                    except:
                        raise ValueError(pType, "is causeing problems")
                    objs = []
                    for type in T:
                        if type in self.objects:
                            objs = objs + self.objects[type]
                    for obj in objs:
                        for gpred in Gpreds1:
                            pp = re.search("\?\S+", param).group(0)
                            p = re.sub("\\" + pp, obj, gpred)
                            Gpreds2.append(p)
                    Gpreds1 = Gpreds2
                    Gpreds2 = []
                self.functions = self.functions + Gpreds1
            for i in range(0, len(self.functions)):
                self.functions[i] = re.sub("\s+", "_", self.functions[i])
            # print(self.functions)
        print("DONE", flush=True)

        # ########################
        # durative actions
        # ########################
        print("Grounding durative actions ............ ", end='', flush=True)
        for action in re.findall("(?s)(?=(\(:durative-action.*?\(:))", unGacts):
            m = re.search(
                "(?s)\(:durative-action\s*(\S+)\s*:parameters\s*\((.*?)\)\s*:duration\s*\((.*?)\)\s*:condition\s*\(\s*(.*?)\)\s*:effect\s*\((.*?)\)\s*\)\s*\(:",
                action)
            name = m.group(1)
            params = m.group(2)
            duration = m.group(3)
            rawParamsList = re.findall("(\?.*?)\s+\-\s*(\S+)", params)
            paramsList = []
            for t in rawParamsList:
                pps = re.findall("\?\S+", t[0])
                for pp in pps:
                    paramsList.append((pp, t[1]))

            conditions = m.group(4)
            andcond = re.search('and\s*\(', conditions)
            if andcond is None:
                conditionsList = ["("+ conditions +")"]
            else:
                neg_cond = re.findall("(?s)\(\s*\S+\s*\S+\s*\(\s*not.*?\)\)\)", conditions)
                conditions = re.sub("(?s)\(\s*\S+\s*\S+\s*\(\s*not.*?\)\)\)", "", conditions)
                pos_cond = re.findall("(?s)\(\s*\S+\s*\S+\s*\(.*?\)\)", conditions)
                conditionsList = list(neg_cond) + list(pos_cond)

            effects = m.group(5)
            andeff = re.search('and\s*\(', effects)
            if andeff is None:
                effectsList = ["("+ effects +")"]
            else:
                neg_eff = re.findall("(?s)\(\s*\S+\s*\S+\s*\(\s*not.*?\)\)\)", effects)
                effects = re.sub("(?s)\(\s*\S+\s*\S+\s*\(\s*not.*?\)\)\)", "", effects)
                pos_eff = re.findall("(?s)\(\s*\S+\s*\S+\s*\(.*?\)\)", effects)
                effectsList = neg_eff + pos_eff

            allCondeff = []
            for c in conditionsList:
                allCondeff.append([c, 0])
            for e in effectsList:
                allCondeff.append([e, 1])

            actionlist1 = [[name, allCondeff, duration]]
            actionlist2 = []
            for paramPair in paramsList:
                acceptableTypes = self.Types.GetDescendant(paramPair[1])
                acceptableObjects = []
                for type in acceptableTypes:
                    if type in self.objects:
                        acceptableObjects = acceptableObjects + self.objects[type]

                # start iterating over all conditions and create new actions
                for action in actionlist1:
                    actionName = action[0]
                    actionConditions = action[1]

                    for accobj in acceptableObjects:
                        newActionConditions = []
                        for cond in actionConditions:
                            # stringtosub = "\\"+paramPair[0]+r"[[:>:]]"
                            stringtosub = "\\"+paramPair[0]+r"\b"
                            # print (stringtosub, accobj)
                            newCond = re.sub(stringtosub, accobj, cond[0])
                            # print("original: ", cond[0], "Param: ", stringtosub, "new: ", newCond)
                            newActionConditions.append([newCond, cond[1]])
                        actionlist2.append([actionName + self.delimiter + accobj, newActionConditions, duration])
                actionlist1 = actionlist2
                actionlist2 = []
            self.operators = self.operators + actionlist1
        print("DONE", flush=True)


        print("Parsing problem init and goal ......... ", end='', flush=True)
        m = re.search("(?s)\(:init\s*(.*?)\)\s*\(:goal\s*\(and\s*(.*?)\)\s*\)\s*(\(:metric.*)\)", restProblem)
        init = m.group(1)
        # print (init)
        goal = m.group(2)
        self.metric = m.group(3)

        self.init = re.findall("\(.*\)", init)
        # self.init = re.findall("(?s)\(.*?\)", init)
        # print (self.init)
        self.goal = re.findall("(?s)\(.*?\)", goal)
        print("DONE", flush=True)

        print("Generating grounded task .............. ", end='', flush=True)
        self.GenerateGroundedTask(domain, problem)
        print("DONE", flush=True)



    def __RemoveComments(self, txt):
        # txt = re.sub("(?m)^\s*;.*?\n", "\n", txt)
        txt = re.sub("(?m);.*?\n", "\n", txt)
        return txt

    def __RemoveLastBracket(self, txt):
        m = re.search('(?s)(.*)\)',txt)
        txt = m.group(1)
        txt = txt + '\n(:'
        return txt


    def GenerateGroundedTask(self, domainFile, problemFile):
        domainTxt = self.GroundedDomainTxt
        problemTxt = self.GroundedProblemTxt

        # Add predicate to domain
        domainTxt = domainTxt + "\n\t(:predicates\n"
        for pred in self.predicates:
            domainTxt = domainTxt + "\t\t(" + pred + ")\n"
        domainTxt = domainTxt + "\t)\n\n"


        # Add functions to domain
        domainTxt = domainTxt + "\n\t(:functions\n"
        for func in self.functions:
            domainTxt = domainTxt + "\t\t(" + func + ")\n"
        domainTxt = domainTxt + "\t)\n\n"


        for action in self.operators:
            actionTxt = "\t(:durative-action " + action[0] + "\n"
            actionTxt = actionTxt + "\t\t:parameters ()\n"
            actionTxt = actionTxt + "\t\t:duration (" + action[2] + ")\n"
            actionTxt = actionTxt + "\t\t:condition (and\n"
            for cond in action[1]:
                if cond[1] == 0:
                    m = re.search("(.*\()(.*?)(\).*)", cond[0])
                    pre = m.group(1)
                    post = m.group(3)
                    pred = m.group(2)
                    pred = re.sub("\s+","_", pred)
                    # print (pre+pred+post)
                    actionTxt = actionTxt + "\t\t\t" + pre + pred + post + "\n"
            actionTxt = actionTxt + "\t\t)\n"
            actionTxt = actionTxt + "\t\t:effect (and\n"
            for eff in action[1]:
                if eff[1] == 1:
                    m = re.search("(.*\()(.*?)(\).*)", eff[0])
                    pre = m.group(1)
                    post = m.group(3)
                    pred = m.group(2)
                    pred = re.sub("\s+","_", pred)
                    actionTxt = actionTxt + "\t\t\t" + pre + pred + post +"\n"
            actionTxt = actionTxt + "\t\t)\n\t)\n"
            domainTxt = domainTxt + actionTxt + "\n"
        domainTxt = domainTxt + ")\n"



        problemTxt = problemTxt + "\t(:init\n"
        for pred in self.init:
            isFunc = re.search("\(=", pred)
            if isFunc is None:
                p = re.sub("\s+", "_", pred)
                # print (p)
            else:
                func = re.search("\(=\s*\((.*?)\)\s*(.*?)\)", pred)
                p = re.sub("\s+", "_", func.group(1))
                p = "(= (" + p + ") " + func.group(2) + ")"
                # print (p)
            problemTxt = problemTxt + "\t\t" + p + "\n"
        problemTxt = problemTxt + "\t)\n"
        problemTxt = problemTxt + "\t(:goal (and \n"
        for pred in self.goal:
            p = re.sub("\s+", "_", pred)
            problemTxt = problemTxt + "\t\t" + p + "\n"
        problemTxt = problemTxt + "\t))\n"
        problemTxt = problemTxt + "\t" + self.metric
        problemTxt = problemTxt + ")\n"

        # write to grounded domain and problem files
        if domainFile != "":
            domainfh = open(domainFile, "w")
            domainfh.write(domainTxt)
            domainfh.close()

            problemfh = open(problemFile, "w")
            problemfh.write(problemTxt)
            problemfh.close()






