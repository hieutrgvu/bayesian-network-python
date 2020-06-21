from abgraph import *


class BayesNode(VertexNode):
    def __init__(self, data):
        super().__init__(data)
        self.parent_list = []
        self.value_list = []
        self.table = []

    def get_parent_list(self):
        return self.parent_list

    def get_value_list(self):
        return self.value_list

    def get_table(self):
        return self.table

    def get_val_idx(self, val):
        return 0
