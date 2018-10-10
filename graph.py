from abc import ABC, abstractmethod
from overrides import overrides
import networkx as nx


class Graph(ABC):

    _graph_impl = None

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def init_from_txt(self, filename):
        pass


class NxGraph(Graph):

    @overrides
    def __init__(self, **kwargs):
        _graph_impl = nx.Graph()
        super().__init__(**kwargs)

    @overrides
    def init_from_txt(self, filename):
        pass