import itertools as it


def get_count_leaves(g):
    res = 0
    for k in g.data:
        if len(k) == 0:
            res += 1
    return res


def get_colours(s, colours):
    res = []
    cur = []
    for i, v in enumerate(list(s)):
        cur.append(colours[i])
        if v == "1":
            res.append(cur)
            cur = []
    return res


def get_count_not_empty(current):
    res = {}
    for i, v in enumerate(list(current)):
        if v == "1":
            res[i] = len(res)
    return res


def get_all_split(default_colour, colours, convert_k, convert_children):
    # 0 if set of colour is empty and need default colour
    count_children = len(convert_children)
    k = len(convert_k)
    default_colour = colours[0]
    for current in it.product("01", repeat=k):
        s = ["0"] * len(colours)
        not_empty = get_count_not_empty(current)
        # TODO add count_children > len(colors)
        for i in range(count_children + len(not_empty)):
            s[i] = "1"
        s = "".join(s)
        for p in set(it.permutations(s)):
            child_colours = get_colours(p, colours)
            res = {}
            for i, v in enumerate(convert_k):
                if i in not_empty:
                    res[v]=[default_colour].extend(child_colours[not_empty[i]])
                    # child_colours[not_empty[i]].append(default_colour)
                    # res[v] = child_colours[not_empty[i]]
                else:
                    res[v] = [default_colour]
            for i in range(len(not_empty), count_children):
                res[convert_children[i - len(not_empty)]] = child_colours[i]
            yield res


def cartes(colorings):
    res = []
    if len(colorings) == 2:
        # list[{}]
        for i in colorings[0]:
            for j in colorings[1]:
                z = i.copy()
                z.update(j)
                res.append(z)
        return res
    else:
        new_colorings = colorings[1:]
        tail_res = cartes(new_colorings)
        res = cartes([colorings[0], tail_res])
        return res

#TODO remove color
#TODO Combinations
def F(g, v, colours, color=None):
    if len(g.data[v]) == 0:
        if not color == None:
            return [{v: color}]
        else:
            return [{v: colours[0]}]
    else:
        if color == None:
            default_color = colours[0]
            colours = colours[1:]
        else:
            default_color = color
        all_coloring = []

        for k in range(2, len(g.data[v]) + 1):
            s = ["0"] * len(g.data[v])
            for i in range(k):
                s[i] = "1"
            s = "".join(s)
            for p in set(it.permutations(s)):
                convert_k = []
                convert_children = []
                for i, val in enumerate(list(p)):
                    if val == "1":
                        convert_k.append(g.data[v][i])
                    else:
                        convert_children.append(g.data[v][i])

                for res in get_all_split(default_color, colours, convert_k, convert_children):
                    current_coloring = []
                    for k, val in res.items():
                        if default_color in val:
                            f_col = F(g, k, colours, default_color)
                            g_col = G(g, k, colours, default_color)

                            f_or_g = f_col + g_col
                            current_coloring.append(f_or_g)

                        else:
                            f_col = F(g, k, colours, default_color)
                            h_col = H(g, k, colours)
                            f_or_h = f_col + h_col
                            current_coloring.append(f_or_h)
                    all_coloring.append(cartes(current_coloring))
        return all_coloring


def G(g, v, colours, color=None):
    if len(g.data[v]) == 0:
        return []

    if color == None:
        default_color = colours[0]
        colours = colours[1:]
    else:
        default_color = color

    all_coloring = []
    for i, ch in enumerate(g.data[v]):
        s = ["0"] * (len(colours) - 1)
        s[0] = "1"
        convert_k = [ch]
        convert_children = []
        for j in g.data[v]:
            if j != ch:
                convert_children.append(j)

        for res in get_all_split(default_color, colours, convert_k, convert_children):
            current_coloring = []
            for k, val in res.items():
                if default_color in val:
                    f_col = F(g, k, colours, default_color)
                    g_col = G(g, k, colours, default_color)

                    f_or_g = f_col + g_col
                    current_coloring.append(f_or_g)

                else:
                    f_col = F(g, k, colours, default_color)
                    h_col = H(g, k, colours)
                    f_or_h = f_col + h_col
                    current_coloring.append(f_or_h)
            all_coloring.append(cartes(current_coloring))
    return all_coloring


def H(g, v, colours):
    if len(g.data[v]) == 0:
        return []
    s = ["0"] * len(colours)
    for i in range(len(g.data[v])):
        s[i] = "1"
    s = "".join(s)
    all_coloring = []
    for p in set(it.permutations(s)):
        child_colours = get_colours(p, colours)
        current_coloring = []
        for i, v in enumerate(g.data[v]):
            h_col = H(g, v, child_colours[i])
            f_col = F(g, v, child_colours[i])
            f_or_h = f_col + h_col
            current_coloring.append(f_or_h)
        all_coloring.append(cartes(current_coloring))
    return all_coloring


def generate(g):
    count_colors = get_count_leaves(g)
    colours = [i for i in range(count_colors)]
    answer = {}
    F(g, 0, colours, answer)
    G(g, 0, colours, answer)
    H(g, 0, colours, answer)
    print(len(list(answer.values())[0]))
