
class TaskAnswer:
    # list of tuple: (vertice_source, vertice_destination, moved_value)
    _steps = []

    def get_steps(self) -> list:
        return self._steps

    def add_step(self, source: int, destination: int, value: float):
        step = (source, destination, value)
        self._steps.append(step)

    def print(self):
        for step in self._steps:
            (source, destination, value) = step
            print("from", source, "to", destination, "move", value)
