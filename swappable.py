import time
from collections import defaultdict
from itertools import combinations

from tools import *
from validate_classical import run_classical_plan
from validate_temporal import run_temporal_plan


def swap(node1, plan1, node2, plan2):
    """check if 2 nodes can swap plans"""

    # if terminal node reached
    if not plan1.nodes[node1].action or not plan2.nodes[node2].action:
        return False

    # calling functions by name from a dictionary (!)
    functions = {'Classical': run_classical_plan,'Temporal': run_temporal_plan}
    problem_type = TEST_PARAMS['PROBLEM_TYPE']

    """only return true if both can be swapped"""
    swap_1 = node1, node2, plan1, plan2
    swap_2 = node2, node1, plan2, plan1

    bool_list = [functions[problem_type](swap_1, 'swap'), functions[problem_type](swap_2, 'swap')]
    if sum(bool_list) == 2:
        return 'Full'
    elif sum(bool_list) == 1:
        return 'Semi'
    else:
        return False

    # if TEST_PARAMS['PROBLEM_TYPE'] == "Temporal":
    #     bool_list = [run_temporal_plan(swap_1, 'swap'), run_temporal_plan(swap_2, 'swap')]
    #     if sum(bool_list) == 2:
    #         return 'Full'
    #     elif sum(bool_list) == 1:
    #         return 'Semi'
    #     else:
    #         return False
    # else:
    #     bool_list = [run_classical_plan(swap_1, 'swap'), run_classical_plan(swap_2, 'swap')]
    #     if sum(bool_list) == 2:
    #         return 'Full'
    #     elif sum(bool_list) == 1:
    #         return 'Semi'
    #     else:
    #         return False


def swappable(plans):
    """brute force check swap possibility between all nodes of all plans"""
    compatibility = defaultdict(list)
    for pair in combinations(plans, 2):
        p1 = pair[0].plan_num
        p2 = pair[1].plan_num
        for ni in range(1, len(pair[0].nodes)):
            for nj in range(1, len(pair[1].nodes)):
                result = swap(ni, plans[p1], nj, plans[p2])
                if result:
                    plan_pair = ((p1, ni), (p2, nj))
                    compatibility[result].append(plan_pair)

    return compatibility


