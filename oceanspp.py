import math
from matplotlib import pyplot as plt

class Graph:
    
    def __init__(self, graph_dict={}):
        self.__graph_dict = graph_dict

    def add_vertex(self, vertex):
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def vertices(self):
        return self.__graph_dict.keys()

    def edges(self):
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {vertex, neighbour} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    #maybe do it as vertex_neighbours?
    def vertex_edges(self, vertex):
        edges = []
        for v in self.__graph_dict[vertex]:
            edges.append((vertex, v))
        return edges

    def remove_edge(self, vertex, edge):
        self.__graph_dict[vertex].remove(edge[1])

    def __str__(self):
        res = "vertices: "
        for vertex in self.__graph_dict:
            res += str(vertex) + " "
        res += "\nedges: "
        for edge in self.edges():
            res += str(edge) + " "
        return res

def edge_distance(vertex1, vertex2):
    return math.sqrt((vertex2[0] - vertex1[0])**2 + (vertex2[1] - vertex1[1])**2)

def shortest_path(graph, ship, port):
    visited = []
    not_visited = graph.vertices()
    not_visited.append(ship)
    distance = {v:9999 for v in not_visited}
    distance[port] = 0

    #Calculate distances
    v = None
    ship_edges = []
    while v != ship:
        min_value = 9999
        for d in not_visited:
            if distance[d] < min_value:
                min_value = distance[d]
                v = d
        visited.append(v)
        not_visited.remove(v)
        if distance[v] + edge_distance(v, ship) < distance[ship]:
            # if visibility between node v and ship:
            if v == (8.0, 6.0) or v == (10.0, 1.5):
                graph.add_edge((v, ship))
                ship_edges.append((ship, v))
            for edge in graph.vertex_edges(v):
                v2 = edge[1]
                if distance[v2] > distance[v] + edge_distance(v, v2):
                    distance[v2] = distance[v] + edge_distance(v, v2)

    #Find the shortest path
    path = [ship]
    min_value = 9999
    v = None
    for edge in ship_edges:
        if distance[edge[1]] + edge_distance(edge[0], edge[1]) < min_value:
            min_value = distance[edge[1]] + edge_distance(edge[0], edge[1])
            v = edge[1]
    path.append(v)

    while v != port:
        min_value = 9999
        min_edge = None
        for edge in graph.vertex_edges(v):
            if distance[edge[1]] < min_value:
                min_value = distance[edge[1]]
                min_edge = edge
        graph.remove_edge(min_edge[1], (min_edge[1], min_edge[0]))
        path.append(min_edge[1])
        v = min_edge[1]
    return path

if __name__ == "__main__":

    #These are the obstacles that will eventually be shorelines
    obstacle_a = { (1.0, 2.0) : [(4.0, 2.5), (1.0, 8.0)],
                  (4.0, 2.5) : [(1.0, 2.0), (5.0, 3.0)],
                  (5.0, 3.0) : [(4.0, 2.5), (4.5, 5.0)],
                  (4.5, 5.0) : [(5.0, 3.0), (3.0, 5.0)],
                  (3.0, 5.0) : [(4.5, 5.0), (3.0, 7.0)],
                  (3.0, 7.0) : [(3.0, 5.0), (4.0, 7.0)],
                  (4.0, 7.0) : [(3.0, 7.0), (4.0, 8.0)],
                  (4.0, 8.0) : [(4.0, 7.0), (1.0, 8.0)],
                  (1.0, 8.0) : [(1.0, 2.0), (4.0, 8.0)]
                }
    obstacle_b = { (6.0, 1.0) : [(7.0, 2.0), (10.0,1.5)],
                  (7.0, 2.0) : [(6.0, 1.0), (8.0, 6.0)],
                  (8.0, 6.0) : [(7.0, 2.0), (10.0,1.5)],
                  (10.0, 1.5) : [(8.0, 6.0), (6.0, 1.0)]
                }

    obstacles = [Graph(obstacle_a), Graph(obstacle_b)]

    #TODO: This is the operating network
    op_graph = { (1.0, 2.0) : [(4.0, 2.5), (1.0, 8.0), (6.0, 1.0)], #A
                 (4.0, 2.5) : [(1.0, 2.0), (5.0, 3.0)], #B
                 (5.0, 3.0) : [(4.0, 2.5), (6.0, 1.0), (8.0, 6.0), (4.5, 5.0)], #C
                 (4.5, 5.0) : [(5.0, 3.0), (4.0, 8.0), (6.0, 1.0)], #D
                 (4.0, 8.0) : [(4.5, 5.0), (1.0, 8.0), (4.0, 7.0), (8.0, 6.0)], #E
                 (1.0, 8.0) : [(1.0, 2.0), (4.0, 8.0)], #F
                 (6.0, 1.0) : [(1.0, 2.0), (5.0, 3.0), (4.5, 5.0), (8.0, 6.0), (10.0, 1.5)], #G
                 (8.0, 6.0) : [(5.0, 3.0), (4.0, 8.0), (6.0, 1.0), (10.0, 1.5)], #H
                 (10.0, 1.5) : [(8.0, 6.0), (6.0, 1.0)], #I
                 (4.0, 7.0) : [(4.0, 8.0)] #J
                }
    
    op_network = Graph(op_graph)
    
    #Run shortest path algorithm
    port = (1.0, 2.0)
    ship = (10.0, 5.5)
    shortest = shortest_path(op_network, ship, port)

    #Draw the obstacles and operating network
    fig = plt.figure(1, figsize=(5,5), dpi=90)
    ax = fig.add_subplot(111)

    #TODO: Make a function for drawing edges
    #Draw the obstacles
    for obstacle in obstacles:
        for edge in obstacle.edges():
            x = []
            y = []
            for vertex in edge:
                x.append(vertex[0])
                y.append(vertex[1])
            ax.plot(x, y, color='blue', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

    #Draw the operating network
    for edge in op_network.edges():
        x = []
        y = []
        for vertex in edge:
            x.append(vertex[0])
            y.append(vertex[1])
        ax.plot(x, y, color='red', alpha=0.7, linewidth=1)

    #draw shortest path
    x,y = zip(*shortest)
    ax.plot(x, y, color='green', alpha=0.7, linewidth=2)
    
    ax.set_title("ocean shortest path test")
    xrange = [0, 11]
    yrange = [0, 9]
    ax.set_xlim(*xrange)
    ax.set_xticks(range(*xrange) + [xrange[-1]])
    ax.set_ylim(*yrange)
    ax.set_yticks(range(*yrange) + [yrange[-1]])
    ax.set_aspect(1)
    fig.savefig("poly.png")
