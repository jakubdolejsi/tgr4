

class Vertex:

    def __init__(self, name, ancestor, cost, distance=float('inf')):
        self._name = name
        self._value = cost
        self._ancestors = {ancestor}
        self._distance = distance

    def add_ancestor(self, ancestor):
        self._ancestors.add(ancestor)

    def set_value(self, value):
        self._value = value

    def set_distance(self, distance):
        self._distance = distance

    def get_name(self):
        return self._name
