from abc import ABC, abstractmethod
from overrides import overrides
import networkx as nx

from task_answer import TaskAnswer
from test_parser import Parser


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
    def print_graph(self, only_nodes=False):
        pass

    @abstractmethod
    def interpretate_task_answer(self, answer: TaskAnswer) -> bool:
        pass

    @abstractmethod
    def _check_required_statement(self) -> bool:
        pass

    @abstractmethod
    def get_neighbours(self, vertex: int) -> list:
        pass

    @abstractmethod
    def make_tree(self):
        pass

    @abstractmethod
    def mark_vertex(self, vertex: int):
        pass

    @abstractmethod
    def get_unmarked_leaves(self) -> list:
        pass

    @abstractmethod
    def get_unmarked_neigbors(self, vertex: int) -> list:
        pass

    @abstractmethod
    def is_mark(self, vertex: int) -> bool:
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
        # may be implement
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
    def init_from_txt(self, filename: str):
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
    def _create_graph(self) -> bool:
        if self._n == 0 or self._edges is None:
            raise Exception("failed init graph params")
        # create vertices
        for i in range(self._n):
            self._graph_impl.add_node(i)
        # create edges
        for edge in self._edges:
            self._graph_impl.add_edge(edge[0], edge[1])
        # init weights
        for i in range(self._n):
            self._graph_impl.node[i]["weight"] = self._X[i]
            self._graph_impl.node[i]["mark"] = False
        return True

    @overrides
    def print_graph(self, only_nodes=False):
        print(list(self._graph_impl.nodes(data=True)))
        if not only_nodes:
            print(list(self._graph_impl.edges()))

    @overrides
    def interpretate_task_answer(self, answer: TaskAnswer) -> bool:
        steps = answer.get_steps()
        for i, step in enumerate(steps):
            (source_ver, dest_ver, value) = step
            edges = self._graph_impl.edges()
            # check correct state
            if self._graph_impl.node[source_ver]["weight"] < value:
                raise Exception("less zero during interpretation on step", i)
            elif not (source_ver, dest_ver) in edges and not (dest_ver, source_ver) in edges:
                raise Exception("graph doesn't contain edge", source_ver, dest_ver, "on step", i)
            elif value < 0:
                raise Exception("negative value on step", i)
            else:
                self._graph_impl.node[source_ver]["weight"] -= value
                self._graph_impl.node[dest_ver]["weight"] += value
        return self._check_required_statement()

    @overrides
    def _check_required_statement(self) -> bool:
        for i in range(self._n):
            if abs(self._graph_impl.node[i]["weight"] - self._Y[i]) > 10 ** -7:
                return False
        return True

    @overrides
    def get_neighbours(self, vertex: int) -> list:
        return self._graph_impl.neighbors(vertex)

    @overrides
    def make_tree(self):
        edges = list(self._graph_impl.edges)
        for edge in edges:
            self._graph_impl.remove_edge(*edge)
            components = nx.algorithms.number_connected_components(self._graph_impl)
            if components > 1:
                self._graph_impl.add_edge(*edge)

    @overrides
    def mark_vertex(self, vertex: int):
        self._graph_impl.node[vertex]["mark"] = True

    @overrides
    def get_unmarked_leaves(self) -> list:
        unmarked_leaves = []
        nodes = self._graph_impl.nodes()
        for node in nodes:
            if self._graph_impl.node[node]["mark"]:
                continue
            # append node if it has 0 or 1 unmarked neighbor
            unmarked_neighbors = self.get_unmarked_neigbors(node)
            if len(unmarked_neighbors) < 2:
                unmarked_leaves.append(node)
        return unmarked_leaves

    @overrides
    def get_unmarked_neigbors(self, vertex) -> list:
        neighbors = self._graph_impl.neighbors(vertex)
        out = []
        count_unmark = 0
        for neighbor in neighbors:
            if not self._graph_impl.node[neighbor]["mark"]:
                out.append(neighbor)
        return out

    @overrides
    def is_mark(self, vertex: int) -> bool:
        return self._graph_impl.node[vertex]["mark"]
