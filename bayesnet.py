import numpy as np
from digraph import *


class BayesNetException(BaseException):
    def __init__(self, item_info):
        self.itemInfo = item_info

    def __str__(self):
        return 'Bayesian Network Error: ' + str(self.itemInfo)


class BayesNode(VertexNode):
    def __init__(self, data, parent_lst, val_dict, distribution):
        super().__init__(data)
        self.parent_lst = parent_lst
        self.val_dict = val_dict
        self.distribution = distribution


class BayesNet(DiGraph):
    def __init__(self):
        super().__init__()
        self.sample_arr = []  # will be convert to numpy array later
        self.topo_dict = {}  # Updated in sample()

    def add(self, vertex, parent_lst, val_dict, val_table):
        self.node_list.append(BayesNode(vertex, parent_lst, val_dict, val_table))

    def check(self):
        pass

    def infer(self, var_infer_dict, var_proof_dict):
        self.var_infer_dict = var_infer_dict
        self.var_proof_dict = var_proof_dict
        self.check()

    def sample(self, sample_num):
        np.random.seed(0)

        sorter = TopoSorter(self)
        topo_lst = sorter.sort()
        self.topo_dict = {vertex: vertex_idx for vertex_idx, vertex in enumerate(topo_lst)}

        for i in range(sample_num):
            sample_val = []
            for vertex in topo_lst:
                sample_val.append(self.roll(vertex, sample_val))
            self.sample_arr.extend(sample_val)

        self.sample_arr = np.array(self.sample_arr).reshape(sample_num, -1)

    def roll(self, vertex, prev_vertex_val):
        node = self.get_vertex_node(vertex)
        pa_idx = [self.topo_dict[vertex] for vertex in node.parent_lst]

        if pa_idx:
            pa_val = tuple(prev_vertex_val[idx] for idx in pa_idx)
            p_val = node.distribution[pa_val]
        else:
            p_val = node.distribution

        # return np.random.choice(p_val.shape[0], p=p_val) # slow???
        rand_val = np.random.uniform()
        for idx in range(p_val.shape[0]):
            rand_val -= p_val[idx]
            if rand_val < 0:
                return idx

        raise BayesNetException("Cannot sampling!")
