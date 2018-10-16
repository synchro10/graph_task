from graph import NxGraph
from task_solver import SimpleSolver
from task_solver import OptimalSolver


def run_single_test():
    test = "res/test3.txt"
    graph = NxGraph()
    graph.init_from_txt(test)
    print("Graph before")
    graph.print_graph()
    solver_kwargs = {
        "graph": graph,
    }
    # solver = SimpleSolver(**solver_kwargs)
    solver = OptimalSolver(**solver_kwargs)
    answer = solver.get_answer()
    answer.print()
    if graph.interpretate_task_answer(answer):
        print(test, "PASSED")
    else:
        print(test, "FAILED")
    print("Graph after")
    graph.print_graph(only_nodes=False)


if __name__ == "__main__":
    run_single_test()
