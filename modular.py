from get_plans import *
from pythonpddl.pythonpddl import pddl
from facts_actions import *
from divesrity_score import *
from swappable import *
from create_plans import *


def parsing(domain_path, problem_path):
    """Parsing original domain and problem"""
    parsed = pddl.parseDomainAndProblem(domain_path, problem_path)

    """get actions, initial state and goal state from pddl problem and domain"""
    return collect_facts_actions(parsed[0], parsed[1])


def load_diverse_plans(p_type, k):
    """load all plans"""
    if p_type == 'Temporal':
        all_plans = load_temporal_plans()
    else:
        all_plans = load_classical_plans()

    if not all_plans:
        return None, None, None, 'No plans Found'

    print('DIVERSE PLANS FOUND: %d' % len(all_plans))
    if k > len(all_plans):
        k = len(all_plans)
    print('GENERATING FOR K=%d PLANS' % k)

    if OPTIMIZATIONS['PLANSET_DIV'] == 'Max':
        print('OBTAINING MAX DIVERSITY PLANSET')
        plan_numbers, PlanSet_Diversity, MaxDiveristyBefore = get_plan_set(all_plans, k)
    else:  # K-First
        print('OBTAINING K-FIRST DIVERSITY PLANSET')
        plan_numbers = sorted(list(all_plans.keys())[:k])
        k_first_plans = dict((k, all_plans[k]) for k in plan_numbers)
        _, PlanSet_Diversity, MaxDiveristyBefore = get_plan_set(k_first_plans, k)

    # """load these plans"""
    if p_type == 'Temporal':
        k_plans = dict((k, all_plans[k]) for k in range(len(plan_numbers)))
    else:
        k_plans = load_plans(all_plans, plan_numbers)

    return k_plans, PlanSet_Diversity, MaxDiveristyBefore, 'plans found'


def get_full_plans(A, I, G, p, p_type):
    plans = []
    for i in range(len(p)):
        if p_type == 'Temporal':
            plan_structure = FullTemporalPlan(A, I, G, p[i], i)
        else:
            plan_structure = FullClassicalPlan(A, I, G, p[i], i)
        plan_structure.construct_plan()
        plans.append(plan_structure)
    return plans


def get_compatible_nodes(plans):
    print('OBTAINING SWAPPABLE NODE PAIRS')
    logging.info('OBTAINING SWAPPABLE NODE PAIRS')
    compatibility_dict = swappable(plans)
    node_dict = {}
    for config in ['Full', 'Semi']:
        node_dict[config] = set([tuple(x[0]) for x in compatibility_dict[config]]).union(
            set([tuple(x[1]) for x in compatibility_dict[config]]))
        print(f'{str(len(compatibility_dict[config]))} {str(config)} compatible merges found')
        logging.info(f'{str(len(compatibility_dict[config]))} {str(config)} compatible merges found')

    if len(compatibility_dict.keys()) < 2:
        print('0 Semi compatible merges found')
        logging.info('0 Semi compatible merges found')
    return compatibility_dict, node_dict


def optimizations(prob_type, mergeable, plans):
    enabled = True
    plan_space_done = False
    remaining_nodes = []
    remaining_merges = []
    compilation_output = []
    planSpace_actions = []

    if OPTIMIZATIONS['STATE_SPACE']:
        """merge nodes with the same state space"""
        enabled = False
        compilation_output = state_space_opt(plans, mergeable)
        if compilation_output:
            return compilation_output, enabled, [], []
        else:
            enabled = True

    if OPTIMIZATIONS['PLAN_SPACE'] and enabled:
        """merge nodes that initiate the same actions from the initial node or from the terminal node"""
        if prob_type == 'Temporal':
            remaining_merges, remaining_nodes, planSpace_actions = temporal_planSpace_merge(mergeable, plans)
        else:
            remaining_merges, remaining_nodes, planSpace_actions = classical_planSpace_merge(mergeable, plans)
        plan_space_done = True
        if not remaining_merges:  # all merges were made
            compilation_output = planSpace_actions
            enabled = False
            print('PLAN SPACE COMPILATION - COMPLETE')
            print(40 * '-')

    return compilation_output, enabled, [remaining_merges, remaining_nodes, plan_space_done], planSpace_actions


