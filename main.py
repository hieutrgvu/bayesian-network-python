from ioparser import *
import getopt
import sys
import time


def parse_graph(file_input):
    io_graph = IOGraph(file_input)
    return io_graph.create_graph()


def read_command():
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    long_options = ["model=", "test="]
    file_name = ""
    file_test = ""
    try:
        arguments, values = getopt.getopt(argument_list, "", long_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print("Error read command line = ", str(err))
        sys.exit(2)

    for current_argument, current_value in arguments:
        if current_argument == "--model":
            file_name = current_value

        if current_argument == "--test":
            file_test = current_value

    return file_name, file_test


def main():

    start_time = time.time()
    input_model = read_command()
    input_model = ["model.txt", "test.txt"]
    if len(input_model) == 2:
        graph_in = parse_graph(input_model[0])
        for i in graph_in.node_list:
            print(i.vertex, " parent_list = ", i.parent_lst, " value_list = ", i.val_dict, " table = ", i.distribution)

    num = 10**6
    graph_in.sample(num)
    print(graph_in.sample_arr)
    print("1", time.time() - start_time)
    a = np.where((graph_in.sample_arr == (0, 0, 0, 1, 0)).all(axis=1))
    print("2", time.time() - start_time)
    b = np.where((graph_in.sample_arr == (1, 0, 0, 1, 0)).all(axis=1))
    a_c = np.count_nonzero(a)
    b_c = np.count_nonzero(b)
    print(a_c)
    print(b_c)
    print(a_c/(a_c + b_c))
    print("3", time.time() - start_time)


if __name__ == "__main__":
    main()
