"""This module will load tpns and compare them"""
import os
import csv
from tools import load_object


def get_dict(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12):
    dict_data = [
        {'K2 FULL STRICT': p1, 'K2 SEMI STRICT': p2, 'K2 FULL LOOSE': p3, 'K2 SEMI LOOSE': p4,
         'K4 FULL STRICT': p5, 'K4 SEMI STRICT': p6, 'K4 FULL LOOSE': p7, 'K4 SEMI LOOSE': p8,
         'K8 FULL STRICT': p9, 'K8 SEMI STRICT': p10,'K8 FULL LOOSE': p11, 'K8 SEMI LOOSE': p12,
         }
    ]
    return dict_data


def compare(path, domain):
    tpns = [load_object(x, path) for x in sorted(os.listdir(path)) if '.csv' not in x]

    k2 = [x for x in tpns if not x.naive and len(x.plans) == 2]
    k4 = [x for x in tpns if not x.naive and len(x.plans) == 4]
    k8 = [x for x in tpns if not x.naive and len(x.plans) == 8]

    k2_FULL = [x for x in k2 if x.compatibility_method == 'Full']
    k2_SEMI = [x for x in k2 if x.compatibility_method == 'Semi']

    k4_FULL = [x for x in k4 if x.compatibility_method == 'Full']
    k4_SEMI = [x for x in k4 if x.compatibility_method == 'Semi']

    k8_FULL = [x for x in k8 if x.compatibility_method == 'Full']
    k8_SEMI = [x for x in k8 if x.compatibility_method == 'Semi']

    k2_FULL_STRCT = [x for x in k2_FULL if x.merge_regime == 'Strict']
    k2_FULL_LOOSE = [x for x in k2_FULL if x.merge_regime == 'Loose']
    k2_SEMI_STRCT = [x for x in k2_SEMI if x.merge_regime == 'Strict']
    k2_SEMI_LOOSE = [x for x in k2_SEMI if x.merge_regime == 'Loose']

    k4_FULL_STRCT = [x for x in k4_FULL if x.merge_regime == 'Strict']
    k4_FULL_LOOSE = [x for x in k4_FULL if x.merge_regime == 'Loose']
    k4_SEMI_STRCT = [x for x in k4_SEMI if x.merge_regime == 'Strict']
    k4_SEMI_LOOSE = [x for x in k4_SEMI if x.merge_regime == 'Loose']

    k8_FULL_STRCT = [x for x in k8_FULL if x.merge_regime == 'Strict']
    k8_FULL_LOOSE = [x for x in k8_FULL if x.merge_regime == 'Loose']
    k8_SEMI_STRCT = [x for x in k8_SEMI if x.merge_regime == 'Strict']
    k8_SEMI_LOOSE = [x for x in k8_SEMI if x.merge_regime == 'Loose']

    k2_FULL_STRCT_compactness = round(sum([x.quality_measures['compactness'] for x in k2_FULL_STRCT]) / (len(k2_FULL_STRCT) or 1), 3)
    k4_FULL_STRCT_compactness = round(sum([x.quality_measures['compactness'] for x in k4_FULL_STRCT]) / (len(k4_FULL_STRCT) or 1), 3)
    k8_FULL_STRCT_compactness = round(sum([x.quality_measures['compactness'] for x in k8_FULL_STRCT]) / (len(k8_FULL_STRCT) or 1), 3)
    # k2_FULL_STRCT_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k2_FULL_STRCT]) / (len(k2_FULL_STRCT) or 1))
    # k4_FULL_STRCT_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k4_FULL_STRCT]) / (len(k4_FULL_STRCT) or 1))
    # k8_FULL_STRCT_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k8_FULL_STRCT]) / (len(k8_FULL_STRCT) or 1))
    k2_FULL_LOOSE_compactness = round(sum([x.quality_measures['compactness'] for x in k2_FULL_LOOSE]) / (len(k2_FULL_LOOSE) or 1), 3)
    k4_FULL_LOOSE_compactness = round(sum([x.quality_measures['compactness'] for x in k4_FULL_LOOSE]) / (len(k4_FULL_LOOSE) or 1), 3)
    k8_FULL_LOOSE_compactness = round(sum([x.quality_measures['compactness'] for x in k8_FULL_LOOSE]) / (len(k8_FULL_LOOSE) or 1), 3)
    # k2_FULL_LOOSE_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k2_FULL_LOOSE]) / (len(k2_FULL_LOOSE) or 1))
    # k4_FULL_LOOSE_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k4_FULL_LOOSE]) / (len(k4_FULL_LOOSE) or 1))
    # k8_FULL_LOOSE_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k8_FULL_LOOSE]) / (len(k8_FULL_LOOSE) or 1))

    k2_SEMI_STRCT_compactness = round(sum([x.quality_measures['compactness'] for x in k2_SEMI_STRCT]) / (len(k2_SEMI_STRCT) or 1), 3)
    k4_SEMI_STRCT_compactness = round(sum([x.quality_measures['compactness'] for x in k4_SEMI_STRCT]) / (len(k4_SEMI_STRCT) or 1), 3)
    k8_SEMI_STRCT_compactness = round(sum([x.quality_measures['compactness'] for x in k8_SEMI_STRCT]) / (len(k8_SEMI_STRCT) or 1), 3)
    # k2_SEMI_STRCT_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k2_SEMI_STRCT]) / (len(k2_FULL_STRCT) or 1))
    # k4_SEMI_STRCT_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k4_SEMI_STRCT]) / (len(k4_FULL_STRCT) or 1))
    # k8_SEMI_STRCT_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k8_SEMI_STRCT]) / (len(k8_FULL_STRCT) or 1))
    k2_SEMI_LOOSE_compactness = round(sum([x.quality_measures['compactness'] for x in k2_SEMI_LOOSE]) / (len(k2_SEMI_LOOSE) or 1), 3)
    k4_SEMI_LOOSE_compactness = round(sum([x.quality_measures['compactness'] for x in k4_SEMI_LOOSE]) / (len(k4_SEMI_LOOSE) or 1), 3)
    k8_SEMI_LOOSE_compactness = round(sum([x.quality_measures['compactness'] for x in k8_SEMI_LOOSE]) / (len(k8_SEMI_LOOSE) or 1), 3)
    # k2_SEMI_LOOSE_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k2_SEMI_LOOSE]) / (len(k2_SEMI_LOOSE) or 1))
    # k4_SEMI_LOOSE_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k4_SEMI_LOOSE]) / (len(k4_SEMI_LOOSE) or 1))
    # k8_SEMI_LOOSE_valid_plans = round(sum([x.quality_measures['n_valid_plans'] for x in k8_SEMI_LOOSE]) / (len(k8_SEMI_LOOSE) or 1))

    coverage_dict = get_dict(len(k2_FULL_STRCT), len(k2_SEMI_STRCT), len(k2_FULL_LOOSE), len(k2_SEMI_LOOSE),
                             len(k4_FULL_STRCT), len(k4_SEMI_STRCT), len(k4_FULL_LOOSE), len(k4_SEMI_LOOSE),
                             len(k8_FULL_STRCT), len(k8_SEMI_STRCT), len(k8_FULL_LOOSE), len(k8_SEMI_LOOSE))

    compactness_dict = get_dict(k2_FULL_STRCT_compactness, k2_SEMI_STRCT_compactness, k2_FULL_LOOSE_compactness, k2_SEMI_LOOSE_compactness,
                                k4_FULL_STRCT_compactness, k4_SEMI_STRCT_compactness, k4_FULL_LOOSE_compactness, k4_SEMI_LOOSE_compactness,
                                k8_FULL_STRCT_compactness, k8_SEMI_STRCT_compactness, k8_FULL_LOOSE_compactness, k8_SEMI_LOOSE_compactness
                                )

    # valid_plans_dict = get_dict(k2_FULL_STRCT_valid_plans, k2_SEMI_STRCT_valid_plans, k4_FULL_STRCT_valid_plans, k4_SEMI_STRCT_valid_plans,
    #                             k8_FULL_STRCT_valid_plans, k8_SEMI_STRCT_valid_plans,
    #                             k2_FULL_LOOSE_valid_plans, k2_SEMI_LOOSE_valid_plans, k4_FULL_LOOSE_valid_plans, k4_SEMI_LOOSE_valid_plans,
    #                             k8_FULL_LOOSE_valid_plans, k8_SEMI_LOOSE_valid_plans
    #                             )

    csv_columns = ['K2 FULL STRICT', 'K2 SEMI STRICT', 'K2 FULL LOOSE', 'K2 SEMI LOOSE', 'K4 FULL STRICT', 'K4 SEMI STRICT',
                   'K4 FULL LOOSE', 'K4 SEMI LOOSE', 'K8 FULL STRICT', 'K8 SEMI STRICT', 'K8 FULL LOOSE', 'K8 SEMI LOOSE']

    with open(path + '/' + domain + ' coverage.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in coverage_dict:
            writer.writerow(data)

    with open(path + '/' + domain + ' compactness.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in compactness_dict:
            writer.writerow(data)

    # with open(path + '/' + domain + ' valid plans.csv', 'w') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    #     writer.writeheader()
    #     for data in valid_plans_dict:
    #         writer.writerow(data)


if __name__ == "__main__":
    domain = 'turn_and_open'
    # relative_path = '/generated_tpns/Done/Temporal/'
    # compare(os.getcwd() + relative_path + domain, domain)
    compare('/home/yotama/Desktop/results/' + domain, domain)

    # filename1 = 'generated_tpns/Classical_2_plans_driverlog_p01_FULL'
    # obj1 = load_object(filename1, os.getcwd())
    # filename2 = 'generated_tpns/Done/Classical/driverlog/Classical_8_plans_driverlog_p11_FULL'
    # obj2 = load_object(filename2, os.getcwd())
    # obj = load_object(filename, '/home/yotama/Desktop')
    print()
