class ItemNotFoundException(BaseException):
    def __init__(self, item_info):
        self.itemInfo = item_info

    def __str__(self):
        return 'The following vertex is not found: ' + str(self.itemInfo)


class VertexNotFoundException(ItemNotFoundException):
    def __init__(self, item_info):
        super().__init__(item_info)


class EdgeNotFoundException(ItemNotFoundException):
    def __init__(self, item_info):
        super().__init__(item_info)


class IfGraph:
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

    def get_outward_edges(self, from_vertex):
        pass

    def get_inward_edges(self, to_vertex):
        pass

    def iterator(self):
        pass

    def size(self):
        pass

    def in_degree(self, vertex):
        pass

    def out_degree(self, vertex):
        pass
