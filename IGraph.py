class ItemNotFoundException(BaseException):
    def __init__(self, itemInfo):
        self.itemInfo = itemInfo

    def __str__(self):
        return 'The following vertex is not found: ' + str(self.itemInfo)


class VertexNotFoundException(ItemNotFoundException):
    def __init__(self, itemInfo):
        super(VertexNotFoundException, self).__init__(itemInfo)


class EdgeNotFoundException(ItemNotFoundException):
    def __init__(self, itemInfo):
        super(EdgeNotFoundException, self).__init__(itemInfo)


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
