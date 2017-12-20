from Graph import Graph
import os

from brute_force import brute_force


def visualize(graph, name, convert = None):
    res = open(name + ".dot", "w")
    res.write("digraph " + name + "{\n")
    if convert is not None:
        graph.write_dfs_start(graph.root, res, convert)
    else:
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
    print("print_H " + s)
    begin = s.index("[")
    return s[1:begin], int(s[begin + 1])


def get_number(v, vertex, g):
    print(v)
    if v in vertex:
        n = vertex[v]
    else:
        g.add_vertex()
        n = len(vertex)
        vertex[v] = n
    return n


def create_extended_newick_graph(s, g, vertex):
    if s[-1] == "]":
        pos = s.rfind("#")
        if pos > 0:
            l, dl = create_extended_newick_graph(s[0:pos], g, vertex)
            v,  d = parse_H(s[pos:])
            v= get_number(v, vertex, g)
            #TODO check direct
            g.add_edge(l, v)
            # if d == 2:
            #     g.add_edge(l, v)
            # else:
            #     g.add_edge(v, l)
            return l, -1
        else:
            v, d = parse_H(s[pos:])
            v = get_number(v, vertex, g)
            return v, d
        pass
    else:
        if s[0] == "(":
            c = s.find(",")
            # (A)#H1[1]|(A)
            if c == -1:
                last = s.find(")")
                v = s[1:last]
                n = get_number(v, vertex, g)
                if last == len(s) - 1:
                    return n, -1
                h, direct = parse_H(s[last + 1:])
                h_n = get_number(h, vertex, g)
                if direct == 1:
                    g.add_edge(h_n, n)
                else:
                    g.add_edge(n, h_n)
                return n, -1
            else:
                c_br = 1
                while True:
                    pos = find_pos_semicolon(s[c_br:-c_br])
                    if pos is not None:
                        break
                    c_br += 1
                l, dl = create_extended_newick_graph(s[c_br:c_br + pos], g, vertex)
                r, dr = create_extended_newick_graph(s[c_br + pos + 1:-c_br], g, vertex)
                cur = len(vertex)
                vertex[cur] = "new vertex"
                g.add_vertex()
                g.add_edge(cur, l)
                g.add_edge(cur, r)
                return cur, -1
        else:
            c = s.find("#")
            if c != -1:
                v, n = parse_H(s)

                return get_number(v, vertex, g), n
            else:
                return get_number(s, vertex, g), -1


def newick_ext_f(name_f):
    f = open(name_f, "r")
    res = []
    for i, s in enumerate(f.readlines()):
        g = Graph()
        print("new string")
        convert = {}
        create_extended_newick_graph(s, g, convert)
        g.find_root()
        rev_convert = {}
        for (k, v) in convert.items():
            rev_convert[v] = k
        visualize(g, "start_" + name_f + str(i), rev_convert)
        # g.fitch()
        # visualize_fitch_step1(g, "fitch_step_1_" + name_f)
        # visualize(g, "fitch_res_" + name_f)
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


# newick_ext_f("ext_newick")
# run_brute_force("brute1")
run_brute_force("brute3")
# run_brute_force("brute2")
# calc("test2")
# calc("one")
# newick_f("test_newick")
# newick_f("big_newick")

# main("input.txt")
# main("test/test3")
# main("cactus")
