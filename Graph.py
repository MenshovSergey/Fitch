from collections import Counter


class Graph:
    def __init__(self, vertex=0):
        if vertex > 0:
            self.colors = [-1] * vertex
            self.data = []
            self.inverse_data = []
            self.R = []
            for i in range(vertex):
                self.data.append([])
                self.inverse_data.append([])
                self.R.append(set())
        else:
            self.data = []
            self.colors = []
            self.inverse_data = []
            self.R = []
        self.root = -1
        self.max_color = -1
        self.need_colors = {}

    def add_edge(self, a, b):
        self.data[a].append(b)
        self.inverse_data[b].append(a)

    def add_color(self, n, c):
        self.colors[n] = c
        if c > self.max_color:
            self.max_color = c
        if c in self.need_colors:
            self.need_colors[c] = 2
        else:
            self.need_colors[c] = 1

    def find_root(self):
        used = [False] * len(self.data)
        for i in range(len(self.data)):
            for v in self.data[i]:
                used[v] = True
        for i, v in enumerate(used):
            if not v:
                self.root = i
                break
        return self.root

    def dfs(self, v, used):
        used[v] = True
        for t in self.data[v]:
            self.dfs(t, used)

    def get_color(self, v):
        if self.colors[v] != -1:
            c = self.colors[v] * 1.0 / self.max_color
            return " [style=filled,fillcolor=\"" + str(c) + " " + str(c) + " " + str(c) + "\"]"
        else:
            return ""

    def get_label(self, v):
        return str(list(self.R[v])).replace("[", "a").replace("]", "").replace(",", "_").replace(" ", "")

    def write_dfs_start(self, v, f):
        self.write_dfs(v, f, [-1] * len(self.colors))

    def write_dfs(self, v, f, used):
        if used[v] == -1:
            used[v] = 1
        else:
            return
        colour_v = self.get_color(v)
        if colour_v != "":
            f.write(str(v) + colour_v + "\n")

        for t in self.data[v]:
            f.write(str(v) + "->" + str(t) + ";\n")
            self.write_dfs(t, f, used)

    def write_fitch_step1(self, v, f):
        colour_v = self.get_color(v)
        label_v = self.get_label(v)
        if colour_v != "":
            f.write("a" + str(v) + label_v + colour_v + "\n")

        for t in self.data[v]:
            label_t = self.get_label(t)
            f.write("a" + str(v) + label_v + "->" + "a" + str(t) + label_t + ";\n")
            self.write_fitch_step1(t, f)

    def is_tree(self):
        used = [False] * len(self.data)
        self.dfs(self.root, used)
        for v in used:
            if not v:
                return False
        return True

    def fitch(self):
        self.fitch_step1(self.root)
        self.fitch_step2(self.root, self.root)

    def fitch_step1(self, v):
        if len(self.data[v]) == 0:
            self.R[v] = {self.colors[v]: 1}
            return
        for k in self.data[v]:
            self.fitch_step1(k)

        intersection = {}
        has_leaf = set()
        # intersection = Counter()
        for k in self.data[v]:
            for ch, count in self.R[k].items():
                if len(self.inverse_data[k]) > 1:
                    count = -1
                if ch in intersection:
                    if count == 1:
                        if not ch in has_leaf:
                            has_leaf.add(ch)
                            intersection[ch] = 1
                        else:
                            intersection[ch] += 1
                    else:
                        intersection[ch] = count
                else:
                    intersection[ch] = count
                    if count == 1:
                        has_leaf.add(ch)

        # Ровно один цвет присутствует
        if len(intersection) == 1:
            self.R[v] = intersection
        else:
            sort = sorted(intersection.items(), key=lambda x: abs(x[1]))
            most_common_colours = sort[0:2]
            if most_common_colours[1][1] > 1:
                print("for vertex v=" + str(v) + "found more 2 colours" + str(most_common_colours))
                exit(-1)
            # Есть два поддерева в которых один и тот же цвет
            elif most_common_colours[0][1] > 1:
                self.R[v] = {most_common_colours[0][0]}
            else:
                self.R[v] = intersection

    def fitch_step2(self, v, parent):
        if self.colors[parent] in self.R[v]:
            self.colors[v] = self.colors[parent]
        else:
            if len(self.R[v]) == 1 and self.need_colors[list(self.R[v])[0]] == 2:
                self.colors[v] = list(self.R[v])[0]
        for t in self.data[v]:
            self.fitch_step2(t, v)
