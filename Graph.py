class Vertex:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, vertex):
        self.adjacency_list[vertex] = []

    def add_directed_edge(self, start, end, weight):
        self.edge_weights[(start, end)] = weight
        if start != end:
            self.adjacency_list[start].append(end)

# Radix sort algorithm to sort adjacency list in ascending order by distance.
    def sort_adjacency_list(self, vertex):
        n = len(self.adjacency_list[vertex])
        bins = [[]]*10
        for i in range(3):
            for j in range(n):
                e = int((self.edge_weights[(vertex, self.adjacency_list[vertex][j])] * 10 / pow(10,i)) % 10)
                if len(bins[e]) > 0:
                    bins[e].append(self.adjacency_list[vertex][j])
                else:
                    bins[e] = [self.adjacency_list[vertex][j]]
            k = 0
            for x in range(10):
                if len(bins[x]) > 0:
                    for y in range(len(bins[x])):
                        self.adjacency_list[vertex][k] = bins[x].pop(0)
                        k += 1
