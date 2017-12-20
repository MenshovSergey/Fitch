from Graph import Graph


def cut_and_create_new_graph(g, color, new_graph, v, convert, used):
    used[v] = 1
    for ch in g.data[v]:
        if g.colors[ch] == color and g.colors[v] == color:
            new_graph.add_edge(convert[v], convert[ch])
            # new_graph.add_edge(convert[ch], convert[v])
        if used[ch] == 0:
            cut_and_create_new_graph(g, color, new_graph, ch, convert, used)


count_v = 0


def check_connectivity(g, v, used):
    global count_v
    count_v += 1
    used[v] = 1
    for ch in g.data[v]:
        if used[ch] == 0:
            check_connectivity(g, ch, used)

def find_roots(g):
    res = []
    for i, k in enumerate(g.inverse_data):
        if len(k) == 0:
            res.append(i)
    return res

def check_coloring(g, colors):
    for k in colors:
        convert = {}
        for i, c in enumerate(g.colors):
            if k == c:
                convert[i] = len(convert)
        new_g = Graph(len(convert))
        used = [0] * len(g.colors)
        cut_and_create_new_graph(g, k, new_g, 0, convert, used)
        roots = find_roots(new_g)
        if len(roots) > 1:
            continue
        used = [0] * len(new_g.data)
        check_connectivity(new_g, 0, used)
        global count_v
        if not count_v == len(convert):
            count_v = 0
            return 0

        count_v = 0

    return 1


sum = 0


def coloring(start, colors, g, convert):
    if start == len(convert):
        global sum
        c = check_coloring(g, colors)
        if c == 1:
            print(g.colors)
        sum += c
    else:

        v = convert[start]
        for k in colors:
            g.colors[v] = k
            coloring(start + 1, colors, g, convert)


def brute_force(graph):
    colors = []
    for c, count in graph.need_colors.items():
        colors.append(c)
    convert = []
    for i, v in enumerate(graph.data):
        if len(v) > 0:
            convert.append(i)
    coloring(0, colors, graph, convert)

    return sum
