from graph import NxGraph
from task_solver import SimpleSolver


def example():
    test = "res/test1.txt"
    graph = NxGraph()
    graph.init_from_txt(test)
    print("Graph before")
    graph.print_graph()
    solver_kwargs = {
        "graph": graph,
    }
    solver = SimpleSolver(**solver_kwargs)
    answer = solver.get_answer()
    answer.print()
    if graph.interpretate_task_answer(answer):
        print(test, "Passed")
    else:
        print(test, "Failed")
    print("Graph after")
    graph.print_graph(only_nodes=True)


example()
