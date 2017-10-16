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

    def add_edge(self, a, b):
        self.data[a].append(b)
        self.inverse_data[b].append(a)

    def add_color(self, n, c):
        self.colors[n] = c
        if c > self.max_color:
            self.max_color = c

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
        return str(list(self.R[v])).replace("[", "a").replace("]", "").replace(",","_").replace(" ","")

    def write_dfs(self, v, f):
        colour_v = self.get_color(v)
        if colour_v != "":
            f.write(str(v) + colour_v + "\n")

        for t in self.data[v]:
            f.write(str(v) + "->" + str(t) + ";\n")
            self.write_dfs(t, f)

    def write_fitch_step1(self, v, f):
        colour_v = self.get_color(v)
        label_v = self.get_label(v)
        if colour_v != "":
            f.write("a"+str(v) + label_v + colour_v + "\n")

        for t in self.data[v]:
            label_t = self.get_label(t)
            f.write("a"+str(v) + label_v + "->" + "a"+str(t) + label_t + ";\n")
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
            if not self.colors[v] == -1:
                self.R[v] = {self.colors[v]}
            else:
                self.R[v] = {1}
            return
        for k in self.data[v]:
            self.fitch_step1(k)

        intersection = self.R[self.data[v][0]]
        for k in self.data[v]:
            intersection = intersection.intersection(self.R[k])
        if len(intersection) == 0:
            res = set()
            for k in self.data[v]:
                res = res.union(self.R[k])
            self.R[v] = res
        else:
            self.R[v] = intersection

    def fitch_step2(self, v, parent):
        if self.colors[parent] in self.R[v]:
            self.colors[v] = self.colors[parent]
        else:
            self.colors[v] = list(self.R[v])[0]
        for t in self.data[v]:
            self.fitch_step2(t, v)
