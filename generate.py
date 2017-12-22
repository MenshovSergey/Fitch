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


def get_count_not_empty(current):
    res = []
    for i, v in enumerate(current):
        if v == "1":
            res.append(i)
    return res


def get_all_split(default_colour, colours, convert_k, convert_children):
    # 0 if set of colour is empty and need default colour
    count_children = len(convert_children)
    k = len(convert_k)
    for current in it.product("01", repeat=k):
        s = ["0"] * len(colours)
        not_empty = get_count_not_empty(current)
        for i in range(count_children + len(not_empty)):
            s[i] = "1"
        s = "".join(s)
        for p in it.permutations(s):
            child_colours = get_colours(p)
            res = {}
            for i, v in enumerate(convert_k):
                if v in not_empty:
                    child_colours[i].append(default_colour)
                    res[v] = child_colours[i]
                else:
                    res[v] = [default_colour]
            for i in range(len(not_empty), count_children):
                res[convert_children[i - len(not_empty)]] = child_colours[i]
            yield res


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
        if color == None:
            default_color = colours[0]
            colours = colours[1:]
        else:
            default_color = color

        for k in range(2, len(g.data[v])+1):
            s = ["0"] * len(g.data[v])
            for i in range(k):
                s[i] = "1"
            s = "".join(s)
            for p in it.permutations(s):
                convert_k = []
                convert_children = []
                for i, val in enumerate(list(p)):
                    if val == "1":
                        convert_k.append(g.data[v][i])
                    else:
                        convert_children.append(g.data[v][i])
                for res in get_all_split(default_color, colours, convert_k, convert_children):
                    for k, val in res.items():
                        if default_color in val:
                            F(g, k, colours, answer, default_color)
                            G(g, k, colours, answer, default_color)
                        else:
                            F(g, k, colours, answer, default_color)
                            H(g, k, colours, answer)


def G(g, v, colours, answer, color=None):
    if len(g.data[v]) == 0:
        return

    if color == None:
        default_color = colours[0]
        colours = colours[1:]
    else:
        default_color = color

    for i, ch in enumerate(g.data[v]):
        s = ["0"] * (len(colours) - 1)
        s[0] = "1"
        convert_k = [ch]
        convert_children = []
        for j in g.data[v]:
            if j != ch:
                convert_children.append(j)
        for res in get_all_split(default_color, colours, convert_k, convert_children):
            for k, val in res.items():
                if default_color in val:
                    F(g, k, colours, answer, default_color)
                    G(g, k, colours, answer, default_color)
                else:
                    F(g, k, colours, answer, default_color)
                    H(g, k, colours, answer)

        # if color is None:
        #     G(g, ch, colours, answer, colours[0])
        #     F(g, ch, colours, answer, colours[0])
        # else:
        #     G(g, ch, colours, answer, color)
        #     F(g, ch, colours, answer, color)
        # for i in g.data[v]:
        #     if i != ch:
        #         if not color is None:
        #             H(g, v, answer, colours[1:])
        #             F(g, v, colours, answer, colours[0])
        #         else:
        #             H(g, v, answer, colours)
        #             F(g, v, colours, answer, color)


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
    answer = {}
    F(g, 0, colours, answer)
    G(g,0, colours, answer)
    H(g,0, answer, colours)
    print(len(list(answer.values())[0]))

