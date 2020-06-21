from ioparser import *
import getopt, sys


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
    input_model = read_command()
    if len(input_model) == 2:
        graph_in = parse_graph(input_model[0])
        for i in graph_in.node_list:
            print(i.vertex, " parent_list = ", i.parent_lst, " value_list = ", i.val_dict, " table = ", i.val_table)


if __name__ == "__main__":
    main()
