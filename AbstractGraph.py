from IGraph import IGraph
from IGraph import ItemNotFoundException


# VertexNode ...
class VertexNode:
    inDegree: int = 0
    outDegree: int = 0
    adList: list

    def __init__(self, data):
        self.vertex = data
        self.inDegree = self.outDegree = 0
        # save list of edge
        self.adList = []

    def connect(self, to_vertex, weight=0):
        edge = self.getEdge(to_vertex)
        if edge is None:
            edge = Edge(self, to_vertex, weight)
            self.adList.append(edge)
            edge.from_vertex.outDegree += 1
            edge.to_vertex.inDegree += 1
        else:
            edge.weight = weight

    def getOutwardEdges(self):
        list = []
        for it in self.adList:
            it_to_vertex = it.to_vertex.vertex
            list.append(it_to_vertex)
        return list

    def getEdge(self, to_vertex):
        edgeIt = self.adList
        for edge in edgeIt:
            if edge == to_vertex:
                return edge

        return None

    def removeTo(self, to_vertex):
        edgeIt = self.adList
        for edge in edgeIt:
            if edge.to_vertex.vertex == to_vertex.vertex:
                self.adList.remove(edge)
                edge.from_vertex.outDegree -= 1
                edge.to_vertex.inDegree -= 1
                break;

    def inDegree(self):
        return self.inDegree

    def outDegree(self):
        return self.outDegree

    def toString(self):
        desc = "V(%s, in:%s, out:%s)", self.vertex, self.inDegree, self.outDegree
        return desc;


# Edge...
class Edge:
    from_vertex: VertexNode
    to_vertex: VertexNode
    weight: float = 0

    def __init__(self, from_vertex: VertexNode, to_vertex: VertexNode, weight: float = 0):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight

    def equals(self, newEdge):
        if self.from_vertex == newEdge.from_vertex:
            fromEquality = True
        if self.to_vertex == newEdge.to_vertex:
            toEquality = True
        return fromEquality and toEquality

    def toString(self):
        message = "E(from:%s, to:%s)", self.from_vertex, self.to_vertex
        return message


class AbstractGraph(IGraph, ItemNotFoundException):
    # list of vertexNode
    nodeList: list

    def __init__(self):
        self.nodeList = []

    def getVertexNode(self, vertex: VertexNode):
        it = self.nodeList
        for node in it:
            if node.vertex == vertex:
                return node

        return None

    def add(self, vertex: VertexNode):
        self.nodeList.append(vertex)

    def remove(self, vertex: VertexNode):
        pass

    def contains(self, vertex: VertexNode):
        node = self.getVertexNode(vertex)
        if node is None:
            return False
        return True

    def connect(self, from_t, to_t, weight: float = 0):
        pass

    def disconnect(self, from_t, to_t):
        pass

    # must be refactor
    def weight(self, from_t, to_t):
        nodeF = self.getVertexNode(from_t)
        nodeT = self.getVertexNode(to_t)
        if nodeF is None:
            return 0

        if nodeT is None:
            return 0

        edge = nodeF.getEdge(nodeT)
        if edge is None:
            return 0

        return edge.weight
