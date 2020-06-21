from bayesgraph import *
import numpy as np


class ErrorException(BaseException):
    def __init__(self, item_info):
        self.itemInfo = item_info

    def __str__(self):
        return 'Error exception case : ' + str(self.itemInfo)


class ErrorFormatFile(ErrorException):
    def __init__(self, item_info):
        super().__init__(item_info)


def read_file_model_input(name_file):
    f = open(name_file, "r")
    return f


def create_graph(data_file):
    bayes_graph = BayesGraph()
    count = 0

    for data_line in data_file:
        data_split = data_line.split(";")
        count += 1
        if count == 1:
            continue

        # node_bayes not existed
        if len(data_split[0]) == 0:
            raise ErrorFormatFile(data_line)

        bayes_node = BayesNode(data_split[0])

        if len(data_split[1]) > 0:
            parent_list = parent_list_parser(data_split[1])
            bayes_node.parent_list = parent_list

        if len(data_split[2]) > 0:
            value_list = value_list_parser(data_split[2])
            bayes_node.value_list = value_list

        if len(data_split[3]) > 0 and len(data_split[4]) > 0:
            table = table_parser(data_split[3], data_split[4])
            bayes_node.table = table

        bayes_graph.add(bayes_node)

    return connect_bayes_node(bayes_graph)


def parent_list_parser(parent_original):
    parent_list = parent_original.split(",")
    return parent_list


def value_list_parser(value_original):
    value_list = value_original.split(",")
    return value_list


def table_parser(shape_table_original, table_original):
    shape_table = shape_table_original.split(",")
    table_string = table_original.split(",")
    table_list = np.array(table_string).astype(np.float)
    tuple_shape_table = tuple(map(int, shape_table_original.split(',')))

    dimension_table = 1
    for i in tuple_shape_table:
        dimension_table = dimension_table * i

    # dimension reshape invalid
    if dimension_table != len(table_list):
        raise ErrorFormatFile(shape_table_original)

    table = np.reshape(table_list, tuple_shape_table)

    return table


def connect_bayes_node(bayes_graph):
    for bayes_node in bayes_graph.node_list:
        if len(bayes_node.parent_list) > 0:
            for vertex in bayes_node.parent_list:
                node = bayes_graph.get_vertex_node(vertex)
                if node is not None:
                    bayes_graph.connect(vertex, bayes_node.vertex)

    return bayes_graph


dataFile = read_file_model_input("demo.txt")
graph = create_graph(dataFile)
for i in graph.node_list:
    print(i.vertex, " parent_list = ", i.parent_list, " value_list = ", i.value_list, " table = ", i.table)

# val_lst -> val_dict
# iograph: create graph
# move bayes.py to bayesgraph.py
# bayesgraph inherit digraph
# move test case to main.py
# push demo.txt on git
