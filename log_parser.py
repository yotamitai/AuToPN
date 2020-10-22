import os


class LogInfo(object):
    def __init__(self):
        self.cost_analysis = []
        self.planning_successes = 0
        self.successes = 0
        self.StF = []
        self.StS = []
        self.LF = []
        self.LS = []
        self.StF_suc = 0
        self.StS_suc = 0
        self.LF_suc = 0
        self.LS_suc = 0

    def calc_avgs(self):
        div = min(len(self.StF), len(self.StS), len(self.LF), len(self.LS))
        print(f'StF_suc: {self.StF_suc}')
        print(f'StS_suc: {self.StS_suc}')
        print(f'LF_suc: {self.LF_suc}')
        print(f'LS_suc: {self.LS_suc}')
        print(f'Optic_suc: {self.planning_successes}')
        ca = sum(self.cost_analysis) / len(self.cost_analysis)
        print(f'CA: {ca}')

        print()
        print(f'#P: {div}')
        if not div:
            StF_comp = '-'
            StS_comp = '-'
            LF_comp = '-'
            LS_comp = '-'
        else:
            StF_comp = round(sum(self.StF[:div]) / div, 2)
            StS_comp = round(sum(self.StS[:div]) / div, 2)
            LF_comp = round(sum(self.LF[:div]) / div, 2)
            LS_comp = round(sum(self.LS[:div]) / div, 2)
        print(f'StF_comp: {StF_comp}')
        print(f'StS_comp: {StS_comp}')
        print(f'LF_comp: {LF_comp}')
        print(f'LS_comp: {LS_comp}')

        print()
        print(self.StF_suc, '$|$', self.StS_suc, '&', self.LF_suc, '$|$', self.LS_suc, '&', self.planning_successes,
              '&', round(ca, 2))
        print()
        print(StF_comp, '$|$', StS_comp, '&', LF_comp, '$|$', LS_comp, '&', div)


def parse(path):
    all_logs = os.listdir(path)
    log_info = LogInfo()
    for file in all_logs:
        with open(os.path.join(path, file), 'r') as f:
            for line in f.readlines():
                if "FAILURE: No possible merges" in line: continue
                if "FAILURE: Could not find a feasible plan" in line: continue
                if 'COST ANALYSIS' in line: log_info.cost_analysis.append(float(line.split()[-1]))
                if 'GENERATED PLANS MESSAGE: Plans found' in line: log_info.planning_successes += 1
                if 'OPTIMIZATION PHASE WITH TIME LIMIT' in line: log_info.successes += 1

                if 'Strict Transitivity and Full Compatibility' in line:
                    if "No compatible pairs found" in line or "No solution found in time limit" in line:
                        pass
                    else:
                        log_info.StF.append(float(line.split()[-1]))
                        log_info.StF_suc += 1
                if 'Strict Transitivity and Semi Compatibility' in line:
                    if "No compatible pairs found" in line or "No solution found in time limit" in line:
                        pass
                    else:
                        log_info.StS.append(float(line.split()[-1]))
                        log_info.StS_suc += 1
                if 'Loose Transitivity and Full Compatibility' in line:
                    if "No compatible pairs found" in line or "No solution found in time limit" in line:
                        pass
                    else:
                        log_info.LF.append(float(line.split()[-1]))
                        log_info.LF_suc += 1
                if 'Loose Transitivity and Semi Compatibility' in line:
                    if "No compatible pairs found" in line or "No solution found in time limit" in line:
                        pass
                    else:
                        log_info.LS.append(float(line.split()[-1]))
                        log_info.LS_suc += 1

    log_info.calc_avgs()


if __name__ == '__main__':
    p_type = [
        # 'Classical'
        'Temporal'
    ]

    domain = [

        # ----------CLASSICAL-----------
        # 'driverlog'
        # 'elevators'
        # 'gripper'
        # 'miconic'
        # 'movie'
        # 'nomystery'
        # 'scanalyzer'
        # 'tpp'
        # 'transport'
        # 'zenotravel'
        # 'pegsol'
        # 'storage'
        # 'mystery'
        # 'barman'
        # 'depot'
        # 'floortile'
        # 'sokoban'
        # 'visitall'
        # ----------Temporal-----------
        # 'crewplanning'
        # 'parking'
        # 'quantum_circuit'
        # 'trucks'
        'turn_and_open'
    ]
    n = [
        # '2'
        '4'
        # '8'
    ]

    loc = os.path.join(os.getcwd(), 'logs', p_type[0], n[0], domain[0])
    parse(loc)
