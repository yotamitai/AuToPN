from __future__ import division
import matplotlib.pyplot as plt
import itertools
import networkx as nx
import numpy as np

def visualize(tpn):
    """visualize the tpn"""

    """initialize graph"""
    G = nx.DiGraph()

    """get edges"""
    tpn_edges = get_edges(tpn.graph)

    """get nodes from edges"""
    G.add_edges_from(tpn_edges, weight=1)

    """initial and terminal nodes"""
    terminal_index = tpn.nodes.index('T')
    initial_index = tpn.nodes.index('I')

    """node colors and sizes"""
    nodelist = tpn.nodes
    node_sizes = [20]*len(nodelist)
    node_colors = ['blue']*len(tpn.nodes)
    node_sizes[initial_index] = 100
    node_colors[initial_index] = 'red'
    node_sizes[terminal_index] = 100
    node_colors[terminal_index] = 'green'

    # pos = nx.layout.kamada_kawai_layout(G)
    # fruchterman_reingold_layout  spring_layout   kamada_kawai_layout

    pos = [nx.layout.kamada_kawai_layout(G), nx.layout.fruchterman_reingold_layout(G),
           nx.layout.spring_layout(G)]
    for p in pos:
        nx.draw_networkx_nodes(G, p, nodelist=nodelist, node_size=node_sizes, node_color=node_colors)
        nx.draw_networkx_edges(G, p, node_size=1, arrowstyle='->', arrowsize=10, edge_color='black', width=2)
        ax = plt.gca()
        ax.set_axis_off()
        plt.show()

    return


def get_edges(graph):
    edges = []
    for edge in graph:
        for node in graph[edge]:
            edges.append((edge, node))
    return edges


def bar_chart_graph(features, max_v, mean_v, name):

    width = 0.8

    indices = np.arange(len(features))

    plt.bar(indices, max_v, width=width,
            color='b', label='Max Diversity')
    plt.bar(indices, mean_v,
            width=0.7 * width, color='r', label='Mean Diversity')

    plt.xticks(indices,
               ['{} Score'.format(i) for i in features])

    plt.legend()
    plt.ylabel('Score')
    plt.xlabel('Criteria')
    plt.tight_layout()
    plt.title('Max Vs. Mean Diveristy plan set. Instance: ' + name)

    plt.show()

    return


def lama_iteration_score_graph(tpns):

    compactness_vec, generality_vec, max_div_vec, validity_dist_vec, names = [], [], [], [], []
    for tpn in tpns:
        compactness_vec.append(tpn.goodness_measures.compactness)
        generality_vec.append(tpn.goodness_measures.generality)
        max_div_vec.append(tpn.goodness_measures.max_diversity)
        validity_dist_vec.append(tpn.goodness_measures.validity_increase)
        names.append(tpn.name)

    # iterations = ['Sol_'+str(x) for x in range(len(tpns))]
    iterations = []

    for name in names:
        if "Python" in name:
            label = 'Python'
        elif "lama" in name:
            label = 'lama' + name[-1]
        else:
            label = 'ff'

        if "Random" in name:
            label += '.R'
        else:
            label += '.M'

        if "action" in name:
            label += ".A"
        else:
            label += ".L"

        label += '.' + name.split('_')[1][:3]
        label += '.' + [x for x in name.split('_') if x[0] == 'H'][0]


        iterations.append(label)

    labels = ['Compactness', 'Generality', 'Max Diversity', 'Validity Increase']
    colors = ["r", "b", "g", "c", "m", "k", "y"]
    values = [compactness_vec, generality_vec, max_div_vec, validity_dist_vec]

    file_name = ' '.join(names[0].split('_')[:2])
    f = plt.figure()
    f.legend(labels)
    f.suptitle(file_name + '\nGoodness Measures', fontsize=14)

    # ax0 = plt.subplot2grid((5, 2), (0, 0), rowspan=1, colspan=2)
    ax1 = plt.subplot2grid((7, 2), (1, 0), rowspan=2, colspan=1)
    ax2 = plt.subplot2grid((7, 2), (1, 1), rowspan=2, colspan=1)
    ax3 = plt.subplot2grid((7, 2), (4, 0), rowspan=2, colspan=1)
    ax4 = plt.subplot2grid((7, 2), (4, 1), rowspan=2, colspan=1)

    axes = [ax1, ax2, ax3, ax4]

    f.subplots_adjust(hspace=0.7, wspace=0.4)
    for i in range(len(axes)):
        axes[i].scatter(iterations, values[i], color=colors[:len(tpns)])
        axes[i].set_ylabel(labels[i])
        axes[i].set_xticklabels(iterations, fontsize='small')
        for tick in axes[i].get_xticklabels():
            tick.set_rotation(90)

    # from mpl_toolkits.mplot3d import Axes3D
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.scatter(compactness_vec, generality_vec, validity_dist_vec)
    # ax.set_xlabel('Compactness')
    # ax.set_ylabel('Generality')
    # ax.set_zlabel('Validity Increase')

    # plt.figure()
    # plt.title(file_name + '\n Compactness vs Generality')
    # plt.scatter(compactness_vec, generality_vec)
    # plt.xlabel('Generality')
    # plt.ylabel('Compactness')
    # plt.show()
    #
    # plt.figure()
    # plt.title(file_name + '\n Compactness vs Validity Increase')
    # plt.scatter(compactness_vec, validity_dist_vec)
    # plt.xlabel('Validity Increase')
    # plt.ylabel('Compactness')
    # plt.show()
    #
    # plt.figure()
    # plt.title(file_name + '\n Validity Increase vs Generality')
    # plt.scatter(validity_dist_vec, generality_vec)
    # plt.xlabel('Validity Increase')
    # plt.ylabel('Compactness')
    plt.show()



    print()


def goodness_by_h(h_dict):

    compactness = {}
    validity = {}
    generality = {}
    diversity = {}

    for h in h_dict:
        data = []
        for tpn in h_dict[h]:
            data.append([tpn.name, tpn.goodness_measures])
        data.sort(key=lambda x: x[0])
        compactness[h] = [x[1].compactness for x in data]
        validity[h] = [x[1].validity_increase for x in data]
        generality[h] = [x[1].generality for x in data]
        diversity[h] = [x[1].max_diversity for x in data]

    tpn_names = [' '.join(x[0].split('_')[:2]) for x in data]

    f = plt.figure()
    f.suptitle('Goodness Measures by Heuristic', fontsize=14)
    labels = ['Compactness', 'Generality', 'Max Diversity', 'Validity Increase']
    values = [compactness, generality, validity, diversity]

    ax1 = plt.subplot2grid((7, 2), (1, 0), rowspan=2, colspan=1)
    ax2 = plt.subplot2grid((7, 2), (1, 1), rowspan=2, colspan=1)
    ax3 = plt.subplot2grid((7, 2), (4, 0), rowspan=2, colspan=1)
    ax4 = plt.subplot2grid((7, 2), (4, 1), rowspan=2, colspan=1)

    axes = [ax1, ax2, ax3, ax4]

    f.subplots_adjust(hspace=0.7, wspace=0.4)
    for i in range(len(axes)):
        for h in h_dict:
            axes[i].plot(tpn_names, values[i][h], '-o', label=h, alpha=0.5)
        axes[i].set_ylabel(labels[i])
        axes[i].set_xticklabels(tpn_names, fontsize='small')
        for tick in axes[i].get_xticklabels():
            tick.set_rotation(90)
    axes[i].legend()


    plt.show()

    print()


