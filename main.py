from ioparser import *


def parse_graph(file_input):
    io_graph = IOGraph(file_input)
    return io_graph.create_graph()


def main():
    graph_in = parse_graph("demo.txt")
    for i in graph_in.node_list:
        print(i.vertex, " parent_list = ", i.parent_lst, " value_list = ", i.val_dict, " table = ", i.val_table)


if __name__ == "__main__":
    main()
