from abc import ABC, abstractmethod
from overrides import overrides

import graph as graph

class TaskSolver(ABC):

    _graph = None

    def __init__(self, **kwargs):
        self._graph = kwargs.pop("graph")

    @abstractmethod
    def get_answer(self):
        pass


class SimpleSolver(TaskSolver):

    @overrides
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @overrides
    def get_answer(self):
        #get list of vertices
        n = self._graph.get_n()
        print(n)
