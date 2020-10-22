import copy
from collections import defaultdict

from tools import *
from validate_temporal import *
from validate_classical import *
from visualize import visualize


class TPN:
    def __init__(self, plans, merges, merged_nodes, merge_objects, problem_type):
        self.graph = defaultdict(list)
        self.merge_sequence = merges
        self.merged_nodes = merged_nodes
        self.merge_objects = merge_objects
        self.planning_problem_type = problem_type

        # for reference
        self.plans = plans
        self.domain_actions = plans[0].actions
        self.goals = plans[0].goals
        self.initial_state = plans[0].initial_state
        self.no_additional_semi_compatible_pairs = False
        self.compatibility_method = None

    def addEdge(self, u, v):
        if v not in self.graph[u]:
            self.graph[u].append(v)

    def check_if_merged(self, plan_and_node):
        """check if this merged node already exists, if so merge to it, else create new one"""
        if plan_and_node in self.merged_nodes.keys():
            merge_name = self.merged_nodes[plan_and_node]
            return merge_name

        return plan_and_node

    def getAllPaths(self, s, d):
        """Prints all paths from 's' to 'd'"""
        self.all_node_paths = []
        visited = defaultdict(lambda: False)
        path = []
        self.getAllPathsUtil(s, d, visited, path)

    def getAllPathsUtil(self, u, d, visited, path):
        """recursive helper function"""
        visited[u] = True
        path.append(u)
        if u == d:
            if tuple(path) not in self.all_node_paths:
                self.all_node_paths.append(tuple(path))

        else:
            for i in set(self.graph[u]):
                if not visited[i]:
                    self.getAllPathsUtil(i, d, visited, path)
        path.pop()
        visited[u] = False

    def get_edges_and_nodes(self):
        """add edges between nodes in the graph"""
        for plan in self.plans:
            current_node_str = 'I'
            for node in plan.nodes[1:-1]:
                next_node = (plan.plan_num, node.node_id)
                next_node = self.check_if_merged(next_node)
                self.addEdge(current_node_str, next_node)
                current_node_str = next_node
            self.addEdge(current_node_str, 'T')
        """get number of nodes in graph"""
        self.nodes = list(self.graph.keys()) + ['T']

    def tpn_solution_actions(self, p_type):
        """get all action sequence plans available from the tpn"""
        # get the initial actions
        initial_actions = self.get_initial_actions(p_type)
        # get all actions originating from merged nodes
        self.get_actions_from_merge(p_type)
        # get action sequences
        solution_actions = self.get_solution_actions(p_type, initial_actions)
        if p_type == 'Temporal':
            solution_actions = self.fix_solution_actions(solution_actions)
        # remove duplicates
        self.solution_actions = tuple(set([tuple(x) for x in solution_actions]))
        # self.solution_actions_original_length = len(solution_actions)

    def fix_solution_actions(self, solutions):
        """make sure the merged start action is the same as it's end action"""
        new_solutions = []
        for solution in solutions:
            # number of start actions must be same as number of end actions
            if len([x for x in solution if x[0] == 'START']) == len([x for x in solution if x[0] == 'END']):
                new_solutions.append(solution)

            # 'All START actions have an END action'
            if not ([y for y in [x[1:3] for x in solution if x[0] == 'START']
                     if y not in [k[1:3] for k in solution if k[0] == 'END']]):
                new_solutions.append(solution)

            # for merge_node in [x for x in solution if x[3] in self.merge_objects.keys()]:
            #     end_node = end_action(merge_node)[:3]
            #     indx = solution.index(merge_node)
            #
            #     """if this action has an end"""
            #     if end_node in [x[:3] for x in solution[indx:]]:
            #         new_solutions.append(solution)
            #     else:
            #         possible_actions = []
            #         for node in self.merge_objects[merge_node[3]]:
            #             possible_action = tuple(self.plans[node[0]].nodes[node[1]].action[:3])
            #             if possible_action == merge_node[:3]:
            #                 pass
            #             else:
            #                 possible_end_node = end_action(possible_action)
            #                 if possible_end_node in [x[:3] for x in solution[indx:]]:
            #                     possible_actions.append(possible_end_node)
            #
            #         if possible_actions:
            #             if len(possible_actions) == 1:
            #                 end_snap_action = [x for x in solution[indx:] if x[:3] == possible_actions[0]][0]
            #                 end_indx = solution.index(end_snap_action)
            #                 solution[end_indx] = tuple(end_node + (end_snap_action[3],))
            #                 new_solutions.append(solution)
            #             else:
            #                 """if there are multiple possible snap actions that can end this start action"""
            #                 # for pa in possible_actions:
            #                 raise NotImplementedError
            #         else:
            #             'Solution dropped - No end action found for merged start action'
            #             pass
        return new_solutions

    def get_initial_actions(self, p_type):
        initial_actions = defaultdict(list)
        for m in self.graph['I']:
            if m[0] == 'M':
                actions = {}
                for n in self.merge_objects[m]:
                    action = self.plans[n[0]].nodes[0].action
                    if p_type == 'Temporal':
                        action = action[:3]
                    if action not in actions:
                        actions[action] = [n]
                    else:
                        actions[action].append(n)
                initial_actions[m] = actions

            else:
                action = self.plans[m[0]].nodes[0].action
                if p_type == 'Temporal':
                    initial_actions[m] = action[:3]
                else:
                    initial_actions[m] = action

        return initial_actions

    def get_actions_from_merge(self, p_type):
        """get all actions from merge objects"""
        merge_actions_dict = {}
        for m in self.merge_objects:
            actions_from_merge = {}
            for node in self.merge_objects[m]:
                if p_type == 'Temporal':
                    actionFrom = self.plans[node[0]].nodes[node[1]].action[:3]
                else:
                    actionFrom = self.plans[node[0]].nodes[node[1]].action
                # if actionFrom not in actions_from_merge.values():
                actions_from_merge[node] = actionFrom
            merge_actions_dict[m] = actions_from_merge
        self.merge_actions = merge_actions_dict

    def get_solution_actions(self, p_type, init_actions):
        solution_actions = []
        for node_seq in self.all_node_paths:

            """initial action"""
            action_seq = self.get_first_action(node_seq, init_actions, p_type)

            """other actions"""
            for i in range(1, len(node_seq) - 1):

                # if merge node
                if node_seq[i] in self.merge_objects:

                    # if merge after merge - need to create more solutions
                    if node_seq[i + 1] in self.merge_objects or node_seq[i + 1] == 'T':
                        new_action_seq = []
                        for action in set([tuple(x) for x in self.merge_actions[node_seq[i]].values()]):
                            for seq in action_seq:
                                new_seq = copy.copy(seq)
                                new_seq.append((tuple(action) + (node_seq[i],)))
                                new_action_seq.append(new_seq)
                        action_seq = new_action_seq

                    else:
                        pln, n = node_seq[i + 1]
                        action = self.merge_actions[node_seq[i]][(pln, n - 1)]
                        for p in action_seq:
                            p.append((tuple(action) + (node_seq[i],)))

                else:
                    # if not a merge node
                    if p_type == "Temporal":
                        action = self.plans[node_seq[i][0]].nodes[node_seq[i][1]].action[:3]
                    else:
                        action = self.plans[node_seq[i][0]].nodes[node_seq[i][1]].action
                    for p in action_seq:
                        p.append((tuple(action) + (node_seq[i],)))

            solution_actions += action_seq

        return solution_actions

    def get_first_action(self, node_seq, init_actions, p_type):
        action_seq = []
        if node_seq[1] in self.merge_objects:
            actions = list(init_actions[node_seq[1]].keys())
            if len(actions) == 1:
                action_seq.append([(tuple(actions[0]) + (node_seq[0],))])
            else:
                """if more than 1 action in merge"""
                for a in actions:
                    action_seq.append([(tuple(a) + (node_seq[0],))])
        else:
            if p_type == "Temporal":
                action = self.plans[node_seq[1][0]].nodes[0].action[:3]
            else:
                action = self.plans[node_seq[1][0]].nodes[0].action
            action_seq.append([tuple(action) + (node_seq[0],)])

        return action_seq

    def get_valid_plans(self, p_type):
        """get all valid plans in the TPN"""
        self.valid_solutions = []
        valid = {}
        if p_type == "Temporal":
            schedules = []
            schedule_action_seq = []
            """add the original solutions"""
            for p in self.plans:
                schedules.append(tuple([tuple(x.action[:4]) for x in p.nodes]))
                schedule_action_seq.append(tuple([tuple(x.action[:3]) for x in p.nodes][:-1]))

            for i in range(len(self.solution_actions)):
                # check if this solution already exists
                if tuple([x[:3] for x in self.solution_actions[i]]) in schedule_action_seq:
                    continue

                """validate solution"""
                plan = self.solution_actions[i]
                plan_actions = [x[:3] for x in plan]
                validate_info = plan_actions, self.domain_actions, self.goals, self.initial_state

                """LP schedule"""
                try:
                    result = LP(plan_actions, self.domain_actions)
                    schedule = list(map(lambda x: round(x, 2), result.x.tolist()))
                    """check that the schedule is ordered and that no actions take place at the same time"""
                    if schedule == sorted(schedule) and len(set(schedule)) == len(schedule):
                        if run_temporal_plan(validate_info + tuple([schedule]), 'validate'):
                            valid[i] = plan
                            schedules.append([tuple(list(plan[j]) + [schedule[j]]) for j in range(len(plan))])
                except Exception as e:
                    pass

            self.scheduels = schedules

        else:  # classical
            for i in range(len(self.solution_actions)):
                plan = [x[:-1] for x in self.solution_actions[i]]
                if plan not in self.valid_solutions:
                    validate_info = self.solution_actions[i], self.domain_actions, self.goals, self.initial_state
                    if run_classical_plan(validate_info, 'validate'):
                        valid[i] = self.solution_actions[i]
                        self.valid_solutions.append(plan)

        self.valid_plans = valid

    def get_decision_nodes(self):
        """get all nodes where a decision is made"""

        """iterate over all node sequences"""
        seen = defaultdict(list)
        for seq in self.all_node_paths:
            for i in range(len(seq) - 1):
                if seq[i] not in seen.keys():
                    """if a new node is seen, add it"""
                    seen[seq[i]].append(seq[i + 1])
                else:
                    """if this node has already been seen, check if it has the same following node"""
                    if seq[i + 1] not in seen[seq[i]]:
                        seen[seq[i]].append(seq[i + 1])
        d_nodes = [x for x in seen if len(seen[x]) > 1]

        self.decision_nodes = {}
        for n in d_nodes:
            self.decision_nodes[n] = seen[n]

    def get_quality_measures(self, p_type, naive):
        """quality measures of the tpn"""

        if not naive:
            # 1) Compactness
            compactness = 1 - float(len(self.graph) + 1) / (
                    sum([len(x.nodes) for x in self.plans]) - (len(self.plans) - 1) * 2)

            # 2) number of valid pans
            # if p_type == 'Temporal':
            #     n_valid_plans = len(self.scheduels)
            # else:
            #     n_valid_plans = len(self.valid_plans)
        else:
            compactness = 0
            n_valid_plans = len(self.plans)

        self.quality_measures = {"compactness": round(compactness, 3)} #, "n_valid_plans": n_valid_plans}


