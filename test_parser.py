
class Parser:
    _file = None
    _n = None
    _x = None
    _y = None
    _edges = None

    def init(self, file):
        self._file = file
        self._parse_file()

    # dummy implementation of parsing file
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

    @staticmethod
    def _get_float_list_from_line(line):
        return [float(i) for i in line.split()]

    @staticmethod
    def _get_edge_from_line(line):
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
