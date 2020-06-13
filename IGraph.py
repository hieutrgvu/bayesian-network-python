class ItemNotFoundException:
    __itemInfo = None

    def __init__(self, itemInfo):
        self.__itemInfo = itemInfo

    def toString(self):
        message = "The following vertex is not found: %s", self.__itemInfo
        return message


class VertexNotFoundException(ItemNotFoundException):
    def VertexNotFoundException(self, vertexInfo):
        super().__init__(self, vertexInfo)


class EdgeNotFoundException(ItemNotFoundException):
    def EdgeNotFoundException(self, vertexInfo):
        super().__init__(self, vertexInfo)


class IGraph:
    def add(self, vertex):
        pass

    def remove(self, vertex):
        pass

    def contains(self, vertex):
        pass

    def connect(self, from_vertex, to_vertex):
        pass

    def connect(self, from_vertex, to_vertex, weight):
        pass

    def weight(self, from_vertex, to_vertex):
        pass

    def getOutwardEdges(self, from_vertex):
        pass

    def getInwardEdges(self, to_vertex):
        pass

    def iterator(self):
        pass

    def size(self):
        pass

    def inDegree(self, vertex):
        pass

    def outDegree(self, vertex):
        pass