def get_params_of_merges(merge_sequence, naive):
    merged_nodes = {}
    merge_objects = {}
    if not naive:
        count = 0
        for step in merge_sequence:
            if 'new' in step[0]:
                merge_name = 'M' + str(count)
                node1 = step[1]
                node2 = step[2]
                merged_nodes[node1] = merge_name
                merged_nodes[node2] = merge_name
                merge_objects[merge_name] = [node1, node2]
                count = count + 1

            elif 'add' in step[0]:
                node = step[2]
                merge_name = 'M' + str(step[1])
                merged_nodes[node] = merge_name
                merge_objects[merge_name].append(node)


    return merged_nodes, merge_objects


def build_tpn(params, naive=None):
    """build a TPN object"""
    plans, merge_sequence, planning_problem_type = params[0], params[1], params[2]

    """get the merge information"""
    merged_nodes, merge_objects = get_params_of_merges(merge_sequence, naive)
    """create tpn"""
    tpn = TPN(plans, merge_sequence, merged_nodes, merge_objects, planning_problem_type)
    """add edges between nodes in the tpn"""
    tpn.get_edges_and_nodes()
    """get all valid node sequences"""
    tpn.getAllPaths('I', 'T')

    tpn.naive = True

    if not naive:
        tpn.naive = False
        """get all valid action sequences"""
        tpn.tpn_solution_actions(planning_problem_type)
        """validity test"""
        tpn.get_valid_plans(planning_problem_type)
        """labels"""
        tpn.get_decision_nodes()
        """visualize"""
        # visualize(tpn)

    """Goodness Measures"""
    tpn.get_quality_measures(planning_problem_type, naive)

    return tpn
