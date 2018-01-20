import networkx as nx

import phylonetwork3
from Graph import Graph


def eNewick_to_graph(eNewick_file):
    eNewick_list = []
    graph_list = []
    with open(eNewick_file, 'r') as data:
        for line in data:
            eNewick_list.append(line)

    for i in range(len(eNewick_list)):
        network = phylonetwork3.classes.PhyloNetwork(eNewick=eNewick_list[i])
        root = network.roots()[0]
        node_names = []
        for name in list(network.nodes()):
            if name != root:
                node_names.append(name)

        number_node = {node_names[i]:(i + 1) for i in range(len(node_names))}
        number_node[root] = 0

        leaves_number = [number_node[key] for key in list(network.leaves())]

        nemed_edges = phylonetwork3.classes.LGTPhyloNetwork(network).principal_edges()
        edges = [(number_node[edge[0]], number_node[edge[1]]) for edge in nemed_edges]

        topology = Graph(len(node_names) + 1)
        for e in edges:
            a, b = e
            topology.add_edge(a, b)
        graph_list.append(topology)
    return graph_list


def eNewick_to_networkx(eNewick_file):
    eNewick_list = []
    graph_list = []
    with open(eNewick_file, 'r') as data:
        for line in data:
            eNewick_list.append(line)

    for i in range(len(eNewick_list)):
        network = phylonetwork3.classes.PhyloNetwork(eNewick=eNewick_list[i])
        root = network.roots()[0]
        node_names = []
        for name in list(network.nodes()):
            if name != root:
                node_names.append(name)

        number_node = {node_names[i]:(i + 1) for i in range(len(node_names))}
        number_node[root] = 0

        leaves_number = [number_node[key] for key in list(network.leaves())]

        nemed_edges = phylonetwork3.classes.LGTPhyloNetwork(network).principal_edges()
        edges = [(number_node[edge[0]], number_node[edge[1]]) for edge in nemed_edges]

        topology = nx.DiGraph()
        for e in edges:
            a, b = e
            topology.add_edge(a, b)
        graph_list.append(topology)
    return graph_list


if __name__ == '__main__':
    print(len(eNewick_to_graph("JoinRes/more_networks_2.tree")))