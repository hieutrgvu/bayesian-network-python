from bayesnet import *
import numpy as np


class ErrorException(BaseException):
    def __init__(self, item_info):
        self.itemInfo = item_info

    def __str__(self):
        return 'Error exception parser io case : ' + str(self.itemInfo)


class ErrorFormatFile(ErrorException):
    def __init__(self, item_info):
        super().__init__(item_info)


class IOGraph:
    def __init__(self, name_file):
        self.name_file = name_file

    def create_graph(self):
        bayes_graph = BayesNet()
        count = 0

        with open(self.name_file, "r") as f:
            data_file = f.readlines()
        for data_line in data_file:
            data_split = data_line.split(";")
            count += 1
            parent_lst = []
            val_dict = {}
            val_table = []
            # skip the first line
            if count == 1:
                continue

            # node_bayes not existed
            if len(data_split[0]) == 0:
                raise ErrorFormatFile("node name not exist in file")

            vertex = data_split[0]

            if len(data_split[1]) > 0:
                parent_lst = data_split[1].split(",")

            if len(data_split[2]) > 0:
                val_dict = value_dict_parser(data_split[2])

            if len(data_split[3]) > 0 and len(data_split[4]) > 0:
                table = val_table_parser(data_split[3], data_split[4])
                val_table = table

            bayes_graph.add(vertex, parent_lst, val_dict, val_table)

        return connect_bayes_node(bayes_graph)


def value_dict_parser(value_original):
    value_list = value_original.split(",")
    val_dict = {}
    count = 0
    for key in value_list:
        val_dict[key] = count
        count += 1
    return val_dict


def val_table_parser(shape_table_original, table_original):
    shape_table = shape_table_original.split(",")
    table_string = table_original.split(",")
    table_list = np.array(table_string).astype(np.float)
    tuple_shape_table = tuple(map(int, shape_table))

    dimension_table = 1
    for i in tuple_shape_table:
        dimension_table = dimension_table * i

    # dimension reshape invalid
    if dimension_table != len(table_list):
        raise ErrorFormatFile("number of shape is diff with data probability")

    table = np.reshape(table_list, tuple_shape_table)

    return table


def connect_bayes_node(bayes_graph):
    for bayes_node in bayes_graph.node_list:
        if len(bayes_node.parent_lst) > 0:
            for vertex in bayes_node.parent_lst:
                node = bayes_graph.get_vertex_node(vertex)
                if node is not None:
                    bayes_graph.connect(vertex, bayes_node.vertex)

    return bayes_graph

