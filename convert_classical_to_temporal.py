from build_tpn import *
"""
recieve txt file with durations of actions and conditions

currently only possible to generate sequential durative plans

Durations file must be .txt file of the following format:
action_name1 duration1
action_name2 duration2
....  

"""

def make_temporal(t):

    """turn solutions to schedules"""
    schedules = []
    for i in t.valid_plans:
        plan = t.solution_actions[i]
        schedule = []
        current_time = float(0)
        for action in plan:
            a_name = action[0]
            params = tuple(action[1:])
            schedule.append(('START', a_name, params, current_time))
            current_time = round(current_time + t.domain_actions[a_name].duration,6)
            schedule.append(('END', a_name, params, current_time))
            current_time = round(current_time + epsilon, 6)
        schedules.append(tuple(schedule))

    return schedules


def load_duration_file(args):
    with open(args.tpn, 'rb') as input:  # Overwrites any existing file.
        tpn = pickle.load(input)

    dur_file = open(args.dur_file, 'r+')
    current_line = dur_file.readline()
    while current_line:
        current_line = current_line.replace('\n','')
        action, duration = current_line.split(' ')
        tpn.domain_actions[action.lower()].duration = float(duration)
        current_line = dur_file.readline()

    """get all valid action sequences"""
    tpn.tpn_solution_actions('Classical')
    """validity test"""
    tpn.get_valid_plans('Classical')
    """labels"""
    tpn.get_decision_nodes()
    """Goodness Measures"""
    tpn.get_quality_measures('Classical', False)

    """turn to temporal"""
    tpn.schedules = make_temporal(tpn)

    """save as temporal"""
    tpn.name = tpn.name.replace('Classical','Temporal')
    save_object(tpn, tpn.name, os.path.dirname(args.tpn))




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-tpn', type=str, default='generated_tpns/Classical_2_driverlog_p01_Strict_Full',
                        help='name of tpn object created by process, in ./generated_tpns')
    parser.add_argument('-dur_file', type=str, default='driverlog_dur.txt', help='path to durations file')

    args = parser.parse_args()

    load_duration_file(args)



