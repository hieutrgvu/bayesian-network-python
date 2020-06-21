from digraph import *


class BayesNode(VertexNode):
    def __init__(self, data, parent_lst, val_dict, val_table):
        super().__init__(data)
        self.parent_lst = parent_lst
        self.val_dict = val_dict
        self.val_table = val_table


class BayesGraph(DiGraph):
    def __init__(self):
        super().__init__()

    def add(self, vertex, parent_lst, val_dict, val_table):
        self.node_list.append(BayesNode(vertex, parent_lst, val_dict, val_table))
