from Graph import Graph
import os


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
        l = create_newick_graph(s[1:pos+1], g)
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


def main(name_f):
    graph = read_data(name_f)
    graph.find_root()
    visualize(graph, "start_" + name_f)
    graph.fitch()
    visualize_fitch_step1(graph, "fitch_step_1_" + name_f)
    visualize(graph, "fitch_res_" + name_f)


newick_f("test_newick")

# main("input.txt")
# main("test/test3")
# main("cactus")
