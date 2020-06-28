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
    def __init__(self, model_file):
        self.model_file = model_file

    def create_graph(self):
        graph = parse_file_model(self.model_file)
        return graph


class Infer:
    def __init__(self, infer_dict, proof_dict):
        self.infer_dict = infer_dict
        self.proof_dict = proof_dict


class IOInfer:
    def __init__(self, test_file):
        self.test_file = test_file
        self.infer_list = []

    def create_infer(self):
        self.infer_list = parse_file_test(self.test_file)


def parse_file_model(model_file):
    bayes_graph = BayesNet()
    count = 0

    with open(model_file, "r") as f:
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
    for bayes_node in bayes_graph.node_dict.values():
        if len(bayes_node.parent_lst) > 0:
            for vertex in bayes_node.parent_lst:
                node = bayes_graph.get_vertex_node(vertex)
                if node is not None:
                    bayes_graph.connect(vertex, bayes_node.vertex)

    return bayes_graph


def parse_file_test(test_file):
    count = 0
    io_infer_list = []

    with open(test_file, "r") as f:
        data_file = f.readlines()
    for data_line in data_file:
        data_split = data_line.split(";")
        count += 1
        # skip the first line
        if count == 1:
            continue

        # check len question
        if len(data_split) == 0:
            raise ErrorFormatFile("test file not enough argument")

        infer_dict = {}
        if len(data_split[0]) > 0:
            infer_dict = infer_dict_parser(data_split[0])

        proof_dict = {}
        if len(data_split[1]) > 0:
            proof_dict = infer_dict_parser(data_split[1])

        infer_object = Infer(infer_dict, proof_dict)
        io_infer_list.append(infer_object)

    return io_infer_list


def infer_dict_parser(infer_original):
    infer_list = infer_original.split(",")
    infer_dict = {}
    for infer_element in infer_list:
        infer = infer_element.split("=")
        if len(infer) == 2:
            infer_dict[infer[0]] = infer[1].rstrip()
        else:
            if infer[0] != '\n':
                raise ErrorFormatFile("test file error format")

    return infer_dict
