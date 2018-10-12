from abc import ABC, abstractmethod
from overrides import overrides
import networkx as nx

class Graph(ABC):

    _graph_impl = None
    _n = 0
    _X = None
    _Y = None
    _edges = None

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def init_from_txt(self, filename):
        pass

    @abstractmethod
    def _create_graph(self):
        pass

    @abstractmethod
    def print_graph(self):
        pass

    @classmethod
    def set_params(cls, n, X, Y, edges):
        if cls._verify_params(n, X, Y, edges):
            cls._n = n
            cls._X = X
            cls._Y = Y
            cls._edges = edges
        else:
            raise Exception("bad params")

    @classmethod
    def _verify_params(cls, n, X, Y, edges):
        #may be implement
        return True

    @classmethod
    def get_n(cls):
        return cls._n

    @classmethod
    def get_x(cls):
        return cls._X

    @classmethod
    def get_y(cls):
        return cls._Y


class NxGraph(Graph):

    @overrides
    def __init__(self, **kwargs):
        self._graph_impl = nx.Graph()
        super().__init__(**kwargs)

    @overrides
    def init_from_txt(self, filename):
        with open(filename, "r") as f:
            parser = Parser()
            parser.init(f)
            n = parser.get_n()
            X = parser.get_x()
            Y = parser.get_y()
            edges = parser.get_edges()
            del parser
        self.set_params(n, X, Y, edges)
        self._create_graph()

    @overrides
    def _create_graph(self):
        if self._n == 0 or self._edges is None:
            raise Exception("failed init graph params")
        #create vertices
        for i in range(self._n):
            self._graph_impl.add_node(i)
        #create edges
        for edge in self._edges:
            self._graph_impl.add_edge(edge[0], edge[1])
        #init weights
        for i in range(self._n):
            self._graph_impl.node[i]["weight"] = self._X[i]
        return True

    @overrides
    def print_graph(self):
        print(list(self._graph_impl.nodes(data=True)))
        print(list(self._graph_impl.edges()))

class Parser:

    _file = None
    _n = None
    _x = None
    _y = None
    _edges = None

    def init(self, file):
        self._file = file
        self._parse_file()

    #dummy implementation of parsing file
    def _parse_file(self):
        try:
            lines = self._file.readlines()
            self._n = int(lines[0])
            self._x = self._get_float_list_from_line(lines[1])
            self._y = self._get_float_list_from_line(lines[2])
            self._edges = []
            for edge_line in lines[3:]:
                self._edges.append(self._get_edge_from_line(edge_line))
        except:
            raise Exception("some error in file format")

    def _get_float_list_from_line(self, line):
        return [float(i) for i in line.split()]

    def _get_edge_from_line(self, line):
        edge = [int(i) for i in line.split()]
        if len(edge) != 2:
            raise Exception("not 2 vertex in edge")
        return edge

    def get_n(self):
        return self._n

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_edges(self):
        return self._edges
