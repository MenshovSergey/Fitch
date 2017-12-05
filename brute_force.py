from Graph import Graph


def cut_and_create_new_graph(g, color, new_graph, v, convert):
    for ch in g.data[v]:
        if g.colors[ch] == color and g.colors[v] == color:
            new_graph.add_edge(convert[v], convert[ch])
        cut_and_create_new_graph(g, color, new_graph, ch, convert)


count_v = 0


def check_connectivity(g, v):
    global count_v
    count_v += 1
    for ch in g.data[v]:
        check_connectivity(g, ch)


def check_coloring(g, colors):
    for k in colors:
        convert = {}
        for i, c in enumerate(g.colors):
            if k == c:
                convert[i] = len(convert)
        new_g = Graph(len(convert))
        cut_and_create_new_graph(g, k, new_g, 0, convert)
        check_connectivity(new_g, 0)
        global count_v
        if not count_v == len(convert):
            return 0

        count_v = 0

    return 1


sum = 0


def coloring(start, end, colors, g):
    if start == end:
        global sum
        sum += check_coloring(g, colors)
        print(g.colors)

    for i in range(start, end):
        if len(g.data[i]) == 0:
            if i == end - 1:
                sum += check_coloring(g, colors)
                print(g.colors)
            continue
        else:
            for k in colors:
                g.colors[i] = k
                coloring(i + 1, end, colors, g)

def brute_force(graph):
    colors = []
    for c, count in graph.need_colors.items():
        colors.append(c)

    coloring(0, len(graph.data), colors, graph)

    return sum
