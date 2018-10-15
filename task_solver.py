from abc import ABC, abstractmethod
from overrides import overrides
import numpy as np

from graph import Graph
from task_answer import TaskAnswer


class TaskSolver(ABC):
    _graph = None

    def __init__(self, graph: Graph):
        self._graph = graph

    @abstractmethod
    def get_answer(self) -> TaskAnswer:
        pass


class OptimalSolver(TaskSolver):

    @overrides
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @overrides
    def get_answer(self) -> TaskAnswer:
        # make tree from graph
        self._graph.make_tree()
        diffs = [x - y for x, y in zip(self._graph.get_x(), self._graph.get_y())]
        answer = TaskAnswer()
        negative_moves = []
        # get unmarked leaves un while loop
        leaves = self._graph.get_unmarked_leaves()
        while leaves:
            for vertex in leaves:
                # one leaf may be mark by another leave
                if self._graph.is_mark(vertex):
                    continue
                vertex_value = diffs[vertex]
                if vertex_value != 0:
                    neigbors = self._graph.get_unmarked_neigbors(vertex)
                    if len(neigbors) == 1:
                        up_vertex = self._graph.get_unmarked_neigbors(vertex)[0]
                        diffs[vertex] = 0
                        diffs[up_vertex] += vertex_value
                        if vertex_value > 0:
                            # send up over-value
                            answer.add_step(vertex, up_vertex, vertex_value)
                        elif vertex_value < 0:
                            # send down less-value
                            negative_moves.append((up_vertex, vertex, -vertex_value))
                # mark leaf
                self._graph.mark_vertex(vertex)
            leaves = self._graph.get_unmarked_leaves()
            print(leaves)
        # append negative_moves to the answer in reverse order
        for move in reversed(negative_moves):
            answer.add_step(*move)
        return answer


class SimpleSolver(TaskSolver):

    _data = None
    _n = 0

    @overrides
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @overrides
    def get_answer(self) -> TaskAnswer:
        # get list of vertices
        n = self._graph.get_n()
        self._n = n
        X = self._graph.get_x()
        Y = self._graph.get_y()
        # store in array data - difference between Y and X
        self._data = np.zeros(shape=[n, ], dtype=np.float32)
        for i in range(n):
            self._data[i] = Y[i] - X[i]

        answer = TaskAnswer()
        # check each vertice
        for current_vertex in range(n):
            # fill the gap with the help of neighbors
            if self._data[current_vertex] > 0:
                self._dws_fill(current_vertex, answer)
        return answer

    def _dws_fill(self, source_vertex: int, answer: TaskAnswer):
        deficiency = self._data[source_vertex]
        visited, stack = set(), [source_vertex]
        #helpful array to remember path to source vertex
        path = np.zeros(shape=(self._n,), dtype=np.int32)
        # while source vertex not fill do BFS
        while stack and abs(deficiency) > 10**-7:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)

                neighbors = self._graph.get_neighbours(vertex)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        path[neighbor] = vertex
                    neighbor_diff = self._data[neighbor]
                    if neighbor_diff < 0:
                        # if current neighbor has more value, then it is need
                        # send all it's diff, or deficiency by path
                        if abs(neighbor_diff) < deficiency:
                            self._add_steps_by_path(path, neighbor, source_vertex, abs(neighbor_diff), answer)
                            self._data[neighbor] = 0
                            deficiency -= abs(neighbor_diff)
                        else:
                            self._add_steps_by_path(path, neighbor, source_vertex, deficiency, answer)
                            self._data[neighbor] += deficiency
                            deficiency = 0
                            break
                    stack.append(neighbor)
        return abs(deficiency) < 10**-7

    def _add_steps_by_path(self, path, source, dest, value, answer):
        i = source
        while i != dest:
            answer.add_step(i, path[i], value)
            i = path[i]
