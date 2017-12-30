import os

from Graph import Graph
from brute_force_n import brute_force
from split_network import calculate_colorings


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


def read_graph_dict_colors(name_f):
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
        s = f.readline()
        vals = s.split(" ")
        for v in vals:
            graph.add_color(int(v), i)

    return graph


def read_only_graph(name_f):
    f = open(name_f, "r")
    n, m = f.readline().split(" ")
    n = int(n)
    m = int(m)
    graph = Graph(m)
    for i in range(n):
        a, b = f.readline().split(" ")
        graph.add_edge(int(a), int(b))
    return graph


def find_pos_semicolon(s):
    c = 0
    for i, v in enumerate(s):
        if v == "(":
            c += 1
        if v == ")":
            c -= 1
        if v == "," and c == 0:
            return i


def create_newick_graph(s, g):
    g.add_vertex()
    cur = len(g.data) - 1
    if s[0] == "(":
        pos = find_pos_semicolon(s[1:-1])
        l = create_newick_graph(s[1:pos + 1], g)
        r = create_newick_graph(s[pos + 2:-1], g)
        g.add_edge(cur, l)
        g.add_edge(cur, r)
        return cur
    else:
        g.add_color(cur, int(s))
        return cur


def newick_f(name_f):
    f = open(name_f, "r")
    s = f.readline()
    g = Graph()
    create_newick_graph(s, g)
    g.find_root()
    visualize(g, "start_" + name_f)
    g.fitch()
    visualize_fitch_step1(g, "fitch_step_1_" + name_f)
    visualize(g, "fitch_res_" + name_f)


def fitch(g, need_draw, name_f):
    if need_draw:
        visualize(g, "start_" + name_f)
    g.fitch()
    if need_draw:
        visualize_fitch_step1(g, "fitch_step_1_" + name_f)
        visualize(g, "fitch_res_" + name_f)


def main(name_f, format, target, draw):
    if format == "CE":
        g = read_data(name_f)
    elif format == "E":
        g = read_only_graph(name_f)
    elif format == "N":
        g = newick_f(name_f)
    elif format == "CDE":
        g = read_graph_dict_colors(name_f)
    else:
        print("Unknown format " + format)
        return -1
    g.find_root()
    if target == "fitch":
        if format == "E":
            print("For fitch need only CE or N or CDE format")
        fitch(g, draw, name_f)
    elif target == "calc":
        if draw:
            visualize(g, "start_" + name_f)
        g.calculate(g.root)
        print("F(root) = " + str(g.F[g.root]))
        print("H(root) = " + str(g.H[g.root]))
        print("G(root) = " + str(g.G[g.root]))
        print("F(root) + H(root) = " + str(g.F[g.root] + g.H[g.root]))
    elif target == "brute":
        g, colors = read_graph_colors(name_f)
        c = brute_force(g, colors)
        print("count convex coloring = " + str(c))
    elif target == "calc_network_cactus":
        calculate_colorings(name_f)
    else:
        print("Unknown target" + target)
        return -1


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--target")
parser.add_argument("--format")
parser.add_argument("--draw", type=bool)
parser.add_argument("--name")

args = vars(parser.parse_args())

main(args["name"], args["format"], args["target"], args["draw"])
