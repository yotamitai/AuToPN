"""This module will load tpns and compare them"""
import os
import csv
from tools import load_object

class CostAnalysis(object):
    def __init__(self):
        self.abs_planning = {}
        self.abs_optimizing = {}
        self.p2o_ratio = {}




def cost_analysis(path, name):
    ca = CostAnalysis()
    with open(path, 'r') as f:
        for line in f.readlines():
            if 'PROBLEM:' in line:
                problem = line.split(' ')[7][:-5]
            if 'FINISHED PLANNING PHASE' in line:
                pln_time = float(line.split(':')[1])
            if 'FINISHED OPTIMIZATION PHASE' in line:
                opt_time = float(line.split(':')[1])

                """cost"""
                ca.abs_planning[problem] = pln_time
                ca.abs_optimizing[problem] = opt_time
                ca.p2o_ratio[problem] = pln_time/(pln_time + opt_time)

    print()
    return ca


if __name__ == "__main__":
    log_path = 'LOG_Classical_2_plans_driverlog_2020-08-13_14:17:46.log'
    domain_plans = 'driverlog_2'

    cost_analysis_dict = {}
    domains ={}
    files = [x for x in sorted(os.listdir('logs/'))]
    for f in files:
        domain, plans = f.split('_')[4], f.split('_')[2]
        ca_file = cost_analysis('logs/' + log_path, domain_plans)
        cost_analysis_dict['_'.join([domain,plans])] = ca_file

    print()


    # csv_columns = ['K2 FULL STRICT', 'K2 SEMI STRICT', 'K2 FULL LOOSE']
    #
    # with open(path + '/' + domain + ' coverage.csv', 'w') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    #     writer.writeheader()
    #     for data in coverage_dict:
    #         writer.writerow(data)
    #
    # with open(path + '/' + domain + ' compactness.csv', 'w') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    #     writer.writeheader()
    #     for data in compactness_dict:
    #         writer.writerow(data)

    # with open(path + '/' + domain + ' valid plans.csv', 'w') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    #     writer.writeheader()
    #     for data in valid_plans_dict:
    #         writer.writerow(data)
