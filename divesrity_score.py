from itertools import combinations

from tools import *


def get_similar(sim, p0, p1):
    if p0 in sim.keys():
        sim[p0].append(p1)
    else:
        flag = True
        for v in sim.values():
            if p0 in v:
                flag = False
                break
            flag = True

        if flag:
            sim[p0] = [p0, p1]


def action_diversity(set_plans, plans_list):
    a_d = {}
    similar_plans = []
    for plan in combinations(plans_list, 2):
        p1 = set_plans[plan[0]]
        p2 = set_plans[plan[1]]
        sym_diff = len(p1.symmetric_difference(p2))
        accumulated = len(p1) + len(p2)
        distance = float(sym_diff) / accumulated

        a_d[plan] = distance

        if not sym_diff:
            if similar_plans:
                for grp in similar_plans:
                    if plan[0] in grp or plan[1] in grp:
                        grp += [plan[0], plan[1]]
            else:
                similar_plans += [[plan[0], plan[1]]]

    similar_dict = {}
    for i in range(len(similar_plans)):
        grp = set(tuple(similar_plans[i]))
        similar_dict[i] = tuple(grp)

    return a_d, similar_dict


def landmark_diversity(plans_string, landmark_list, plan_lm_dict):
    lm_dist = {}
    similar_plans = {}
    n_disjunct_lm = len([x for x in landmark_list if len(x) > 1])
    for plan in combinations(plans_string, 2):
        value = 0
        for lm in landmark_list:
            lm_i = landmark_list.index(lm)
            lm_p1 = set(plan_lm_dict[plan[0]][lm_i])
            lm_p2 = set(plan_lm_dict[plan[1]][lm_i])
            sym_diff = len(lm_p1.symmetric_difference(lm_p2))
            accumulated = len(lm_p1.union(lm_p2))
            fraction = float(sym_diff) / accumulated
            value += fraction

        distance = 1.0 / n_disjunct_lm * value
        lm_dist[plan] = distance

    return lm_dist, similar_plans


def maximal_set(dist_mat, plans_list, k, plans, zero_diversity_dict):
    """ get the maximal diversity set"""

    if OPTIMIZATIONS['PLANSET_DIV'] == 'Max':
        relevant_plan_list = get_non_zero_plans(plans_list, k, zero_diversity_dict, plans)

        set_dict = {}
        for c in combinations(relevant_plan_list, k):
            set_dict[c] = Div(c, dist_mat)
        max_val = max(set_dict.values())
        max_list = [x for x in set_dict if set_dict[x] == max_val]
        """get random max value plan pair:"""
        set_plans = random.choice(max_list)
    else:
        max_val = Div(plans_list, dist_mat)
        set_plans = plans_list

    zero_list = []
    for z in zero_diversity_dict:
        zero_list += zero_diversity_dict[z]
    num_zero_plans = sum([1 for x in set_plans if x in zero_list]) - len(zero_diversity_dict)

    return set_plans, max_val, num_zero_plans


def get_non_zero_plans(p_list, k, zero_dict, plans):
    """removes plans that have zero diversity and returns the relevant plans"""

    new_list = []
    zero_list = []
    """add 1 plan from each plan cluster"""
    for z in zero_dict:
        if OPTIMIZATIONS['SHORT-PLANS']:
            """we prefer saving the first plans as they will more often be shorter and better"""
            s = [len(plans[y]) for y in zero_dict[z]]
            idx = s.index(min(s))
            new_list.append(zero_dict[z][idx])
        else:
            new_list.append(random.choice(zero_dict[z]))

        zero_list += zero_dict[z]

    """add all unique plans"""
    unique_list = [x for x in p_list if x not in zero_list]
    for u in unique_list:
        new_list.append(u)

    """if needed, add more similar plans"""
    for i in range(k-len(new_list)):
        y = [j for j in zero_list if j not in new_list]
        x = random.choice(y)
        new_list.append(x)

    return sorted(new_list)


def Div(plan_set, dist_mat):
    """Div(Pi) - The diversity score of a given plan set Pi"""
    keys = []
    for c in combinations(plan_set, 2):
        keys.append(c)
    return sum([dist_mat[x] for x in keys])/(len(keys))


