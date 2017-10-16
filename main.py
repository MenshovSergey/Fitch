from Graph import Graph
import os


def visualize(graph, name):
    res = open(name + ".dot", "w")
    res.write("digraph " + name + "{\n")
    graph.write_dfs(graph.root, res)
    res.write("}")
    res.close()
    os.system("dot " + name + ".dot -Tpng -o " + name + ".png")


# TODO
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


def main(name_f):
    graph = read_data(name_f)
    graph.find_root()
    visualize(graph, "start")
    graph.fitch()
    visualize_fitch_step1(graph, "fitch_step_1")
    visualize(graph, "fitch_res")


main("input.txt")
