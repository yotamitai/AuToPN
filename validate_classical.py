"""validate a plan"""


def run_classical_plan(init, utility):
    """run the plan from this node and see if the goal is reached"""
    if utility == 'swap':
        origin_node_num, test_node_num, original_plan, test_plan = init[0], init[1], init[2], init[3]
        current_state = list(original_plan.nodes[origin_node_num].facts)
        plan = [list(x)[0].split(' ') for x in test_plan.plan[test_node_num:]]
        actions = test_plan.actions
        goals = test_plan.goals
    elif utility == 'validate':
        plan, actions, goals, initial_state = init[0], init[1], init[2], init[3]
        current_state = list(initial_state)

    """while the terminal node is not reached or the plan fails"""
    for action in plan:
        current_state = do_action(action, actions, current_state)
        """if the plan was not possible- return false"""
        if not current_state:
            return False

    """check if goal achieved"""
    for goal in goals:
        if goal not in current_state:
            return False

    return True


def do_action(action, action_dict, current_state):
    """executing an action/step in the plan"""
    action_name = action[0]
    params = action[1:]
    types = dict(zip(action_dict[action_name].parameters, params))

    """Create new node"""
    new_state = current_state

    """ check that all preconditions hold true"""
    if not check_preconditions(action_name, action_dict, types, new_state):
        return False

    """add effects"""
    new_state = add_effects(action_name, action_dict, types, new_state)

    """del effects"""
    new_state = del_effects(action_name, action_dict, types, new_state)

    return new_state


def check_preconditions(a, action_dict, types, facts):
    """ check that all preconditions hold true"""
    for p in action_dict[a].preconditions:
        precond = [p[0], [types[x] for x in p[1]]]
        if precond not in facts:
            return False
    return True


def add_effects(a, action_dict, types, facts):
    """ add facts """
    for add_effect in action_dict[a].add_effects:
        f = [add_effect[0], [types[x] for x in add_effect[1]]]
        facts.append(f)
    return facts


def del_effects(a, action_dict, types, facts):
    """ delete facts """
    for del_effect in action_dict[a].del_effects:
        the_fact = [del_effect[0], [types[x] for x in del_effect[1]]]
        if the_fact in facts:
            facts.remove(the_fact)
    return facts