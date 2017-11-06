from collections import Counter


class Graph:
    def __init__(self, vertex=0):
        self.count_loop = -1
        if vertex > 0:
            self.colors = [-1] * vertex
            self.data = []
            self.inverse_data = []
            self.R = []
            self.start_loop = [0] * vertex
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

    def write_fitch_step1(self, v, f, used):
        if used[v] == -1:
            used[v] = 1
        else:
            return
        colour_v = self.get_color(v)
        label_v = self.get_label(v)
        if colour_v != "":
            f.write("a" + str(v) + label_v + colour_v + "\n")

        for t in self.data[v]:
            label_t = self.get_label(t)
            f.write("a" + str(v) + label_v + "->" + "a" + str(t) + label_t + ";\n")
            self.write_fitch_step1(t, f, used)

    def is_tree(self):
        used = [False] * len(self.data)
        self.dfs(self.root, used)
        for v in used:
            if not v:
                return False
        return True

    def count_colours(self, counter):
        res = 0
        for number, count in counter.items():
            if number == 1:
                res += count
            else:
                res += 1
        return res

    def fitch(self):
        self.fitch_step1(self.root,[-1] * len(self.colors))
        self.fitch_step2(self.root, self.root)

    def fitch_step1(self, v, used):
        if used[v] == -1:
            used[v] = 1
        else:
            return
        if len(self.data[v]) == 0:
            self.R[v] = {self.colors[v]: 1}
            return
        for k in self.data[v]:
            self.fitch_step1(k, used)

        intersection = {}
        has_leaf = set()
        diff_counter = {}
        # intersection = Counter()
        for k in self.data[v]:
            for colour, count in self.R[k].items():
                if len(self.inverse_data[k]) > 1:
                    if self.start_loop[k] == 0:
                        self.count_loop -= 1
                        count = self.count_loop
                        self.start_loop[k] = count
                    else:
                        count = self.start_loop[k]

                if colour in diff_counter:
                    diff_counter[colour].update([count])
                else:
                    diff_counter[colour] = Counter([count])

                if colour in intersection:
                    if count == 1:
                        if not colour in has_leaf:
                            has_leaf.add(colour)
                            intersection[colour] = 1
                    else:
                        intersection[colour] = count
                else:
                    intersection[colour] = count
                    if count == 1:
                        has_leaf.add(colour)

        # Ровно один цвет присутствует
        if len(diff_counter) == 1:
            k = list(diff_counter.keys())[0]
            if len(diff_counter[k]) > 1:
                self.R[v] = {k: 1}
            else:
                self.R[v] = {k: diff_counter[k].most_common(1)[0]}
        else:
            sort = sorted(diff_counter.items(), key=lambda x: self.count_colours(x[1]),reverse=True)
            most_common_colours = sort[0:2]
            if self.count_colours(most_common_colours[1][1]) > 1:
                print("for vertex v=" + str(v) + "found more 2 colours" + str(most_common_colours))
                exit(-1)

            # Есть два поддерева в которых один и тот же цвет
            elif self.count_colours(most_common_colours[0][1]) > 1:
                self.R[v] = {most_common_colours[0][0]: 1}
            else:
                cur = {}
                for col, counter in diff_counter.items():
                    count = counter.most_common(1)[0][0]
                    cur[col] = count
                self.R[v] = cur

    def fitch_step2(self, v, parent):
        if self.colors[parent] in self.R[v]:
            self.colors[v] = self.colors[parent]
        else:
            if len(self.R[v]) == 1 and self.need_colors[list(self.R[v])[0]] == 2:
                self.colors[v] = list(self.R[v])[0]
        for t in self.data[v]:
            self.fitch_step2(t, v)
