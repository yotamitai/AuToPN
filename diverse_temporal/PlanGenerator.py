from diverse_temporal.PDDL.Grounding import Grounder
import subprocess
from diverse_temporal.PDDL.PDDLSParser import *
from diverse_temporal.PlanHandler.PlanUtils import *
from diverse_temporal.PDDL.PathEliminationCompilation import *
import threading
import sys
import re
import math
import time
import uuid
from tools import DIRECTORIES


class MultiOut(object):
    def __init__(self, *args):
        self.handles = args

    def write(self, s):
        for f in self.handles:
            f.write(s)


class Transcript(object):

    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = filename

    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass



class PlanGenerator():
    def __init__(self, domainFile, problemFile, isGrounded = True, planner = Planner.scotty, verbose = False, timeout = 0):
        """
        constractor for the plan generation object
        :param domainFile: path to the domain file
        :param problemFile: path to the problem file
        :param isGrounded: flag denoting if the pddl files are gounded or lifted
        :param planner: enum denoting the name of the planner to use, options are Planner.Scotty, Planner.Optic.
                if not specified Planner.Scotty is used
        :param verbose: flag denoting if the planner should output the progress to the standart output, False if not specified valid only for Scotty
        :param timeout: timeout to wait for completion of external planner job, if not specified the time is unbounded
        """
        self.process = None
        self.status = None
        self.error = ""
        self.output = ""
        self.timeout = timeout
        self.verbose = verbose
        self.k = 0
        self.domainFile = domainFile
        self.problemFile = problemFile
        self.OUT_DIR = DIRECTORIES["PLAN_OUTPUT_DIR"] #"diverse_temporal/Dumps/"
        self.JSON_FILE = self.OUT_DIR + "/plan_results.json"
        self.OPTIC_OUT = self.OUT_DIR + "/optic.out"
        self.BASE_DOMAIN = self.OUT_DIR + "/groundedDomain.pddl"
        self.BASE_PROBLEM = self.OUT_DIR + "/groundedProblem.pddl"
        self.TEMP_DOMAIN = self.OUT_DIR + "/domain.pddl"
        self.TEMP_PROBLEM = self.OUT_DIR + "/problem.pddl"
        self.planner = planner
        self.eliminationMaps = []

        # Ground if ungrounded
        if isGrounded == False:
            G = Grounder(self.domainFile, self.problemFile)
            G.Ground(self.BASE_DOMAIN, self.BASE_PROBLEM)
        else:
            self.BASE_DOMAIN = self.domainFile
            self.BASE_PROBLEM = self.problemFile

        # Generate the first temp copy of the task
        task = PDDLSParser(self.BASE_DOMAIN, self.BASE_PROBLEM).GetParsedInstance()
        task.GenerateDomainFile(self.TEMP_DOMAIN)
        task.GenerateProblemFile(self.TEMP_PROBLEM)

        # Setup the planner
        if planner == Planner.scotty:
            self.plannerCMD = ["diverse_temporal/scotty/scotty", "-o", self.JSON_FILE, "--search-method", "astar", self.TEMP_DOMAIN, self.TEMP_PROBLEM]
        elif planner == Planner.optic_plus:
            self.plannerCMD = ["diverse_temporal/Optic/rewrite-no-lp_new", "--total-order-search", self.TEMP_DOMAIN, self.TEMP_PROBLEM ]
        else:
            self.plannerCMD = ["diverse_temporal/Optic/optic-clp", "-N", "-T", "-b", self.TEMP_DOMAIN, self.TEMP_PROBLEM]



    def Reset(self):
        """
        Reset the iterative planning problem to its initial state, all compilations are deleted
        :return:
        """
        # Generate the first temp copy of the task
        self.eliminationMaps = []
        self.k = 0
        task = PDDLSParser(self.BASE_DOMAIN, self.BASE_PROBLEM).GetParsedInstance()
        task.GenerateDomainFile(self.TEMP_DOMAIN)
        task.GenerateProblemFile(self.TEMP_PROBLEM)

    def RunPlanner(self):
        """
        thread worker function to run the planner external subprocess
        :return:
        """
        output_text = ""
        self.process = subprocess.Popen(self.plannerCMD, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(self.process.stdout.readline, ""):
            line = stdout_line
            output_text = output_text+line
            if self.verbose:
                print(line.rstrip())
        self.process.stdout.close()
        return_code = self.process.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, self.plannerCMD)

        if self.planner == Planner.optic_plus or self.planner == Planner.optic:
            f = open(self.OPTIC_OUT, 'w')
            f.write(output_text)
            f.flush()
            f.close()



    def __iter__(self):
        return self

    def __next__(self):
        """
        iterator for the plan generation object
        :return:
        TemporalPlan object
        """
        PlannerThread = threading.Thread(target=self.RunPlanner())
        PlannerThread.start()

        if self.timeout > 0:
            PlannerThread.join(self.timeout*60)
            if PlannerThread.is_alive():
                self.process.terminate()
                PlannerThread.join()
                raise TimeoutError("planner exceeded allowed running time without finding a feasible plan")
        else:
            PlannerThread.join()



        if self.planner == Planner.scotty:
            try:
                planReader = TemporalPlanReader(self.planner, self.JSON_FILE).GetPlan()     # IntrimTemporalPlan
            except:
                raise StopIteration("Scotty could not find any feasible plan")
        else:
            try:
                planReader = TemporalPlanReader(self.planner, self.OPTIC_OUT).GetPlan()
            except:
                raise StopIteration("Optic could not find any feasible plan")

        plan = planReader.GetPlanObject(self.eliminationMaps)       # TemporalPlan
        plan4Seq = planReader.GetSnapPlan()                         # {TemporalEvent}
        planSeq = PlanSequence(plan4Seq)

        task = PDDLSParser(self.TEMP_DOMAIN, self.TEMP_PROBLEM).GetParsedInstance()
        instanceCompiler = CompiledPlanningInstance(task, planSeq, self.k + 1)
        instanceCompiler.Compile()
        self.eliminationMaps.insert(0, instanceCompiler.GetTansformation())
        instanceCompiler.GenerateCompiledDomainFile(self.TEMP_DOMAIN)
        instanceCompiler.GenerateCompiledProblemFile(self.TEMP_PROBLEM)
        self.k = self.k + 1

        return plan


