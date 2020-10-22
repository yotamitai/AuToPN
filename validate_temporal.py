"""validate a temporal plan"""

import numpy as np
from scipy.optimize import linprog

epsilon = 0.01


def run_temporal_plan(init, utility):
    """run the plan from this node and see if the goal is reached"""
    if utility == 'swap':
        origin_node_num, test_node_num, original_plan, test_plan = init[0], init[1], init[2], init[3]
        plan = [x.action for x in test_plan.nodes][test_node_num:-1]
        history = [x.action for x in original_plan.nodes][:origin_node_num]
        new_plan = history + plan
        """sanity check - snap action plans must have same number of START and END actions"""
        if not len([x for x in new_plan if x[0] == 'START']) == len([x for x in new_plan if x[0] == 'END']):
            return False
        return check_temporal_plan([new_plan, test_plan.actions, test_plan.goals, test_plan.initial_state], 'swap')

    elif utility == 'validate':
        plan, actions, goals, initial_state, schedule = init[0], init[1], init[2], init[3], init[4]
        # get plan with durations
        # plan_with_durations = get_durations(plan, actions)
        # if plan_with_durations:
        #     new_plan = fix_schedule(plan_with_durations)
        #     if new_plan:
        return check_temporal_plan([plan, actions, goals, initial_state, schedule], 'validate')


def end_action(a):
    return tuple(['END'] + list(a[1:]))


def start_action(a):
    return tuple(['START'] + list(a[1:]))


def check_temporal_plan(init, utility):
    plan, actions, goals, initial_state = init[0], init[1], init[2], init[3]
    current_state = list(initial_state)
    """while the terminal node is not reached or the plan fails"""
    for action in plan:
        current_state = do_action(action, actions, current_state)
        """if the plan was not possible- return false"""
        if not current_state:
            return False

        if utility == 'validate':
            schedule = init[4]
            # check durations
            if action[0] == 'START':
                start_time = schedule[plan.index(action)]
                end_time = schedule[plan.index(end_action(action))]
                if round(end_time - start_time, 1) == round(actions[action[1]].duration[0], 1):
                    continue
                else:
                    return False

    """check if goal achieved"""
    for goal in goals:
        if goal not in current_state:
            return False
    return True


def do_action(action, action_dict, current_state):
    """executing an action/step in the plan"""
    stage = action[0]
    action_name = action[1]
    variables = action[2]

    types = dict(zip(action_dict[action_name].parameters, variables))

    """Create new node"""
    new_state = current_state

    """ check that all preconditions hold true"""
    if not check_preconditions(stage, action_name, action_dict, types, new_state):
        return False

    """add effects"""
    new_state = add_effects(stage, action_name, action_dict, types, new_state)

    """del effects"""
    new_state = del_effects(stage, action_name, action_dict, types, new_state)

    return new_state


def check_preconditions(stage, a, action_dict, types, facts):
    """ check that all preconditions hold true"""
    for p in action_dict[a].preconditions:
        if stage.lower() in p:
            precond = [p[0], [types[x] for x in p[1]]]
            if precond not in facts:
                return False
    return True


def add_effects(stage, a, action_dict, types, facts):
    """ add facts """
    if stage == "START":
        for add_effect in action_dict[a].start_add_effects:
            f = [add_effect[0], [types[x] for x in add_effect[1]]]
            facts.append(f)
    else:
        for add_effect in action_dict[a].end_add_effects:
            f = [add_effect[0], [types[x] for x in add_effect[1]]]
            facts.append(f)
    return facts


def del_effects(stage, a, action_dict, types, facts):
    """ delete facts """
    if stage == "START":
        for del_effect in action_dict[a].start_del_effects:
            f = [del_effect[0], [types[x] for x in del_effect[1]]]
            if f in facts:
                facts.remove(f)
    else:
        for del_effect in action_dict[a].end_del_effects:
            f = [del_effect[0], [types[x] for x in del_effect[1]]]
            if f in facts:
                facts.remove(f)
    return facts


def LP(plan, actions):
    """linear program for obtaining schedule"""

    num_vars = len(plan)
    """equations"""
    A_eq = np.zeros((num_vars, num_vars))
    A_lb = np.zeros((num_vars, num_vars))

    """constants"""
    b_eq = np.zeros((num_vars))
    b_lb = np.zeros((num_vars))

    """objective function to minimize"""
    c = np.ones((num_vars))
    """another option"""
    # c = np.zeros((num_vars))
    # c[-1] = 1

    """epsilon seperatation between all actions"""
    for i in range(num_vars - 1):
        A_lb[i][i] = -1
        A_lb[i][i + 1] = 1
        b_lb[i] = epsilon

        if plan[i][0] == 'START':
            indx = plan[i:].index(end_action(plan[i])) + i
            """A_eq - the duration of the actions"""
            A_eq[i][indx] = 1
            A_eq[i][i] = -1
            b_eq[i] = actions[plan[i][1]].duration[1]  # TODO max duration is taken here

    """translate lower bounds to upper bounds"""
    A_ub = -1 * A_lb
    b_ub = -1 * b_lb

    res = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=(0, None)) # options={'sym_pos': False}
    return res
