from modular import *
from cp_solver import cp_problem
from build_tpn import build_tpn
import logging
import time


def fix_domain_for_temporal(path):
    os.chdir(os.path.dirname(path))
    old_domain = open("domain.pddl", 'r+')
    new_domain = open('new_domain', 'w')
    current_line = old_domain.readline()
    while current_line:
        # if '(:types' in current_line:
        #     d
        if 'durative-action' in current_line:
            if 'requirements' not in current_line:
                current_line = current_line[:19] + '_'.join(current_line[19:-1].split('-')) + '\n'
        new_domain.write(current_line)
        current_line = old_domain.readline()

    old_domain.close()
    new_domain.close()
    os.remove("domain.pddl")
    os.rename('new_domain', 'domain.pddl')
    os.chdir(DIRECTORIES["HOME_DIR"])


def get_run_params(p_type, comp, h, ps_div, opt):
    TEST_PARAMS['PROBLEM_TYPE'] = p_type
    TEST_PARAMS['HEURISTIC'] = h
    OPTIMIZATIONS['PLAN_SPACE'], OPTIMIZATIONS['STATE_SPACE'] = opt
    OPTIMIZATIONS['PLANSET_DIV'] = ps_div
    OPTIMIZATIONS['COMPILATION'] = comp
    return


def get_merge_sequence(merge_list):
    merge_seq = []
    relevant = [x for x in merge_list if len(x) > 1]
    for indx, m in enumerate(relevant):
        if len(m) == 1:
            continue
        for i in range(len(m)):
            node = m[i]
            if i == 0:
                merge_seq += [('new', m[0], m[1])]
            elif i >= 2:
                merge_seq += [('add', indx, node)]
    return merge_seq


def get_best_tpn(params):
    """main function"""
    os.chdir(DIRECTORIES["HOME_DIR"])
    prob_type, domain_path, problem_path, d_name, p_name, num_sol, n_plans_to_merge, compilation, h, ps_div, opt, \
    planner, verbose, timeout, compatibility_methods, merge_regimes, grounded, solver = params
    get_run_params(prob_type, compilation, h, ps_div, opt)
    logging.info('----------------- NEW PROBLEM -----------------')
    print('----------------- NEW PROBLEM -----------------')
    print('DOMAIN: %s, PROBLEM: %s, TYPE: %s N: %s' % (d_name, p_name, TEST_PARAMS['PROBLEM_TYPE'], str(num_sol)))
    logging.info('DOMAIN: %s, PROBLEM: %s, TYPE: %s' % (d_name, p_name, TEST_PARAMS['PROBLEM_TYPE']))
    # if prob_type == 'Temporal': fix_domain_for_temporal(domain_path)
    logging.info("STARTED PLANNING PHASE")
    planning_time = time.time()
    found_plans, msg = generate_plans(prob_type, domain_path, problem_path, num_sol, planner, verbose, grounded)
    logging.info(f'GENERATED PLANS MESSAGE: {msg}')
    overall_planning_time = time.time() - planning_time
    logging.info(f"FINISHED PLANNING PHASE, TIME: {overall_planning_time}")
    if not found_plans:
        logging.info(f'FAILURE: {msg}')
        return None, msg, None
    A, I, G = parsing(domain_path, problem_path)
    k_plans, PlanSet_Diversity, MaxDiveristyBefore, msg = load_diverse_plans(prob_type, n_plans_to_merge)
    if not k_plans:
        return None, msg, None
    P = get_full_plans(A, I, G, k_plans, prob_type)
    compatible_pairs_dict, mergeable_nodes = get_compatible_nodes(P)
    """naive tpn"""
    naive_tpn = build_tpn([P, {}, prob_type], naive=True)
    if not sum([bool(x) for x in compatible_pairs_dict.values()]):  # no possible merges found
        logging.info('FAILURE: No possible merges - returned naive TPN')
        return False, 'No possible merges - returned naive TPN', naive_tpn

    tpns = {}
    logging.info(f"OPTIMIZATION PHASE WITH TIME LIMIT: {timeout}")
    cost_analysis = []
    for regime in merge_regimes:
        for method in compatibility_methods:
            """CP"""
            logging.info(f"STARTED OPTIMIZATION WITH COMPATIBILITY: {method}, TRANSITIVITY: {regime}")
            optimization_time = time.time()
            merges, msg = cp_problem(compatible_pairs_dict, mergeable_nodes, method, regime, timeout, solver)
            logging.info(f'OPTIMIZATION MESSAGE: {msg}')
            logging.info(f"FINISHED {method} COMPATIBILITY {regime} TRANSITIVITY - TIME:{time.time() - optimization_time}")
            if merges:
                cost_analysis.append(time.time() - optimization_time)
                merge_sequence = get_merge_sequence(merges)
                result = build_tpn([P, merge_sequence, prob_type])
                result.compatibility_method = method
                result.merge_regime = regime
                tpns[regime + '_' + method] = result
                print(f'\tCompactness for {regime} Transitivity and {method} Compatibility: {result.quality_measures["compactness"] }')
                logging.info(f'\tCompactness for {regime} Transitivity and {method} Compatibility: {result.quality_measures["compactness"] }')
                if method == 'Semi' and not compatible_pairs_dict[method]:
                    print(f'\t\tSemi Compatibility - No additional compatible pairs')
                    logging.info(f'\t\tSemi Compatibility - No additional compatible pairs')
                    result.no_additional_semi_compatible_pairs = True
            else:
                print(f'\t {regime} Transitivity and {method} Compatibility: {msg}')
                logging.info(f'\t {regime} Transitivity and {method} Compatibility: {msg}')
                tpns[regime + '_' + method] = None

    print(f'PLANNING TIME: {overall_planning_time} OPTIMIZING AVERAGE: {sum(cost_analysis) / len(cost_analysis)}')
    print(f'COST ANALYSIS: {overall_planning_time/(sum(cost_analysis) / len(cost_analysis))}')
    logging.info(f'PLANNING TIME: {overall_planning_time} OPTIMIZING AVERAGE: {sum(cost_analysis) / len(cost_analysis)}')
    logging.info(f'COST ANALYSIS: {overall_planning_time / (sum(cost_analysis) / len(cost_analysis))}')
    print(40 * '-')
    logging.info(40 * '-')
    return tpns, 'TPNs Generated', naive_tpn
