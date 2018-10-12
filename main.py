from graph import NxGraph
from task_solver import SimpleSolver

graph = NxGraph()
graph.init_from_txt("res/test1.txt")
graph.print_graph()
solver_kwargs = {
    "graph": graph,
}
solver = SimpleSolver(**solver_kwargs)
answer = solver.get_answer()
