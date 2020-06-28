from ioparser import *
import getopt
import sys
import time


def parse_graph(model_file):
    io_graph = IOGraph(model_file)
    return io_graph.create_graph()


def parse_infer(test_file):
    in_infer = IOInfer(test_file)
    in_infer.create_infer()
    return in_infer


def read_command():
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    long_options = ["model=", "test=", "method="]
    file_name = ""
    file_test = ""
    method = ""

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

        if current_argument == "--method":
            method = current_value

    return file_name, file_test, method


def main():
    start_time = time.time()

    input_model = read_command()
    if len(input_model) >= 2:
        graph_in = parse_graph(input_model[0])
        for i in graph_in.node_dict.values():
            print(i.vertex, " parent_list = ", i.parent_lst, " value_list = ", i.val_dict, " table = ", i.distribution)

        infer_in = parse_infer(input_model[1])
        method = "likelihood"
        if len(input_model) == 3 and input_model[2] != "":
            method = input_model[2]

        output_file = open('output.txt', 'w')
        for i in infer_in.infer_list:
            output_value = ""
            print("method = ", method)
            print("infer_dict = ", i.infer_dict, " proof_dict = ", i.proof_dict)
            if "forward" in method:
                output_value = graph_in.infer_forward(i.infer_dict, i.proof_dict)
            elif "likelihood" in method:
                output_value = graph_in.infer_likelihood(i.infer_dict, i.proof_dict)
            output_file.write(str(output_value) + "\n")

        output_file.close()

    print("Time: ", time.time() - start_time)


if __name__ == "__main__":
    main()
