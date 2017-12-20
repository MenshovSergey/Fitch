import itertools as it


def get_count_leaves(g):
    res = 0
    for k in g.data:
        if len(k) == 0:
            res += 1
    return res


def get_colours(s):
    res = []
    cur = []
    for i, v in enumerate(s):
        cur.append(i)
        if v == "1":
            res.append(cur)
            cur = []
    return res


def F(g, v, colours, answer, color=None):
    if len(g.data[v]) == 0:
        if not color is None:
            if v in answer:
                answer[v].append(color)
            else:
                answer[v] = [color]
        else:
            if len(colours) == 1:
                if v in answer:
                    answer[v].append(colours[0])
                else:
                    answer[v] = [colours[0]]
    else:
        for i in range(0, len(g.data[v])):
            for j in range(i, len(g.data[v])):

    return


def G(g, v, colours, answer, color=None):
    if len(g.data[v]) == 0:
        return
    for ch in g.data[v]:
        # TODO maybe split on colours
        s = ["0"] * (len(colours) -1)
        for i in range(len(g.data[v])):
            s[i] = "1"
        if color is None:
            G(g, ch, colours, answer, colours[0])
            F(g, ch, colours, answer, colours[0])
        else:
            G(g, ch, colours, answer, color)
            F(g, ch, colours, answer, color)
        for i in g.data[v]:
            if i != ch:
                if not color is None:
                    H(g, v, answer, colours[1:])
                    F(g, v, colours, answer, colours[0])
                else:
                    H(g, v, answer, colours)
                    F(g, v, colours, answer, color)
    pass


def H(g, v, answer, colours):
    if len(g.data[v]) == 0:
        return
    s = ["0"] * len(colours)
    for i in range(len(g.data[v])):
        s[i] = "1"
    s = "".join(s)
    for p in it.permutations(s):
        child_colours = get_colours(p)
        for i, v in enumerate(g.data[v]):
            H(g, v, child_colours[i], answer)
            F(g, v, child_colours[i], answer)


def generate(g):
    count_colors = get_count_leaves(g)
    colours = [i for i in range(count_colors)]
