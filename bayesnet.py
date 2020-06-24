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
        self.sample_arr = np.array([0])  # will be convert to numpy array later
        self.topo_dict = {}  # Updated in sample()

    def add(self, vertex, parent_lst, val_dict, val_table):
        self.node_list.append(BayesNode(vertex, parent_lst, val_dict, val_table))

    def infer(self, var_infer_dict, var_proof_dict):
        pass

    def check(self, var_dict):
        pass

    def infer_forward(self, var_infer_dict, var_proof_dict, sample_num=10**6):
        # G = A; I = Cao, D = Kho
        # var_infer_dict = {"G": "A"}
        # var_proof_dict = {"I": "Cao", "D": "Kho"}
        self.check(var_infer_dict)
        self.sample(sample_num)

        proof_mask = []
        proof_compare = []
        for vertex, val in var_proof_dict.items():
            proof_mask.append(self.topo_dict[vertex])
            node = self.get_vertex_node(vertex)
            proof_compare.append(node.val_dict[val])

        infer_mask = []
        infer_compare = []
        for vertex, val in var_infer_dict.items():
            infer_mask.append(self.topo_dict[vertex])
            node = self.get_vertex_node(vertex)
            infer_compare.append(node.val_dict[val])

        if proof_mask:
            proof = np.where((self.sample_arr[:, proof_mask] == proof_compare).all(axis=1))
            infer = np.where((self.sample_arr[proof[0][:, None], infer_mask] == infer_compare).all(axis=1))
            return infer[0].shape[0] / proof[0].shape[0]
        else:
            infer = np.where((self.sample_arr[:, infer_mask] == infer_compare).all(axis=1))
            return infer[0].shape[0] / self.sample_arr.shape[0]

    def sample(self, sample_num):
        np.random.seed(0)
        sample_lst = []

        sorter = TopoSorter(self)
        topo_lst = sorter.sort()
        self.topo_dict = {vertex: vertex_idx for vertex_idx, vertex in enumerate(topo_lst)}

        for i in range(sample_num):
            sample_val = []
            for vertex in topo_lst:
                sample_val.append(self.roll(vertex, sample_val))
            sample_lst.extend(sample_val)

        self.sample_arr = np.array(sample_lst).reshape(sample_num, -1)

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
