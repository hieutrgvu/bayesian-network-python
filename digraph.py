from abgraph import *


class DiGraph(AbstractGraph):
    def __init__(self):
        super().__init__()

    def connect(self, from_vertex, to_vertex, weight=0.0):
        from_node = self.get_vertex_node(from_vertex)
        to_node = self.get_vertex_node(to_vertex)

        if from_node is None or to_node is None:
            raise VertexNotFoundException(from_vertex)

        from_node.connect(to_node, weight)

    def disconnect(self, from_vertex, to_vertex):
        from_node = self.get_vertex_node(from_vertex)
        to_node = self.get_vertex_node(to_vertex)

        if from_node is None or to_node is None:
            raise VertexNotFoundException(from_vertex)

        edge = from_node.get_edge(to_node)
        if edge is None:
            msg = "E(from:{}, to:{})".format(str(from_node), str(to_node))
            raise EdgeNotFoundException(msg)

        from_node.remove_to(to_node)

    def remove(self, vertex):
        del_node = self.get_vertex_node(vertex)
        if del_node is None:
            raise VertexNotFoundException(vertex)

        for node in self.node_list:
            if node.get_edge(del_node) is not None:
                node.remove_to(del_node)

            if del_node.get_edge(node) is not None:
                del_node.remove_to(node)

        self.node_list.remove(del_node)


class TopoSorter:
    def __init__(self, graph):
        self.graph = graph

    def sort(self):
        # BFS sort
        topo_order = []
        in_degree_map = {vertex: self.graph.in_degree(vertex) for vertex in self.graph}
        topo_queue = [v for (v, in_degree) in in_degree_map.items() if in_degree == 0]

        while len(topo_queue) != 0:
            vertex = topo_queue.pop(0)
            topo_order.append(vertex)
            neighbors = self.graph.get_outward_edges(vertex)
            for v in neighbors:
                in_degree_map[v] -= 1
                if in_degree_map[v] == 0:
                    topo_queue.append(v)

        return topo_order
