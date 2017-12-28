from collections import defaultdict
import networkx as nx

import partitions


def all_leaves(G, v):
    if len(G.neighbors(v)) == 0:
        return [v]
    else:
        res = []
        for u in G.neighbors(v):
            res.extend(all_leaves(G, u))
        return res


def find_root(G):
    for v in G.nodes():
        if len(G.predecessors(v)) == 0:
            return v


def tuple_to_dict(tup):
    k = 0
    res = dict()
    for i in list(tup):
        if i == -1:
            k += 1
        else:
            res[i] = k
    return res


def dict_to_tuple(di):
    keys = sorted(list(di.keys()))
    sets = defaultdict(list)
    vals = dict()
    num = 0
    for key in keys:
        val = di[key]
        if val in vals:
            k = vals[val]
        else:
            vals[val] = num
            num += 1
            k = vals[val]
        sets[k].append(key)
    res = []
    for i in range(num):
        res.extend(sets[i])
        res.append(-1)
    return tuple(res)


def is_rooted(G):
    roots = []
    for v in G.nodes():
        if len(G.predecessors(v)) == 0:
            roots.append(v)
    if len(roots) == 1:
        root = roots[0]
        res = True
        for v in G.nodes():
            if not nx.has_path(G, root, v):
                res = False
        return res
    else:
        return False


def is_convex_full(G, colors):
    same_color = defaultdict(list)
    for v in colors.keys():
        same_color[colors[v]].append(v)
    res = True
    for color in same_color.keys():
        Gc = nx.subgraph(G, same_color[color])
        if not is_rooted(Gc):
            res = False
    return res


def generate(G, colors):
    not_colored = sorted(list(set(G.nodes()).difference(set(colors.keys()))))
    if len(not_colored) == 0:
        return [colors.copy()]
    res = []
    v = not_colored[0]
    cols = []
    for vl in all_leaves(G, v):
        cols.append(colors[vl])
    cols = sorted(list(set(cols)))
    for col in cols:
        new_colors = colors.copy()
        new_colors[v] = col
        res.extend(generate(G, new_colors))
    return res


def is_convex_leaves(G, colors):
    root = find_root(G)
    leaves = all_leaves(G, root)
    if set(leaves) != set(colors.keys()):
        print('not all leaves are colored,or some not leaves are colored!')
        return False
    not_colored = list(set(G.nodes()).difference(set(leaves)))
    all_possible = generate(G, colors)
    res = False
    for col in all_possible:
        if is_convex_full(G, col):
            res = True
            return res
    return res


# G = nx.DiGraph()
# G.add_edge(0,1)
# G.add_edge(0,2)
# G.add_edge(0,7)
# G.add_edge(0,8)
# G.add_edge(1,6)
# G.add_edge(2,6)
# G.add_edge(1,3)
# G.add_edge(2,4)
# G.add_edge(6,5)
# G.add_edge(6,9)

# print(set(all_leaves(G,0)))
#
#
# colors = dict()
# colors[3] = 1
# colors[4] = 1
# colors[5] = 1
# colors[7] = 2
# colors[8] = 2
# colors[9] = 1
#
# print(is_convex_leaves(G,colors))
#
# G = nx.DiGraph()
# G.add_edge(0,11)
# G.add_edge(11,6)
# G.add_edge(6,14)
# G.add_edge(6,1)
# G.add_edge(11,5)
# G.add_edge(1,13)
# G.add_edge(13,5)
# G.add_edge(5,15)
# G.add_edge(13,4)
# G.add_edge(4,7)
# G.add_edge(4,8)
# G.add_edge(1,9)
# G.add_edge(9,8)
# G.add_edge(8,2)
# G.add_edge(9,12)
# G.add_edge(12,10)
# G.add_edge(12,3)
#
# col = (2, 15, -1, 3, 10, 14, -1, 7, -1)
# coloring = tuple_to_dict(col)
#
# print(is_convex_leaves(G,coloring))
#
#
#
#
def brute_force(G, col):
    root = find_root(G)
    leaves = list(set(all_leaves(G, root)))
    all_pos = partitions.all_parts(leaves)

    kk = 0
    for col in all_pos:
        coloring = partitions.as_a_coloring(col)
        if is_convex_leaves(G, coloring):
            kk += 1
    return kk

# print(kk)