def combine_planspace_actions(compilation_output, planSpace_actions):
    if OPTIMIZATIONS['COMPILATION'] == 'Python':
        merge_num = sum([1 for x in compilation_output if x[0] == 'new'])

    else:
        # pairs appear only with the 'Mid' compilation
        pairs = [x for x in compilation_output if 'pair' in x.lower()]
        compilation_output = [x for x in compilation_output if x not in pairs]
        merges = [x for x in compilation_output if ' merge' in x.lower()]
        lonely = [x for x in compilation_output if 'unmerged_node' in x.lower()]

        assert merges or planSpace_actions or pairs, 'Failed to find a non trivial plan'

        """get list of merged nodes"""
        node2merge = defaultdict(list)
        for line in merges:
            words = line.lower().split()
            if 'create_merge' in words:
                merge_num = int(words[2][5:])
            else:
                merge_num = int(words[3][5:])
            node_num = tuple(int_id(words[1][4:]))
            node2merge[merge_num].append(node_num)

        """deal with pairs(Mid compilation)"""
        # looks like: add_pair_to_merge node11 node12 node21 node22 merge0
        for line in pairs:
            words = line.lower().split()
            merge_num = int(words[5][5:])
            node1_num = tuple(int_id(words[3][4:]))
            node2_num = tuple(int_id(words[4][4:]))
            node2merge[merge_num].append(node1_num)
            node2merge[merge_num].append(node2_num)

        node2merge = dict(enumerate(node2merge.values()))


        compilation_output = []
        for merge in node2merge:
            compilation_output.append(('new', node2merge[merge][0], node2merge[merge][1]))
            for i in range(2, len(node2merge[merge])):
                compilation_output.append(('add', merge, node2merge[merge][i]))
        if lonely:
            compilation_output.append(('lonely', len(lonely)))
        merge_num = len(node2merge)

    new_ps_actions = []
    for a in planSpace_actions:
        if a[0] == 'add':
            temp_a = list(a)
            temp_a[1] += merge_num
            a = tuple(temp_a)
        new_ps_actions.append(a)

    return compilation_output + new_ps_actions


def state_space_opt(p, possible_merges):
    """state space optimization"""
    stateSpace_merges, stateSpace_actions = stateSpace_merge(p, possible_merges)
    merge_diff = set(possible_merges).symmetric_difference(set(stateSpace_merges))

    if not merge_diff:
        print('STATE SPACE COMPILATION - COMPLETE')
        print(40 * '-')
        return stateSpace_actions
    else:
        return False


def compile_python(plan_space_done, remaining_nodes, remaining_merges, planSpace_actions, swappable_merges):
    print('PYTHON COMPILING...')
    if plan_space_done:
        print('WITH PLAN SPACE OPTIMIZATION')
        compilation_output, compilation_time = get_merges(remaining_nodes, remaining_merges)
        compilation_output = combine_planspace_actions(compilation_output, planSpace_actions)
    else:
        compilation_output, compilation_time = get_merges(remaining_nodes, swappable_merges)
    print('...DONE!')
    print('COMPILATION TIME: %.02f' % compilation_time)
    print(40 * '-')

    return compilation_output


def compilation_search(compilation, remaining, planSpace_actions, swappable_merges, domain_path, d_name, p_name, mergeable_nodes):
    remaining_merges, remaining_nodes, plan_space_done = remaining

    if compilation == 'Python':
        return [], compile_python(plan_space_done, remaining_nodes, remaining_merges, planSpace_actions, swappable_merges)

    else:
        if plan_space_done:
            print('WITH PLAN SPACE OPTIMIZATION')
            n_merges = int(len(remaining_nodes) / 2)
            d_nodes = get_domain_literals(remaining_nodes)
            p_obj, p_init = get_problem_literals(domain_path, remaining_nodes, n_merges, remaining_merges)

        else:
            n_merges = int(len(mergeable_nodes) / 2)  # worst case
            d_nodes = get_domain_literals(mergeable_nodes)
            p_obj, p_init = get_problem_literals(domain_path, mergeable_nodes, n_merges, swappable_merges)

        compilation_output_path = DIRECTORIES["COMPILATION_PDDL"]
        cleanup(compilation_output_path)
        path_new_domain = create_domain(d_name)
        new_p_name = d_name + "_" + p_name + ".pddl"
        path_new_problem = create_new_problem(p_obj, p_init, new_p_name, d_nodes)
        print('DOMAIN AND PROBLEM FILES GENERATED')
        print(OPTIMIZATIONS['COMPILATION'] + ' COMPILING...')

        return [path_new_domain, path_new_problem], []
