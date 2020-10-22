import argparse
import logging
from tools import *
from main import get_best_tpn
import datetime


def run(args):
    """collect parameters"""
    try:  # for split domains
        test = int(args.d.split('/')[-2])
        args.d_name = args.d.split('/')[-3]
    except:
        args.d_name = args.d.split('/')[-2]
    args.p_name = args.p.split('/')[-1].split('.')[0]
    args.d = os.path.join(os.getcwd(), 'benchmarks', args.d)
    args.p = os.path.join(os.getcwd(), 'benchmarks', args.p)
    args.n = int(args.n)
    params = [args.p_type, args.d, args.p, args.d_name, args.p_name, args.n, args.n, 'Python', 'C0', 'K-First',
              [None, None], args.planner, args.verbose, args.timeout, ['Full', 'Semi'], ['Strict', 'Loose'],
              args.ground, 'Gecode']
    method_list = []

    """OUTPUT DIR"""
    DIRECTORIES["PLAN_OUTPUT_DIR"] = os.path.join(os.getcwd(), 'output/planner_output', args.p_type, args.d_name,
                                                  args.p_name, str(args.n))
    if not os.path.exists(DIRECTORIES["PLAN_OUTPUT_DIR"]):
        os.makedirs(DIRECTORIES["PLAN_OUTPUT_DIR"])

    """RUN"""
    name = '_'.join([args.p_type, str(args.n), args.d_name, args.p_name])
    log_name = 'logs/' + '_'.join([name, datetime.datetime.now().strftime("%d-%m %H:%M").replace(' ', '_')])
    logging.basicConfig(filename=log_name + '.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    tpns, msg, naive_tpn = get_best_tpn(params)
    if tpns:
        for regime_method in tpns:
            tpn_name = '_'.join([name, regime_method])
            if tpns[regime_method]:
                tpns[regime_method].name = name
                save_object(tpns[regime_method], tpn_name, DIRECTORIES['TPN_DIR'])
                method_list.append([tpn_name, 'TPN generated'])
            else:
                save_object(naive_tpn, tpn_name, DIRECTORIES['TPN_DIR'])
                method_list.append([tpn_name, 'Time limit reached'])
    else:
        name = '_'.join([name, msg.upper()])
        save_object(naive_tpn, name, DIRECTORIES['TPN_DIR'])
        method_list.append([name, msg])

    return method_list


def get_prob_name(problem):
    if problem[-5:] == '.pddl':
        return problem[:-5]  # remove pddl extension
    else:
        return problem


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automatically generate a TPN for input temporal planning problem.')
    parser.add_argument("-p_type", help="PDDL problem type", default='Temporal')
    parser.add_argument("-d", help="PDDL domain file path from benchmarks folder", default=None)
    parser.add_argument('-p', type=str, help='problem file path from benchmarks folder')
    parser.add_argument("-n", help="number of plans", default=None)
    parser.add_argument("-ground", help="grounded domain", default=False)
    parser.add_argument('-planner', type=str, help='which planner to use', default='optic_plus')
    parser.add_argument('-verbose', type=bool, help='verbose for planner', default=False)
    parser.add_argument('-timeout', type=int, help='COP timeout (sec), default is 5 min (300 sec)', default=30 * 60)
    args = parser.parse_args()

    run(args)

    # -p_type Classical -d Classical/driverlog/domain.pddl -n 2 -p Classical/driverlog/p01.pddl
    # -p_type Temporal -d Temporal/parking/domain.pddl -n 2 -p Temporal/parking/p15-9-3.pddl
    # -p_type Temporal -d Temporal/quantum_circuit/quantum_circuit_01/domain.pddl -n 2 -p Temporal/quantum_circuit/quantum_circuit_01/problem_n4_i1_u1.0_P1_V2.pddl