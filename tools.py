import os
import time
from shutil import copyfile
import subprocess
from subprocess import Popen
from time import sleep
import ForbidIterative.plan as fi
try:
    import cPickle as pickle
except:
    import pickle

Classical_planning_timeout = 30*60

DIRECTORIES = {
    "HOME_DIR": os.getcwd(),
    "BENCHMARK_DIR": os.getcwd() + '/benchmarks',
    "OUTPUT_DIR": os.getcwd() + '/output',
    # "PLANS_DIR": os.getcwd() + '/output/planner_output',
    "COMPILATION_PDDL": os.getcwd() + "/output/compilation_pddl",
    "TPN_DIR": os.getcwd() + '/generated_tpns',
    "FAST_DOWNWARD": os.path.expanduser('~/FD'),
    "TEMPORAL_DUMPS":  '',
    "PLAN_OUTPUT_DIR": '',
    "MINIZINC_DIR": os.path.expanduser('~/Minizinc')
}

PARAMETERS = {
    'VISUALIZATION': False,
    'GENERATE_DIVERSE_PLANS': True,
    'PROBLEM_PARAMS': [],
    'PRINT': False,
    'RUN_LAMA': True,
    'LAMA_TIME_LIMIT': "1m",
    'GET_PDDL': False,
    'LAMA_MEMORY_LIMIT': '8G',
}

OPTIMIZATIONS = {
    'SHORT-PLANS': False,       # in landmark diversity: which plan to take from zero_div groups
    'COMPILATION': 'LAMA',    # Python or PDDL compilation
    'PLANSET_DIV': 'Max',       # Max or K-First planset diversity
    'DIVERSITY': 'action',      # what diversity metric to use
    'STATE_SPACE': False,        # Acknowledge state space merges
    'PLAN_SPACE': False,         # Acknowledge plan space merges
    'HEURISTICS': {
        'C2': [10,1,100,1],
        'C1': [1,10,100,10],    # ACTIONS: create-merge/add-to-merge/lonely/add-pair-to-merge
        'C3': [1,1,10,1],
        'C0': [1,1,1,1],        # always out-performed
        'Compact': [1,0,1000,0]
    },
    'PDDL_COMPILATIONS': ['Strict', 'Mid', 'Loose', 'SuperLoose']
}

TEST_PARAMS = {
    'DOMAIN': 'depot',
    'PROBLEM': 'pfile10',
    'NUM_SOL': 5,
    'K_PLANS': 5,
    'LANDMARKS': [],
    'HEURISTIC':  [10, 1, 100, 0],
    'COST_FUNCTION': 'Compact',
    'COMPILATION': 'LAMA',    # Python or PDDL compilation
    'DIVERSITY': 'action',
    'PROBLEM_TYPE': 'Classical', # 'Temporal'
    'COMPILATION_RULE': 'Strict',
    'GROUNDED': False,
    'SEMI_GROUNDED': False,
}

class argsclass(object):
    def __init__(self, args):
        self.planner = args[0]
        self.domain = args[1]
        self.problem = args[2]
        self.clean_local_folder = args[3]
        self.conditional_effects = args[4]
        self.keep_intermediate_tasks = args[5]
        self.number_of_plans = args[6]
        self.overall_time_limit = args[7]
        self.plans_as_json = args[8]
        self.quality_bound = args[9]
        self.reordering = args[10]
        self.results_file = args[11]
        self.symmetries = args[12]
        self.use_local_folder = args[13]
        self.suppress_planners_output =args[14]
        self.upper_bound_on_number_of_plans = args[15]
        # self.overall_memory_limit = args[16]
        self.start_time = time.time()
        self.output_dir = DIRECTORIES["PLAN_OUTPUT_DIR"]

def get_simple_time_limit(overall_limit, start_time):
    return max(0, overall_limit - (time.time() - start_time))


def cleanup(path):
    """clear content of output folder"""
    for item in os.listdir(path):
        if item == '__init__.py' or item == 'ff' or item == 'siw':
            continue
        item_path = os.path.join(path, item)
        try:
            if os.path.isfile(item_path):
                os.unlink(item_path)
        except Exception as e:
            print(e)
    return


def copy_file(src, dst):
    """copy src(the file name in the current directory) to the destination """
    copyfile(src, dst)
    return


def call_diverse_planner(domain_path, problem_path, num_sol):
    fi.main('topk', domain_path, problem_path, num_sol, DIRECTORIES["PLAN_OUTPUT_DIR"], Classical_planning_timeout)
    return


def popen_timeout(command, stdin, timeout=600):  # default timeout 10 min
    with open(stdin, 'r') as f:
        p = Popen(command, stdin=f) #, stdout=PIPE, stderr=PIPE)
        for t in range(timeout):
            sleep(1)
            if p.poll() is not None:
                return p.communicate()
        p.kill()
    return 'Timeout'


def preprocess():
    preprocess_path = DIRECTORIES["HOME_DIR"] + "/dlama/src/preprocess/preprocess"
    cmd = [preprocess_path]
    # with open('output.sas', 'r') as f:
    #     proc = subprocess.Popen([preprocess_path], stdin=f)
    #     proc.wait()
    output = popen_timeout(cmd, 'output.sas')
    print('PREPROCESSING COMPLETE')
    return


def planning(n):
    diverse_planning_path = DIRECTORIES["HOME_DIR"] + "/dlama/src/search/downward"
    cmd = [diverse_planning_path, 'ipc', 'dlama', '1', str(n)]
    seconds = 900
    # with open('output', 'r') as f:
    #     proc = subprocess.Popen([diverse_planning_path, 'ipc', 'dlama', '1', str(n)], stdin=f)  #, stdout=PIPE)
    #     proc.wait()
    #     output = proc.communicate()[0]
    output = popen_timeout(cmd, 'output', seconds)
    assert output != 'Timeout', 'Diverse plan generation timeout (30m)'
    print('SOLVING COMPLETE - files created in output directory')
    return


def same_actions_between_plans(plans):
    seen = set()
    repeated = set()
    for p in plans:
        for i in set(p.plan_actions):
            if i in seen:
                repeated.add(i)
            else:
                seen.add(i)
    return len(repeated) +1, [x[0] for x in repeated]


def validate(loc, domain, problem, plan, bulk=False):
    val_path = DIRECTORIES["HOME_DIR"] + "/VAL/validate"
    os.chdir(loc)
    params = [val_path, '-S', domain, problem, plan]
    proc = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()
    stdout, stderr = proc.communicate()

    if bulk:
        try:
            int(stdout.split()[0])
            return True
        except:
            return False

    else:
        assert (int(stdout.split()[0])), 'Validation Failed'
        return True


def str_id(p, n):
    return str(p) + '_' + str(n)


def int_id(string):
    return [int(x) for x in (string.split("_"))]


def save_object(obj, filename, loc):
    """save object to pickle with file name"""
    with open(loc + '/' + filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, -1)


def load_object(filename, loc):
    """load pickle object by file name"""
    with open(loc + '/' + filename, 'rb') as input:  # Overwrites any existing file.
        obj = pickle.load(input)
    return obj
