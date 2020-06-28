import numpy as np
from digraph import *
import random


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
        self.forward_samples = np.array([0])
        self.likelihood_samples = {}  # For caching. Dictionary's keys is the proof.
        self.topo_dict = {}  # Updated in sample()

    def add(self, vertex, parent_lst, val_dict, val_table):
        self.node_dict[vertex] = BayesNode(vertex, parent_lst, val_dict, val_table)

    def check(self, var_dict):
        for key, value in var_dict.items():
            if key not in self.node_dict:
                raise BayesNetException("node test not existed in graph")

            node = self.node_dict.get(key)
            if value not in node.val_dict:
                raise BayesNetException("value not existed in graph")

    def infer_forward(self, var_infer_dict, var_proof_dict, sample_num=10 ** 6):
        # G = A; I = Cao, D = Kho
        # var_infer_dict = {"G": "A"}
        # var_proof_dict = {"I": "Cao", "D": "Kho"}
        self.check(var_infer_dict)
        self.check(var_proof_dict)
        samples = self.sample_forward(sample_num)

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
            proof_loc = np.where((samples[:, proof_mask] == proof_compare).all(axis=1))
            infer = np.where((samples[proof_loc[0][:, None], infer_mask] == infer_compare).all(axis=1))
            return infer[0].shape[0] / proof_loc[0].shape[0]
        else:
            infer = np.where((samples[:, infer_mask] == infer_compare).all(axis=1))
            return infer[0].shape[0] / samples.shape[0]

    def infer_likelihood(self, var_infer_dict, var_proof_dict, sample_num=10 ** 6):
        if not var_proof_dict:
            print("Inference with likelihood requires proof! Using forward sampling instead...")
            return self.infer_forward(var_infer_dict, var_proof_dict)

        self.check(var_infer_dict)
        self.check(var_proof_dict)
        samples = self.sample_likelihood(sample_num, var_proof_dict)

        infer_mask = []
        infer_compare = []
        for vertex, val in var_infer_dict.items():
            infer_mask.append(self.topo_dict[vertex])
            node = self.get_vertex_node(vertex)
            infer_compare.append(node.val_dict[val])

        infer_loc = np.where((samples[:, infer_mask] == infer_compare).all(axis=1))
        likelihood_val = np.ones(samples.shape[0])

        for vertex in var_proof_dict.keys():
            node = self.get_vertex_node(vertex)
            var_lookup = [self.topo_dict[v] for v in node.parent_lst]
            var_lookup.append(self.topo_dict[node.vertex])
            var_samples = samples[:, var_lookup]
            var_unique = np.unique(var_samples, axis=0)

            for sample in var_unique:
                loc = np.where((var_samples == sample).all(axis=1))
                likelihood_val[loc[0]] *= node.distribution[tuple(sample)]

        return np.sum(likelihood_val[infer_loc[0]]) / np.sum(likelihood_val)

    def sample_forward(self, sample_num):
        if self.forward_samples.shape[0] == sample_num:
            return self.forward_samples

        random.seed(0)
        sample_lst = []
        sorter = TopoSorter(self)
        topo_lst = sorter.sort()
        self.topo_dict = {vertex: vertex_idx for vertex_idx, vertex in enumerate(topo_lst)}

        for i in range(sample_num):
            sample_val = []
            for vertex in topo_lst:
                sample_val.append(self.roll(vertex, sample_val))
            sample_lst.extend(sample_val)

        self.forward_samples = np.array(sample_lst).reshape(sample_num, -1)
        return self.forward_samples

    def sample_likelihood(self, sample_num, proof):
        if frozenset(proof) in self.likelihood_samples:
            return self.likelihood_samples[frozenset(proof)]

        random.seed(0)
        sample_lst = []
        sorter = TopoSorter(self)
        topo_lst = sorter.sort()
        self.topo_dict = {vertex: vertex_idx for vertex_idx, vertex in enumerate(topo_lst)}

        for i in range(sample_num):
            sample_val = []
            for vertex in topo_lst:
                if vertex in proof:
                    sample_val.append(self.get_vertex_node(vertex).val_dict[proof[vertex]])
                else:
                    sample_val.append(self.roll(vertex, sample_val))
            sample_lst.extend(sample_val)

        self.likelihood_samples[frozenset(proof)] = np.array(sample_lst).reshape(sample_num, -1)
        return self.likelihood_samples[frozenset(proof)]

    def roll(self, vertex, prev_vertex_val):
        node = self.get_vertex_node(vertex)
        pa_idx = [self.topo_dict[vertex] for vertex in node.parent_lst]

        if pa_idx:
            pa_val = tuple(prev_vertex_val[idx] for idx in pa_idx)
            p_val = node.distribution[pa_val]
        else:
            p_val = node.distribution

        rand_val = random.uniform(0, 1)
        for idx in range(p_val.shape[0]):
            rand_val -= p_val[idx]
            if rand_val < 0:
                return idx

        raise BayesNetException("Cannot sampling!")
