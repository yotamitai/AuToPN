from PlanGenerator import  PlanGenerator
from PlanHandler import PlanUtils
import sys


def main():
    # domainFile = "Domains/cushingD.pddl"                # optic cannot solve beyond first problem
    # problemFile = "Domains/cushingP.pddl"
    # domainFile = "Domains/floorD.pddl"                     # optic cannot solve beyond first problem
    # problemFile = "Domains/floorP.pddl"
    # domainFile = "Domains/trucksD.pddl"                      # working
    # problemFile = "Domains/trucksP.pddl"
    # domainFile = "Domains/quantumD.pddl"                     # working
    # problemFile = "Domains/quantumP.pddl"
    # domainFile = "Domains/sokobanD.pddl"                    # too large for the grounding process...
    # problemFile = "Domains/sokobanP.pddl"
    # domainFile = "Domains/turnadoD.pddl"                    # optic get stuck - too large space
    # problemFile = "Domains/turnadoP.pddl"
    # domainFile = "Domains/roadD.pddl"                       # too large for the grounding process...
    # problemFile = "Domains/roadP.pddl"
    # domainFile = "Domains/manparD.pddl"                   # formula durations
    # problemFile = "Domains/manparP.pddl"
    # domainFile = "Domains/airD.pddl"                        # vodoo
    # problemFile = "Domains/airP.pddl"
    # domainFile = "Domains/parkingD.pddl"                    # working
    # problemFile = "Domains/parkingP.pddl"
    # domainFile = "Domains/crewD.pddl"                       # working
    # problemFile = "Domains/crewP.pddl"
    # domainFile = "Domains/printerD.pddl"                    # constants
    # problemFile = "Domains/printerP.pddl"
    # domainFile = "Domains/openD.pddl"                       # working
    # problemFile = "Domains/openP.pddl"
    # domainFile = "Domains/matchcelerD.pddl"                 # optic cannot solve
    # problemFile = "Domains/matchcelerP.pddl"
    # domainFile = "Domains/pegD.pddl"                        # too large for optic
    # problemFile = "Domains/pegP.pddl"
    # domainFile = "Domains/storageD.pddl"                  # either predicates
    # problemFile = "Domains/storageP.pddl"
    # domainFile = "Domains/tmsD.pddl"                      # some wierd problem with the object tree
    # problemFile = "Domains/tmsP.pddl"
    domainFile = "Domains/driverD.pddl"                    # working!
    problemFile = "Domains/driverP.pddl"
    # domainFile = "Domains/sateD.pddl"                     # predicates comparison
    # problemFile = "Domains/sateP.pddl"
    # domainFile = "Domains/D.pddl"
    # problemFile = "Domains/P.pddl"


    # Generator = PlanGenerator(domainFile, problemFile, False, PlanU
    # tils.Planner.optic_plus, False, 1)
    # Generator = PlanGenerator(domainFile, problemFile, True, PlanUtils.Planner.optic, True, 1)
    # Generator = PlanGenerator(domainFile, problemFile, False, PlanUtils.Planner.optic, True, 1)
    Generator = PlanGenerator(domainFile, problemFile, False, PlanUtils.Planner.optic_plus, True, 1)      # ungrounded
    # Generator = PlanGenerator(domainFile, problemFile, True, PlanUtils.Planner.optic_plus, True, 1)       # grounded
    # Generator = PlanGenerator(domainFile, problemFile, False, PlanUtils.Planner.scotty, True, 1)

    try:
        for i in range(1):
            # To get the next plan:
            plan = next(Generator)
            print("plan number ", i + 1)

            # To print temporal plan:
            print (plan.PrintPlan())

            # To get the temporal plan tuples list:
            # l = plan.GetPlanAsList()

            # To print the snap action plan:

            # print (plan.PrintSnapPlan())

            # To get the snap action plan tuples list:
            # l = plan.GetSnapPlanAsList()
    except Exception as e:
        print (str(e))
        print ("Could not find a feasible plan")




if __name__ == "__main__":
    main()
