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
    for data_line in data_file:
        data_split = data_line.split(";")
        # format line invalid
        if len(data_split) != 5:
            raise ErrorFormatFile(data_line)

        # node_bayes not existed
        if len(data_split[0]) == 0:
            raise ErrorFormatFile(data_line)
