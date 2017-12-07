from Graph import Graph
import os

from brute_force import brute_force


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


def parse_H(s):
    begin = s.index("[")
    return s[1:(begin + 1)], int(s[begin + 1])


def get_number(v, vertex):
    if v in vertex:
        n = vertex[v]
    else:
        n = len(vertex)
        vertex[v] = n
    return n


def create_extended_newick_graph(s, g, vertex):
    if s[0] == "(":
        c = s.find(",")
        # (A)#H1[1]|(A)
        if c == -1:
            last = s.find(")")
            v = s[0:(last + 1)]
            n = get_number(v, vertex)
            if last == len(s):
                return n, -1
            h, direct = parse_H(s[last + 1])
            h_n = get_number(h, vertex)
            if direct == 1:
                g.add_edge(h_n, n)
            else:
                g.add_edge(n, h_n)
            return n, -1
        else:
            pos = find_pos_semicolon(s[1:-1])
            l, dl = create_extended_newick_graph(s[1:pos + 1], g, vertex)
            r, dr = create_extended_newick_graph(s[pos + 2:-1], g, vertex)
            cur = len(vertex)
            vertex[cur] = "new vertex"
            if dl == 1:
                g.add_edge(cur, l)
            else:
                g.add_edge(l, cur)
            g.add_edge(cur, r)
            return cur, -1
    else:
        c = s.find("#")
        if c == -1:
            return parse_H(s)
        else:
            return get_number(s, vertex), -1


def newick_ext_f(name_f):
    f = open(name_f, "r")
    res = []
    for s in f.readlines():
        g = Graph()
        create_extended_newick_graph(s, g, {})
        g.find_root()
        visualize(g, "start_" + name_f)
        g.fitch()
        visualize_fitch_step1(g, "fitch_step_1_" + name_f)
        visualize(g, "fitch_res_" + name_f)
        res.append(g)


def main(name_f):
    graph = read_data(name_f)
    graph.find_root()
    visualize(graph, "start_" + name_f)
    graph.fitch()
    visualize_fitch_step1(graph, "fitch_step_1_" + name_f)
    visualize(graph, "fitch_res_" + name_f)


def calc(name_f):
    graph = read_data(name_f)
    graph.find_root()
    visualize(graph, "start_" + name_f)
    graph.calculate(graph.root)
    print(graph.F[0])
    print(graph.H[0])
    print(graph.F[0] + graph.H[0])
    print("end")


def run_brute_force(name_f):
    graph = read_data(name_f)
    graph.find_root()
    visualize(graph, "start_" + name_f)
    res = brute_force(graph)
    print(res)


# run_brute_force("brute1")
run_brute_force("brute2")
# calc("test2")
# calc("one")
# newick_f("test_newick")
# newick_f("big_newick")

# main("input.txt")
# main("test/test3")
# main("cactus")
