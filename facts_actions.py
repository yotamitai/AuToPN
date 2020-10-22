"""FACTS and ACTIONS"""
from tools import *

class Action:
    def __init__(self, action):
        self.name = str(action.name).lower()
        self.parameters = [str(x.arg_name) for x in action.parameters.args]
        self.preconditions = self.get_preconditions(action.pre)
        self.add_effects, self.del_effects = self.get_effects(action.eff)

    def get_preconditions(self, p):
        preconditions = []
        for precondition in p.subformulas:
            if hasattr(precondition, 'subformulas'):
                assert precondition.subformulas[0].name, 'Failure due to Negative Preconditions'
                preconditions += [[str(precondition.subformulas[0].name),
                                  [str(x.arg_name) for x in precondition.subformulas[0].args.args]]]
            else:
                preconditions += [[str(precondition.name),
                                   [str(x.arg_name) for x in precondition.args.args]]]
        return preconditions

    def get_effects(self, e):
        effects_add, effects_del = [], []
        for effect in e:
            if effect.op:
                effects_del += [[str(effect.subformulas[0].name),
                                [str(x.arg_name) for x in effect.subformulas[0].args.args]]]
            else:
                effects_add += [[str(effect.subformulas[0].name),
                                [str(x.arg_name) for x in effect.subformulas[0].args.args]]]
        return effects_add, effects_del


class DurativeAction:
    def __init__(self, action):
        self.name = str(action.name).lower()
        self.parameters = [str(x.arg_name) for x in action.parameters.args]
        self.preconditions = self.get_durrative_preconditions(action.cond)
        self.start_add_effects, self.end_add_effects, self.end_del_effects, self.start_del_effects = \
            self.get_durrative_effects(action.eff)
        try:
            self.duration = (action.duration_lb.val, action.duration_ub.val)
        except:
            raise Exception("Cant handle variable dependent action durations")

    def get_durrative_preconditions(self, a):
        preconditions = []
        for pre in a:
            sub_formula = pre.formula.subformulas[0]
            preconditions += [[str(sub_formula.name), [str(x.arg_name) for x in sub_formula.args.args],
                             str(pre.timespecifier)]]
        return preconditions

    def get_durrative_effects(self, e):
        effects_add, effects_del = [], []
        for effect in e:
            sub_formula = effect.formula.subformulas[0]
            if effect.formula.op:
                effects_del += [[str(sub_formula.name), [str(x.arg_name) for x in sub_formula.args.args],
                                 str(effect.timespecifier)]]
            else:
                effects_add += [[str(sub_formula.name), [str(x.arg_name) for x in sub_formula.args.args],
                                 str(effect.timespecifier)]]

        effects_add_start = [x[:-1] for x in effects_add if x[-1] == 'start']
        effects_add_end = [x[:-1] for x in effects_add if x[-1] =='end']
        effects_del_end = [x[:-1] for x in effects_del if x[-1] == 'end']
        effects_del_start = [x[:-1] for x in effects_del if x[-1] == 'start']

        return effects_add_start, effects_add_end, effects_del_end, effects_del_start


def collect_facts_actions(domain, problem):
    i = get_initial_state(problem.initialstate)
    g = get_goal_state(problem.goal)
    if domain.actions:
        a = get_actions(domain.actions)
    if domain.durative_actions:
        a = get_temporal_actions(domain.durative_actions)
    return a, i, g


def get_actions(a):
    actions_dic = {}
    for action in a:
        actions_dic[str(action.name).lower()] = Action(action)
    return actions_dic


def get_temporal_actions(a):
    actions_dic = {}
    for action in a:
        actions_dic[str(action.name).lower()] = DurativeAction(action)
    return actions_dic


def get_initial_state(i):
    initial_state = []
    for proposition in i:
        if not hasattr(proposition, 'subformulas'):
            continue
        initial_state.append([str(proposition.subformulas[0].name), [str(x.arg_name) for x in proposition.subformulas[0].args.args]])
    return tuple(initial_state)


def get_goal_state(g):
    goal_state = []
    for goal in g.subformulas:
        goal_state.append([str(goal.subformulas[0].name), [str(x.arg_name) for x in goal.subformulas[0].args.args]])
    return tuple(goal_state)


