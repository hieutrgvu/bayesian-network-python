from ifgraph import *


class Edge:
    def __init__(self, from_node, to_node, weight=0.0):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

    def __eq__(self, edge):
        from_eq = (self.from_node.vertex == edge.from_node.vertex)
        to_eq = (self.to_node.vertex == edge.to_node.vertex)
        return from_eq and to_eq

    def __str__(self):
        return "E(from:{}, to: {}): ".format(str(self.from_node), str(self.to_node))


class VertexNode:
    def __init__(self, data):
        self.vertex = data
        self.in_degree = 0
        self.out_degree = 0
        self.edge_list = []

    def connect(self, to_node, weight=0.0):
        edge = self.get_edge(to_node)
        if edge is None:
            edge = Edge(self, to_node, weight)
            self.edge_list.append(edge)
            edge.from_node.out_degree += 1
            edge.to_node.in_degree += 1
        else:
            edge.weight = weight

    def get_edge(self, to_node):
        for edge in self.edge_list:
            if edge == Edge(self, to_node):
                return edge

        return None

    def get_outward_edges(self):
        return [edge.to_node.vertex for edge in self.edge_list]

    def remove_to(self, to_node):
        for edge in self.edge_list:
            if edge.to_node.vertex == to_node.vertex:
                self.edge_list.remove(edge)
                edge.from_node.out_degree -= 1
                edge.to_node.in_degree -= 1
                break

    def __str__(self):
        msg = "V({}, in:{}, out:{})".format(str(self.vertex), self.in_degree, self.out_degree)
        return msg


class AbstractGraph(IfGraph):
    def __init__(self):
        self.node_dict = {}

    def get_vertex_node(self, vertex):
        return self.node_dict.get(vertex)

    def add(self, vertex):
        self.node_dict[vertex] = VertexNode(vertex)

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

    def get_outward_edges(self, from_vertex):
        node = self.get_vertex_node(from_vertex)
        if node is None:
            raise VertexNotFoundException(from_vertex)

        return node.get_outward_edges()

    def get_inward_edges(self, to_vertex):
        vertex_list = []
        for node in self.node_dict.values():
            for edge in node.edge_list:
                if edge.to_node.vertex == to_vertex:
                    vertex_list.append(edge.from_node.vertex)

        return vertex_list

    def size(self):
        return len(self.node_dict)

    def in_degree(self, vertex):
        node = self.get_vertex_node(vertex)
        if node is None:
            raise VertexNotFoundException(vertex)

        return node.in_degree

    def out_degree(self, vertex):
        node = self.get_vertex_node(vertex)
        if node is None:
            raise VertexNotFoundException(vertex)

        return node.out_degree

    def __str__(self):
        desc = "===========================================\n"
        desc += "Vertices:\n"
        for node in self.node_dict.values():
            desc += "  " + str(node) + "\n"

        desc += "-------------------------------------------\n"
        desc += "Edges:\n"
        for node in self.node_dict.values():
            for edge in node.edge_list:
                line = "E({}, {}, {})".format(str(node.vertex), edge.to_node.vertex, edge.weight)
                desc += "  " + line + "\n"

        desc += "==========================================="

        return desc

    def __iter__(self):
        iter_graph = []
        for value in self.node_dict.values():
            iter_graph.append(value)

        self.iter_graph = iter_graph
        return self

    def __next__(self):
        if len(self.iter_graph) > 0:
            return self.iter_graph.pop(0).vertex
        else:
            raise StopIteration
