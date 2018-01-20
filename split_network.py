from collections import OrderedDict

from Graph import Graph
from eNewickRead import eNewick_to_graph
from generator import gen_coloring


def get_bin_masks(size):
    return [[int(i) for i in format(x, 'b').zfill(size)] for x in range(2 ** size)]

def remove_new_leaves(network, new_tree):
    rem = []
    for i, v in enumerate(new_tree.data):
        if len(v) == 0:
            if len(network.data[i]) > 0:
                rem.append(i)
    return rem

def create(child_list, all_income_edge, homoplasy_set, homoplasy, mask, bad):
    topology = Graph(len(child_list))
    # add all normal edge
    for v in all_income_edge.keys():
        if v in bad:
            continue
        if v not in homoplasy_set:
            for e in all_income_edge[v]:
                a, b = e
                topology.add_edge(a, b)
    for i in range(len(homoplasy)):
        # add one of the homoplasy edge
        a, b = all_income_edge[homoplasy[i]][mask[i]]
        topology.add_edge(a, b)
    return topology

def tree_variations(network):
    child_list = network.data

    all_income_edge = OrderedDict()
    for i in range(len(child_list)):
        all_income_edge[i] = []

    for i in range(len(child_list)):
        for e in child_list[i]:
            all_income_edge[e].append((i, e))

    homoplasy = [i for i in all_income_edge.keys() if len(all_income_edge[i]) > 1]
    homoplasy_set = set(homoplasy)
    tree_variations_arr = []
    for mask in get_bin_masks(len(homoplasy)):
        topology = Graph(len(child_list))
        # add all normal edge
        for v in all_income_edge.keys():
            if v not in homoplasy_set:
                for e in all_income_edge[v]:
                    a, b = e
                    topology.add_edge(a, b)
        for i in range(len(homoplasy)):
            # add one of the homoplasy edge
            a, b = all_income_edge[homoplasy[i]][mask[i]]
            topology.add_edge(a, b)

        bad = remove_new_leaves(network, topology)
        topology = create(child_list, all_income_edge,homoplasy_set, homoplasy, mask, bad)
        tree_variations_arr.append(topology)
    print("start\n")
    return tree_variations_arr


def calculate_colorings(network_list):
    # network_list = eNewick_to_graph(name_f)
    # for topology in network_list:
    #     leaves_number = topology.get_leaves()
    #     t = time.time()
    #     print(run_brute_force(topology, leaves_number))
    #     print("timing  ", time.time() - t)

    # network_list[0].find_root()
    # visualize(network_list[0], "network14")
    for i in network_list:
        all_answer = set([])
        for tree in tree_variations(i):
            all_answer = all_answer.union(gen_coloring(tree))
            print(len(all_answer))
        print("calculate")
        print(len(all_answer))