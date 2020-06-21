from abgraph import *
from bayes import *


class BayesGraph(AbstractGraph):
    def __init__(self):
        super().__init__()

    def add(self, bayes_node):
        self.node_list.append(bayes_node)