def get_plan_states():
    abs_file_path = DIRECTORIES["PLAN_OUTPUT_DIR"] + '/states.py'
    plan_states = {}
    i = 0
    file_object = open(abs_file_path, 'r')
    x = file_object.readline()
    my_list = []
    x = x[14:].replace(' ', '').replace('"', '').replace("\n", "").split(';')
    my_list.append(x)
    x = file_object.readline()
    while x:
        x = x.replace(' ', '').replace('"', '').replace("\n", "").split(';')
        my_list.append(x)
        x = file_object.readline()
        if "],[" in x:
            plan_states[i] = my_list
            i += 1
            my_list = []
            x = x[3:]
    plan_states[i] = my_list[:-1]
    file_object.close()

    return plan_states


def get_landmark_diversity(plans, new_plan_states, n_set_plans, landmark_set):

    """for each plan, find its specific disjunctive landmarks from the state space of the plan"""
    plans_lm_dict = {}
    for i in plans:
        plan = new_plan_states[i - 1]
        plan_lm = defaultdict(lambda: [])
        for state in plan:
            for disjunc_lm in landmark_set:
                disj_i = landmark_set.index(disjunc_lm)
                for lm in disjunc_lm:
                    if lm in plan_lm[disj_i]:
                        continue
                    if lm in state:
                        plan_lm[disj_i].append(lm)
        plans_lm_dict[i] = plan_lm

    """create plan "combinations" string"""
    plan_list = sorted(plans_lm_dict.keys())
    """get diversity scores"""
    plan_distances, no_diversity_dict = landmark_diversity(plan_list, landmark_set, plans_lm_dict)
    """find maximal diversity"""
    plan_set, lm_diversity_score, n_zero_div_plans = maximal_set(plan_distances, plan_list, n_set_plans,
                                                                 plans, no_diversity_dict)
    """return diversity"""
    best_diversity_score = lm_diversity_score

    return best_diversity_score, plan_set, plan_distances


def get_action_diversity(plans, n_set_plans):
    """get the set of unique actions in each plan"""
    set_plans = {}
    for i in plans:
        if TEST_PARAMS['PROBLEM_TYPE'] == 'Temporal':
            set_plans[i] = set(([x[0] for x in plans[i].actions]))
        else:
            set_plans[i] = set(plans[i])

    plan_list = sorted(set_plans.keys())
    """get diversity scores"""
    plan_distances, no_diversity_dict = action_diversity(set_plans, plan_list)

    """find maximal diversity"""
    plan_set, diversity_of_planset, n_zero_div_plans = maximal_set(plan_distances, plan_list, n_set_plans,
                                                                plans, no_diversity_dict)
    """return diversity"""
    return diversity_of_planset, plan_set, plan_distances


def get_landmark_set():
    abs_file_path = DIRECTORIES["PLAN_OUTPUT_DIR"] + '/landmarks.py'
    landmarks = []
    file_object = open(abs_file_path, 'r')
    x = file_object.readline()
    x = file_object.readline()
    while x:
        x = x.replace("\n", "").replace(' ', '').replace('"', '').split(';')
        landmarks.append(x)
        x = file_object.readline()[2:]
    file_object.close()

    return landmarks


def get_plan_set(plans, n_set_plans):
    """retrive the plan-set """

    # TODO not implemented for temporal. also missing work on zero diversity plan choice
    # """LANDMARK DIVERSITY"""
    # if TEST_PARAMS['DIVERSITY'] == 'landmark':
    #     """load plan states"""
    #     plan_states = get_plan_states()
    #     landmark_set = get_landmark_set()
    #     best_diversity_score, plan_set, plan_distances = get_landmark_diversity(plans, plan_states, n_set_plans, landmark_set)

    """ACTION SET DIVERSITY"""
    diversity_of_planset, plan_set, plan_distances = get_action_diversity(plans, n_set_plans)

    """get max diversity between 2 plans"""
    keys = []
    for c in combinations(plan_set, 2):
        keys.append(c)
    max_div_in_planset = max([plan_distances[x] for x in keys])

    return list(plan_set), diversity_of_planset, max_div_in_planset
