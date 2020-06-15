from digraph import *


def topo_demo():
    dag = DiGraph()
    for i in range(10):
        dag.add(str(i))

    dag.connect('0', '1')
    dag.connect('0', '5')
    dag.connect('1', '7')
    dag.connect('3', '2')
    dag.connect('3', '4')
    dag.connect('3', '7')
    dag.connect('3', '8')
    dag.connect('4', '8')
    dag.connect('6', '0')
    dag.connect('6', '1')
    dag.connect('6', '2')
    dag.connect('8', '2')
    dag.connect('8', '7')
    dag.connect('9', '4')
    print(dag)

    sorter = TopoSorter(dag)
    print(sorter.sort())


topo_demo()
