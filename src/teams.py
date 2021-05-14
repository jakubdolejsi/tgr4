import sys
import re
from collections import defaultdict


class Graph:
    pattern = '(.*)\s-\s(.*)'

    def __init__(self):
        self.graph = defaultdict(set)
        self.vertices = list()

    def load(self, source):
        source = iter(source.readlines())
        first_line = next(source)
        self.vertices = first_line.split(',')

        for line in source:
            _from, _to = re.match(self.pattern, line.strip()).groups()
            self.graph[_from].add(_to)
            self.graph[_to].add(_from)


    def color_nodes(self):
        smallest_groups = {}
        for name in sorted(self.graph, key=lambda x: len(self.graph[x]), reverse=True):
            neighbour_colors = list(smallest_groups.get(neighbour) for neighbour in self.graph[name])
            new_group = [color for color in range(len(self.graph)) if color not in neighbour_colors]
            smallest_groups[name] = new_group[0]

        groups = defaultdict(set)
        for key, val in sorted(smallest_groups.items()):
            groups[val].add(key)

        return groups

    @staticmethod
    def print_color_map(maps):
        for names in maps.values():
            print(", ".join(names))

def main():

    graph = Graph()
    graph.load(sys.stdin)
    maps = graph.color_nodes()
    graph.print_color_map(maps)


if __name__ == '__main__':
    main()
