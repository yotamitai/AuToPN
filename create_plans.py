import copy

from tools import *


# -----------------------------------CLASSICAL------------------------------------------
class ClassicalNode:
    def __init__(self, facts, parent):
        self.facts = sorted(facts)
        self.parent = parent
        self.child = []
        self.action = []
        self.node_id = []
        self.landmark_achieved = None


class FullClassicalPlan:
    def __init__(self, actions, initial_state, goals, plan, plan_num):
        self.actions = actions
        self.initial_state = initial_state
        self.goals = goals
        self.plan = plan.plan_actions
        self.nodes = []
        self.plan_num = plan_num
        self.ordered_lm = []

    def construct_plan(self):
        """constructing a plan"""
        self.nodes.append(ClassicalNode(list(self.initial_state), None))
        current_node = self.nodes[-1]
        current_node.node_id = 0

        """follow the plan from start till end and retrieve facts"""
        for step in self.plan:
            params = step[0].split()
            assert params[0] in self.actions, "unknown action in plan"
            current_node.action = tuple(params)
            node_index = current_node.node_id
            current_node = self.do_action(params[0], params[1:], current_node)
            current_node.node_id = node_index + 1
            # make this new node the child of the last node
            self.nodes[-2].child = current_node
        # edit the last node's child
        self.nodes[-1].child = 'Terminal'

        return

    def do_action(self, action, params, current_node):
        """executing an action/step in the plan"""
        types = dict(zip(self.actions[action].parameters, params))

        """Create new node"""
        new_node = ClassicalNode(copy.copy(current_node.facts), current_node)
        self.nodes.append(new_node)

        """ check that all preconditions hold true"""
        self.check_preconditions(action, types, new_node.facts)

        """add effects"""
        new_node.facts, new_facts = self.add_effects(action, types, new_node.facts)

        """check if sub-goal and landmark achieved"""
        for fact in new_facts:
            for lm in TEST_PARAMS['LANDMARKS']:
                if fact in lm:
                    self.ordered_lm.append([str(TEST_PARAMS['LANDMARKS'].index(lm)), len(self.nodes)])
                    new_node.landmark_achieved = TEST_PARAMS['LANDMARKS'].index(lm)

        """del effects"""
        new_node.facts = self.del_effects(action, types, new_node.facts)

        """sort facts in node (will be used for comparing nodes later on)"""
        new_node.facts.sort()

        return new_node

    def check_preconditions(self, action, types, facts):
        """ check that all preconditions hold true"""
        for p in self.actions[action].preconditions:
            precond = [p[0], [types[x] for x in p[1]]]
            assert precond in facts, "Illegal action- Precondition does not hold"
        return

    def add_effects(self, action, types, facts):
        """ add facts """
        new_facts = []
        for add_effect in self.actions[action].add_effects:
            f = [add_effect[0], [types[x] for x in add_effect[1]]]
            if f not in facts:
                facts.append(f)
                new_facts.append(f)
        return facts, new_facts

    def del_effects(self, action, types, facts):
        """ delete facts """
        for del_effect in self.actions[action].del_effects:
            f = [del_effect[0], [types[x] for x in del_effect[1]]]
            if f in facts:
                facts.remove(f)
        return facts

    # def get_future_landmarks(self):
    #     future_lm_set = []
    #     for node in reversed(self.nodes):
    #         node.future_lm = copy.copy(future_lm_set)
    #         if node.landmark_achieved in range(len(TEST_PARAMS['LANDMARKS'])):
    #             if node.landmark_achieved not in future_lm_set:
    #                 future_lm_set.append(node.landmark_achieved)
    #                 future_lm_set.sort()
    #     return
    #
    # def get_past_landmarks(self):
    #     past_lm_set = []
    #     for node in self.nodes:
    #         node.past_lm = copy.copy(past_lm_set)
    #         if node.landmark_achieved in range(len(TEST_PARAMS['LANDMARKS'])):
    #             if node.landmark_achieved not in past_lm_set:
    #                 past_lm_set.append(node.landmark_achieved)
    #                 past_lm_set.sort()
    #     return


