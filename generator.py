from collections import defaultdict

__author__ = 'nikita'
import networkx as nx
import itertools
import random


# import readNewick

def split_list(a, k):
    res = []
    if k == 0:
        if len(a) == 0:
            return [[]]
        else:
            return []
    if len(a) >= k:
        n = len(a)
        dividers = itertools.combinations(list(range(n - 1)), k - 1)
        for pos in dividers:
            cur = 0
            split = []
            for i in pos:
                split.append(a[cur:i + 1])
                cur = i + 1
            split.append(a[cur:])
            res.append(split)
    return res


def split_list_empty(a, k):
    res = []
    n = len(a)
    dividers = itertools.combinations(list(range(n + k - 1)), k - 1)
    cur = 0
    split = []
    for pos in dividers:
        cur = 0
        split = []
        for i in range(len(pos)):
            split.append(a[cur:pos[i] - i])
            cur = pos[i] - i
        split.append(a[cur:])
        res.append(split)
    return res


def cartes(lists):
    # lists is list of lists oф dictionaries
    res = []
    if len(lists) == 0:
        return []
    if len(lists) == 1:
        return lists[0]
    if len(lists) == 2:
        # list[{}]
        for i in lists[0]:
            for j in lists[1]:
                z = i.copy()
                z.update(j)
                res.append(z)
        return res
    else:
        new_colorings = lists[1:]
        tail_res = cartes(new_colorings)
        res = cartes([lists[0], tail_res])
        return res


def all_leaves(G, v):
    if len(G.data[v]) == 0:
        return [v]
    else:
        res = []
        for u in G.data[v]:
            res.extend(all_leaves(G, u))
        return res


def all_color(G, v, colors, all_results):
    if (v, tuple(colors)) in all_results:
        return all_results[(v, tuple(colors))]
    Fc = []
    Gc = []
    Hc = []
    if len(all_leaves(G, v)) < len(colors):
        # all_results[(v,tuple(colors))] = (Fc,Gc,Hc)
        return (Fc, Gc, Hc)
    if len(G.data[v]) == 0:
        if len(colors) == 1:
            ans = dict()
            ans[v] = colors[0]
            Fc = [ans]
    else:
        children = G.data[v]
        num_of_ch = len(children)
        for k in range(0, num_of_ch + 1):
            if k == 0:
                splits = split_list(colors, num_of_ch)
                for split in splits:
                    f_or_h = []
                    for ch in range(len(children)):
                        res_ch = all_color(G, children[ch], split[ch], all_results)
                        f_or_h.append(res_ch[0] + res_ch[2])
                    Hc.extend(cartes(f_or_h))
            # if k == 1:
            #     for ch in range(len(children)):
            #         for co in range(1,len(colors)-num_of_ch+2):
            #             res_ch = all_color(G,children[ch],colors[:co])
            #             f_or_g = res_ch[0]+res_ch[1]
            #             splits = split_list(colors[co:],num_of_ch-1)
            #             for split in splits:
            #                 f_or_h = []
            #                 oc = 0
            #                 for ch2 in range(len(children)):
            #                     if not ch2 == ch:
            #                         res_ch = all_color(G,children[ch2],split[oc])
            #                         oc += 1
            #                         f_or_h.append(res_ch[0]+res_ch[1])
            #                 Gc.extend(cartes([f_or_g]+f_or_h))
            if k >= 1:
                options = itertools.combinations(children, k)
                for choosen in options:
                    for co in range(1, len(colors) - num_of_ch + k + 1):
                        choosen_colors = colors[1:co]
                        other_colors = colors[co:]
                        choosen_splits = split_list_empty(choosen_colors, k)
                        other_splits = split_list(other_colors, num_of_ch - k)
                        for csplit in choosen_splits:
                            for osplit in other_splits:
                                cc = 0
                                oc = 0
                                f_or_h = []
                                f_or_g = []
                                for u in children:
                                    if u in choosen:
                                        res_ch = all_color(G, u, [colors[0]] + csplit[cc], all_results)
                                        cc += 1
                                        f_or_g.append(res_ch[0] + res_ch[1])
                                    else:
                                        res_ch = all_color(G, u, osplit[oc], all_results)
                                        oc += 1
                                        f_or_h.append(res_ch[0] + res_ch[2])
                                if k == 1:
                                    Gc.extend(cartes(f_or_g + f_or_h))
                                else:
                                    Fc.extend(cartes(f_or_g + f_or_h))

    if len(all_leaves(G, v)) > 3:
        all_results[(v, tuple(colors))] = (Fc, Gc, Hc)
    return (Fc, Gc, Hc)


def make_random_tree(k):
    G = nx.DiGraph()
    G.add_node(0)
    G.add_edge(0, 3)
    G.add_edge(0, 1)
    G.add_edge(0, 2)
    num_of_leaves = 3
    vol = 4
    while num_of_leaves < k:
        leaves = all_leaves(G, 0)
        l = random.choice(leaves)
        G.add_edge(l, vol)
        G.add_edge(l, vol + 1)
        vol += 2
        num_of_leaves += 1
    return G


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


def find_root(G):
    for v in G.nodes():
        if len(list(G.predecessors(v))) == 0:
            return v


def find_root_test(G):
    k = 0
    for v in G.nodes():
        if len(list(G.predecessors(v))) == 0:
            k += 1
    if k > 1:
        return 'Alarm!'
    else:
        return 'OK'


# graph_list = readNewick.eNewick_to_graph('a.tree')
# G = graph_list[0]
def gen_coloring(G):
    import time
    start = time.clock()
    # G = make_random_tree(20)

    # G = nx.DiGraph()
    # G.add_edge(0,1)
    # G.add_edge(0,2)
    # G.add_edge(0,7)
    # G.add_edge(0,13)
    # G.add_edge(1,6)
    # G.add_edge(1,11)
    # G.add_edge(2,3)
    # G.add_edge(2,4)
    # G.add_edge(2,5)
    # G.add_edge(2,14)
    # G.add_edge(7,8)
    # G.add_edge(8,10)
    # G.add_edge(8,12)
    # G.add_edge(7,9)

    root = G.find_root()
    print("count vertex in graph = " + str(len(G.data)))

    max_k = len(all_leaves(G, root))
    all_colorings = []

    for k in range(max_k):
        all_results = dict()

        Fc, Gc, Hc = all_color(G, G.root, list(range(k + 1)), all_results)
        # print(k + 1, len(Fc) + len(Hc))
        for ff in Fc:
            all_colorings.append(dict_to_tuple(ff))
        for hh in Hc:
            all_colorings.append(dict_to_tuple(hh))

    print("time for generate coloring = " + str(time.clock() - start))
    print("count all colorings for this graph = "+ str(len(all_colorings)))
    return set(all_colorings)
    # print(Fc)
    # print(Gc)
    # print(Hc)
    # print(cartes([]))
