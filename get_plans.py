import gc

from tools import *
import logging
from diverse_temporal.PlanGenerator import PlanGenerator
from diverse_temporal.PlanHandler import PlanUtils
import subprocess, signal


class Plan:

    def __init__(self, first_action, last_action, plan_actions, number):
        self.first_action = first_action
        self.last_action = last_action
        self.plan_actions = plan_actions
        self.number = number


def generate_plans(p_type, domain_path, problem_path, num_sol, planner_name, verbose, is_grounded):
    """this function generates the diverse plans"""
    unique_id = None
    """call the planner"""
    if p_type == 'Temporal':
        cleanup(DIRECTORIES["PLAN_OUTPUT_DIR"])

        if planner_name == 'scotty':
            Planner = PlanUtils.Planner.scotty
        elif planner_name == 'optic_plus':
            Planner = PlanUtils.Planner.optic_plus
        else:
            Planner = PlanUtils.Planner.optic

        print('TEMPORL PLANNER: %s' %planner_name)
        Generator = PlanGenerator(domain_path, problem_path, is_grounded, Planner, verbose, timeout=30)
        try:
            for i in range(num_sol):
                plan = next(Generator)
                save_object(plan, 'templan' +str(i), DIRECTORIES['PLAN_OUTPUT_DIR'])
                print('plan #%d found' %i)
        except Exception as e:
            print("Could not find a feasible plan")
            logging.info(f'EXCEPTION - {e}')
            return False, "Could not find a feasible plan"

    else: # Classical
        """clear content of output folder"""
        cleanup(DIRECTORIES["PLAN_OUTPUT_DIR"])
        try:
            call_diverse_planner(domain_path, problem_path, num_sol)
        except Exception as e:
            print(f"Could not find a feasible plan - Exception:\n{e}")
            logging.info(f'EXCEPTION - {e}')
            # p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
            # out, err = p.communicate()
            # for line in out.splitlines():
            #     if 'downward' in str(line):
            #         pid = int(line.split(None, 1)[0])
            #         os.kill(pid, signal.SIGKILL)
            #         break

            return False, "Could not find a feasible plan"

    os.chdir(DIRECTORIES["OUTPUT_DIR"])
    return True, 'Plans found'


def load_temporal_plans():
    path = DIRECTORIES["PLAN_OUTPUT_DIR"]
    plans = {}
    for f in os.listdir(path):
        if "templan" in f:
            plan_num = int(f[7:])
            plan = load_object(f, DIRECTORIES['PLAN_OUTPUT_DIR'])
            plan.snap_actions = plan.GetSnapPlanAsList()
            plan.actions = plan.GetPlanAsList()
            plans[plan_num] = plan
    return plans

def load_classical_plans():
    """load all plans"""
    path = DIRECTORIES["PLAN_OUTPUT_DIR"]
    plans = {}
    for f in os.listdir(path):
        abs_file_path = path + '/' + f
        if "sas_plan" in f:
            plan_num = int(f[9:])
            # if plan_num > n:
            #     continue
            file_object = open(abs_file_path, 'r')
            x = file_object.readline()
            my_list = []
            while x:
                my_list.append(tuple([x[x.find("(") + 1:x.find(")")]]))
                x = file_object.readline()
            file_object.close()
            my_list = my_list[:-1]
            if tuple(my_list) not in list(plans.values()):
                plans[plan_num] = tuple(my_list)
    return plans


def load_plans(plans, specific_plans):
    tpn_plans = []
    for i in specific_plans:
        plan = plans[i]
        tpn_plans.append(Plan(plan[0], plan[-1], plan, i))
    return tpn_plans