# -----------------------------------TEMPORAL------------------------------------------

class TemporalNode:
    def __init__(self, facts, parent, time):
        self.facts = sorted(facts)
        self.parent = parent
        self.child = []
        self.action = []
        self.num = 0
        self.time = time


class FullTemporalPlan:
    def __init__(self, actions, initial_state, goals, plan, plan_num):
        self.actions = actions
        self.initial_state = initial_state
        self.goals = goals
        self.events = plan.events
        rounded_snap_actions = []
        for s_a in plan.snap_actions:
            temp = list(s_a)
            temp[2] = round(temp[2], 6)
            rounded_snap_actions.append(tuple(temp))
        self.snap_actions = rounded_snap_actions
        self.nodes = []
        self.plan_num = plan_num
        self.plan = plan
        self.steps = plan.steps
        self.epsilon = 0.01

    def split_activity(self, activity):
        temp = activity[4].replace(' ', '').split('--')
        [stage, action], variables = temp[0].split('-'), tuple(temp[1:])
        params = activity[:4]
        time = params[1]
        return (stage, action, variables, time, params)


    def construct_plan(self):
        """constructing a plan"""
        self.nodes.append(TemporalNode(list(self.initial_state), None, 0))
        current_node = self.nodes[0]
        current_node.num = 0

        """follow the plan from start till end and retrieve facts"""
        indx = 0
        for step in self.snap_actions:
            current_node.action = self.split_activity(step)
            current_node.node_id = indx
            current_node = self.do_action(current_node)
            # make this new node the child of the last node
            self.nodes[-2].child = current_node
            indx += 1
        # edit the last node's child
        self.nodes[-1].child = 'Terminal'

        return

    def do_action(self, current_node):
        """executing an action/step in the plan"""
        stage, action, variables, time, params = current_node.action
        types = dict(zip(self.actions[action].parameters, variables))

        """Create new node"""
        new_node = TemporalNode(copy.copy(current_node.facts), current_node, current_node.time)
        self.nodes.append(new_node)

        """ check that all preconditions hold true"""
        self.check_preconditions(stage, action, types, current_node.facts)

        """add effects"""
        new_node.facts = self.add_effects(stage, action, types, new_node.facts)

        """del effects"""
        new_node.facts = self.del_effects(stage, action, types, new_node.facts)

        """time"""
        new_node.time = params[1]

        """sort facts in node (will be used for comparing nodes later on)"""
        new_node.facts.sort()

        return new_node

    def check_preconditions(self, stage, action, types, facts):
        """ check that all preconditions hold true"""
        for p in self.actions[action].preconditions:
            if stage.lower() in p:
                precond = [p[0], [types[x] for x in p[1]]]
                try:
                    assert precond in facts, "Illegal action- Precondition does not hold"
                except:
                    print('illegal action')
        return

    def add_effects(self, stage, action, types, facts):
        """ add facts """
        if stage == "START":
            for add_effect in self.actions[action].start_add_effects:
                f = [add_effect[0], [types[x] for x in add_effect[1]]]
                if f not in facts:
                    facts.append(f)
        else:
            for add_effect in self.actions[action].end_add_effects:
                f = [add_effect[0], [types[x] for x in add_effect[1]]]
                if f not in facts:
                    facts.append(f)
        return facts

    def del_effects(self, stage, action, types, facts):
        """ delete facts """
        if stage == "START":
            for del_effect in self.actions[action].start_del_effects:
                f = [del_effect[0], [types[x] for x in del_effect[1]]]
                if f in facts:
                    facts.remove(f)
        else:
            for del_effect in self.actions[action].end_del_effects:
                f = [del_effect[0], [types[x] for x in del_effect[1]]]
                if f in facts:
                    facts.remove(f)
        return facts