import os
from Graph import Graph
from brute_force_n import brute_force, is_convex_leaves
from eNewickRead import eNewick_to_graph
from split_network import calculate_colorings


def visualize_networkx(g, colors):
    pass


def visualize(graph, name):
    res = open(name + ".dot", "w")
    res.write("digraph " + name + "{\n")
    graph.write_dfs_start(graph.root, res)
    res.write("}")
    res.close()
    os.system("dot " + name + ".dot -Tpng -o " + name + ".png")


def visualize_fitch_step1(graph, name):
    res = open(name + ".dot", "w")
    res.write("digraph " + name + "{\n")
    graph.write_fitch_step1(graph.root, res)
    res.write("}")
    res.close()
    os.system("dot " + name + ".dot -Tpng -o " + name + ".png")


def read_data(name_f):
    f = open(name_f, "r")
    n, m, count_color = f.readline().split(" ")
    n = int(n)
    m = int(m)
    count_color = int(count_color)
    graph = Graph(m)
    for i in range(n):
        a, b = f.readline().split(" ")
        graph.add_edge(int(a), int(b))

    f.readline()
    for i in range(count_color):
        n, c = f.readline().split(" ")
        graph.add_color(int(n), int(c))
    return graph


def read_graph_colors(name_f):
    f = open(name_f, "r")
    n, m, count_color = f.readline().split(" ")
    n = int(n)
    m = int(m)
    count_color = int(count_color)
    graph = Graph(m)
    for i in range(n):
        a, b = f.readline().split(" ")
        graph.add_edge(int(a), int(b))

    f.readline()
    colors = {}
    for i in range(count_color):
        n, c = f.readline().split(" ")
        colors[n] = c
    return graph, colors


# def read_graph_dict_colors(name_f):
#     f = open(name_f, "r")
#     n, m, count_color = f.readline().split(" ")
#     n = int(n)
#     m = int(m)
#     count_color = int(count_color)
#     graph = Graph(m)
#     for i in range(n):
#         a, b = f.readline().split(" ")
#         graph.add_edge(int(a), int(b))
#     f.readline()
#
#     for i in range(count_color):
#         s = f.readline()
#         vals = s.split(" ")
#         for v in vals:
#             graph.add_color(int(v), i)
#
#     return graph
def read_only_colors_p(f):
    res = {}
    count_colour = int(f.readline())
    for i in range(count_colour):
        s = f.readline()
        leaves = s.split(" ")
        for v in leaves:
            res[i] = v

    return res


def read_only_colors_l(input_coloring):
    f = open(input_coloring, "r")
    colors = {}
    count_colour = int(f.readline())
    for i in range(count_colour):
        n, c = f.readline().split(" ")

        colors[int(n)] = int(c)
    return colors


def read_only_graph(input_graph):
    f = open(input_graph, "r")
    n, m = f.readline().split(" ")
    n = int(n)
    m = int(m)
    graph = Graph(m)
    for i in range(n):
        a, b = f.readline().split(" ")
        graph.add_edge(int(a), int(b))
    return graph


def fitch(g, need_draw, name_f):
    if need_draw:
        visualize(g, "start_" + name_f)
    g.fitch()
    if need_draw:
        visualize_fitch_step1(g, "fitch_step_1_" + name_f)
        visualize(g, "fitch_res_" + name_f)


def main(input_graph, input_type, task, input_coloring, draw=False):
    if input_type[0] == "E":
        g = read_only_graph(input_graph)
    elif input_type[0] == "N":
        g = eNewick_to_graph(input_graph)
    else:
        print("UNKNOWN FORMAT " + input_type[0])
        return -1

    colors = {}
    if len(input_type) == 2:
        if input_type[1] == "L":
            colors = read_only_colors_l(input_coloring)
        elif input_type[1] == "P":
            colors = read_only_colors_p(input_coloring)
        else:
            print("UNKNOWN FORMAT " + input_type[1])
            return -1

    g.find_root()
    is_tree = g.is_tree()
    if task == "check_if_convex":
        if is_tree:
            g.set_colors(colors)
            fitch(g, draw, input_graph)
        else:
            print("Target graph is cactus/network")
            if draw:
                visualize_networkx(g[0], colors)
            res = is_convex_leaves(g[0], colors)
            if res:
                print("Convex for graph is convex")
            else:
                print("Convex for graph not convex")
    elif task == "count":
        if is_tree:
            g.calculate(g.root)
            print("count convex colorings = " + str(g.F[g.root] + g.H[g.root]))
        else:
            calculate_colorings(g)
    else:
        print("UNKNOWN TASK " + task)
        return -1
    # if task == "is_convex_tree":
    #     if input_type == "E":
    #         print("For fitch need only CE or N or CDE format")
    #     fitch(g, draw, input_graph)
    # elif task == "calc":
    #     if draw:
    #         visualize(g, "start_" + input_graph)
    #     g.calculate(g.root)
    #     print("F(root) = " + str(g.F[g.root]))
    #     print("H(root) = " + str(g.H[g.root]))
    #     print("G(root) = " + str(g.G[g.root]))
    #     print("F(root) + H(root) = " + str(g.F[g.root] + g.H[g.root]))
    # elif task == "brute":
    #     g, colors = read_graph_colors(input_graph)
    #     c = brute_force(g, colors)
    #     print("count convex coloring = " + str(c))
    # elif task == "calc_network_cactus":
    #     calculate_colorings(input_graph)
    #
    # elif task == "is_convex_network":
    #     g, colors = read_graph_colors(input_graph)
    #     res = is_convex_leaves(g, colors)
    #     if res:
    #         print("This graph has convex coloring")
    #     else:
    #         print("This graph don't have convex coloring")
    # else:
    #     print("Unknown target" + task)
    #     return -1


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--task")
parser.add_argument("--input_graph")
parser.add_argument("--input_coloring")
parser.add_argument("--input_type")
parser.add_argument("--draw", type=bool)

args = vars(parser.parse_args())

main(args["input_graph"], args["input_type"], args["task"], args["input_coloring"], args["draw"])
