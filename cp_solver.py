import logging
import pymzn
import numpy
import os
import uuid

pymzn.config.__setattr__('minizinc', os.path.join(os.getcwd(), 'CP/MiniZinc/bin/minizinc'))
# pymzn.debug()

Gurobi = pymzn.Gurobi(solver_id='gurobi', dll='/opt/gurobi702/linux64/lib/libgurobi70.so')
# Gecode = pymzn.Gecode(solver_id='gecode')


def get_strict_merges(mat, num2tp_dict):
    i = 0
    found_merges = []
    row = mat[i]
    row_list = list(range(len(mat)))
    while row:
        merge_indexes = [x for x in range(len(row)) if row[x]]
        [row_list.remove(x) for x in merge_indexes]
        if len(merge_indexes) > 1:
            merge_nodes = [num2tp_dict[x] for x in merge_indexes]
            found_merges.append(merge_nodes)
        if not row_list:
            break
        i = row_list[0]
        row = mat[i]
    return found_merges


def get_loose_merges(mat, num2tp_dict):
    found_merges = []
    min_merge = {}
    for i in range(len(mat)):
        merge_indexes = [x for x in range(len(mat[i])) if mat[i][x]]
        min_indx = min(merge_indexes)
        for count, indx in enumerate(merge_indexes):
            if indx in min_merge.keys():
                if min_merge[indx] == min_indx:
                    continue
                else:
                    min_indx = min_merge[indx]
                    for i in range(count):
                        min_merge[merge_indexes[i]] = min_indx
            else:
                min_merge[indx] = min_indx
    for merge_num in set(min_merge.values()):
        found_merges.append([num2tp_dict[x] for x in min_merge if min_merge[x] == merge_num])

    return found_merges


def cp_problem(compatible_dict, timepoints, method, regime, time_limit, solver):
    logging.info(f'OPTIMIZATION SOLVER: {solver}')
    if method == 'Full':
        compatible_pairs = compatible_dict['Full']
        relevant_timepoints = timepoints['Full']
    else:
        compatible_pairs = compatible_dict['Full'] + compatible_dict['Semi']
        relevant_timepoints = timepoints['Full'].union(timepoints['Semi'])

    if not compatible_pairs:
        return False, 'No compatible pairs found'

    numbers_timepoints_dict = dict(enumerate(sorted(relevant_timepoints)))
    timepoints_numbers_dict = {y: x for x, y in numbers_timepoints_dict.items()}

    compatible_matrix = numpy.full((len(relevant_timepoints), len(relevant_timepoints)), False)
    # NOTE: in the compatibility table a cord must be compatible with itself (i.e the main diagonal must be True)
    numpy.fill_diagonal(compatible_matrix, True)
    for tp1, tp2 in compatible_pairs:
        n1, n2 = timepoints_numbers_dict[tp1], timepoints_numbers_dict[tp2]
        compatible_matrix[n1][n2], compatible_matrix[n2][n1] = True, True
    compatible_matrix = compatible_matrix.tolist()

    """turn information to dzn file"""
    cp_file_path = os.path.join(os.path.dirname(__file__), 'CP')
    dzn_name = os.path.join(cp_file_path, regime +'_' + str(uuid.uuid4()) + '.dzn')
    mzn_name = os.path.join(cp_file_path, regime + '.mzn')
    info_dict = {'compatible': compatible_matrix, 'num_timepoints': len(relevant_timepoints)}
    if regime == 'Loose':
        node_plans_vector = []
        for i, val in numbers_timepoints_dict.items():
            node_plans_vector.append(val[0])
        info_dict['node_plans'] = node_plans_vector
    pymzn.dict2dzn(info_dict, fout=dzn_name)

    """solve"""
    # TODO pymzn.minizinc gets stuck in minizinc.py line 179 when searching model for output statements. commented it out.
    if solver == 'Gurobi':
        solution = pymzn.minizinc(mzn_name, dzn_name, timeout=time_limit, output_mode='dict', solver=Gurobi)
    else:
        solution = pymzn.minizinc(mzn_name, dzn_name, timeout=time_limit, output_mode='dict')

    if not solution:
        return False, 'No solution found in time limit'

    """obtain merges from solution"""
    merge_matrix = solution[0]['merge']
    found_merges = get_strict_merges(merge_matrix, numbers_timepoints_dict) if regime == 'Strict' \
        else get_loose_merges(merge_matrix, numbers_timepoints_dict)

    os.unlink(dzn_name)
    return found_merges, 'Solution found'


if __name__ == '__main__':
    # test env
    compatible_dict = {
        'Full': [
            # ((0, 1), (1, 1)), ((0, 1), (3, 1)), ((3, 1), (1, 1)),
            # ((4, 4), (5, 5)),
            # ((3, 1), (6, 1)),
            # ((6, 2), (4, 1)),
            # ((0, 2), (2, 2)),
            ((5, 1), (2, 1)), ((1, 1), (2, 1)), ((1, 1), (5, 1)),
            ((6, 1), (7, 1)), ((6, 1), (8, 1)), ((8, 1), (7, 2)), ((6, 1), (8, 2)),
            ((0, 1), (1, 1)), ((1, 1), (2, 1)), ((2, 1), (3, 1)), ((2, 1), (3, 2)),
        ]}
    timepoints = {x for x, y in compatible_dict['Full']}.union({y for x, y in compatible_dict['Full']})
    timepoints_dict = {'Full': timepoints}
    method = 'Full'
    regime = 'Loose'
    merges = cp_problem(compatible_dict, timepoints_dict, method, regime, 300, None)
    print(merges)
