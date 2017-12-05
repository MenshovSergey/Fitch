from collections import Counter
from sympy import Poly, S
from sympy.abc import a, x, y

class Graph:
    def __init__(self, vertex=0):
        if vertex > 0:
            self.colors = [-1] * vertex
            self.data = []
            self.inverse_data = []
            self.R = []
            self.bad = []
            self.F = {}
            self.H = {}
            self.G = {}
            for i in range(vertex):
                self.data.append([])
                self.inverse_data.append([])
                self.R.append(set())
                self.bad.append(set())
        else:
            self.data = []
            self.colors = []
            self.inverse_data = []
            self.R = []
            self.bad = []
        self.root = -1
        self.max_color = -1
        self.need_colors = {}

    def add_edge(self, a, b):
        self.data[a].append(b)
        self.inverse_data[b].append(a)

    def add_vertex(self):
        self.data.append([])
        self.R.append(set())
        self.bad.append(set())
        self.inverse_data.append([])
        self.colors.append(-1)

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
        return str(list(self.R[v])).replace("[", "a").replace("]", "").replace(",","_").replace(" ","")

    def write_dfs_start(self,v,f):
        self.write_dfs(v,f,[-1] * len(self.colors))

    def write_dfs(self, v, f,used):
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

    def find_forgot_colour(self, bad_counter, current_colour, v):
        if current_colour in bad_counter:
            bad_counter.pop(current_colour)
        most_common = bad_counter.most_common(1)
        if len(most_common) > 0 and most_common[0][1] > 1:
            print("for vertex v = " +str(v)+" found 2 colours " + str(bad_counter.most_common(1)[0]))
            exit(-1)

    def add_bad_vertex(self, v, c, intersection):
        for k in intersection:
             if k != c:
                self.bad[v].add(k)

    def calculate(self, v):
        if len(self.data[v]) == 0:
            self.F[v] = x.as_poly(x)
            self.H[v] = (x-x).as_poly(x)
            self.G[v] = (x-x).as_poly(x)
        else:
            for k in self.data[v]:
                self.calculate(k)
            self.H[v] = (x**0).as_poly(x)
            for i in self.data[v]:
                self.H[v] = self.H[v] * (self.F[i]+ self.H[i])

            self.G[v] = (x-x).as_poly(x)
            for i in self.data[v]:
                c = self.F[i] + self.G[i]
                for j in self.data[v]:
                    if i != j:
                        c = c * (self.F[j] + self.H[j])
                self.G[v] = self.G[v] + c
            self.F[v] = (x ** 0).as_poly(x)
            for i in self.data[v]:
                self.F[v] = self.F[v] * (self.F[i] + self.H[i] + (self.F[i] + self.G[i])/x)
            self.F[v] = x.as_poly(x) * self.F[v] - x.as_poly(x) * self.H[v] - self.G[v]

    def fitch(self):
        self.fitch_step1(self.root)
        self.fitch_step2(self.root, self.root)

    def fitch_step1(self, v):
        if len(self.data[v]) == 0:
            self.R[v] = {self.colors[v]}
            self.add_bad_vertex(v, -1,list(self.R[v]))
            return
        for k in self.data[v]:
            self.fitch_step1(k)
        intersection = Counter()
        bad_counter = Counter()
        for k in self.data[v]:
            intersection.update(list(self.R[k]))
            self.bad[v] = self.bad[v].union(self.bad[k])
            bad_counter.update(list(self.bad[k]))

        #Ровно один цвет присутствует
        if len(intersection) == 1:
            res = set(intersection.keys())
            c = intersection.most_common(1)[0][0]
            self.find_forgot_colour(bad_counter, c, v)
            self.add_bad_vertex(v, c, list(intersection.keys()))
            self.R[v] = res
        else:
            most_common_colours = intersection.most_common(2)
            if most_common_colours[1][1] > 1:
                print("for vertex v=" + str(v) + "found more 2 colours" + str(most_common_colours))
                exit(-1)
            #Есть два поддерева в которых один и тот же цвет
            elif most_common_colours[0][1] > 1:
                self.R[v] = {most_common_colours[0][0]}
                c = most_common_colours[0][0]
                self.find_forgot_colour(bad_counter, c, v)
                self.add_bad_vertex(v, c, intersection)
            else:
                self.R[v] = set(intersection.keys())
                self.add_bad_vertex(v, -1, list(intersection.keys()))
                self.find_forgot_colour(bad_counter,-1,v)

    def fitch_step2(self, v, parent):
        if self.colors[parent] in self.R[v]:
            self.colors[v] = self.colors[parent]
        else:
            if len(self.R[v]) == 1 and self.need_colors[list(self.R[v])[0]] == 2:
                self.colors[v] = list(self.R[v])[0]
        for t in self.data[v]:
            self.fitch_step2(t, v)
