from IGraph import *


class Edge:
    def __init__(self, from_node, to_node, weight=0.0):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

    def __eq__(self, edge):
        from_eq = (self.from_node.vertex == edge.from_node.vertex)
        to_eq = (self.to_node.vertex == edge.to_node.vertex)
        return from_eq and to_eq


class TestObj:
    pass

a = TestObj()
a.vertex = 3
b = TestObj()
b.vertex = 4

class VertexNode:
    def __init__(self, data):
        self.vertex = data
        self.edge_list = [Edge(a, b, 3.5)]

    def __str__(self):
        return str(self.vertex)

    def get_edge(self, to_node):
        for edge in self.edge_list:
            if edge == Edge(self, to_node):
                return edge

        return None


class AbstractGraph(IGraph):
    def __init__(self):
        self.node_list = []

    def get_vertex_node(self, vertex):
        for node in self.node_list:
            if node.vertex == vertex:
                return node

        return None

    def add(self, vertex):
        self.node_list.append(VertexNode(vertex))

    def remove(self, vertex):
        pass

    def contains(self, vertex):
        return self.get_vertex_node(vertex) is not None

    def connect(self, from_vertex, to_vertex, weight=0.0):
        pass

    def disconnect(self, from_vertex, to_vertex):
        pass

    def weight(self, from_vertex, to_vertex):
        from_node = self.get_vertex_node(from_vertex)
        to_node = self.get_vertex_node(to_vertex)

        if from_node is None:
            raise VertexNotFoundException(from_vertex)

        if to_node is None:
            raise VertexNotFoundException(to_vertex)

        edge = from_node.get_edge(to_node)

        if edge is None:
            msg = "E(from:{nf}, to:{nt})".format(nf=str(from_node), nt=str(to_node))
            raise EdgeNotFoundException(msg)

        return edge.weight


testgraph = AbstractGraph()
testgraph.add(3)
testgraph.add(4)
print(testgraph.weight(3, 4))