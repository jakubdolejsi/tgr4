import sys

import re

from Edge import Edge


class AND(object):

    def __init__(self, obj):
        self.obj = obj

    def And(self):
        return self.obj


class Graph(object):
    first_line_pattern = '(?P<name>.*):\s(?P<cost>\d*)'
    main_pattern = '(?P<name>.*):\s(?P<from>.*)\s>\s(?P<to>.*)\s(?P<cost>\d*)'

    def __init__(self):
        self.graph = dict()
        self.source = None
        self.sink = 'EXIT'
        self.longest_path = list()
        self.to_end = None

    def load(self, source):
        source = iter(self._strip_all(source.readlines()))
        first_line = next(source)

        name, cost = self._match_pattern(self.first_line_pattern, first_line)
        self.source = name
        self.to_end = int(cost)

        for line in source:
            name, _from, to, capacity = self._match_pattern(self.main_pattern, line)
            self.graph[name] = Edge(capacity, _from, to)

    def get_current_flow(self, start, sink, path=None, visited=None):
        if start == sink:
            return path
        if visited is None:
            visited = list()
        if path is None:
            path = list()
        for vertex in self.get_vertex_edges(start):
            if vertex not in path and self.graph[vertex].get_capacity_difference() > 0 and self.graph[vertex].to_r not \
                    in visited:
                flow = self.get_current_flow(self.graph[vertex].to_r, sink, path + [vertex], visited + [start])
                if not flow:
                    continue
                return flow

    @staticmethod
    def _match_pattern(pattern, string):
        return re.match(pattern, string).groups()

    @staticmethod
    def _strip_all(source):
        return [s.strip() for s in source]

    def get_vertex_edges(self, name):
        return [v for v in sorted(self.graph.keys()) if self.graph[v].from_r == name]

    def get_path_flow(self, flow):
        return min([self.graph[edge].get_capacity_difference() for edge in flow])

    def add_flow(self, path, size):
        for edge in path:
            self.graph[edge].add_used_capacity(int(size))

    def compute_max_flow(self):
        flow = self.get_current_flow(self.source, self.sink)

        while flow:
            if len(flow) > len(self.longest_path):
                self.longest_path = flow
            f = self.get_path_flow(flow)
            self.add_flow(flow, f)
            flow = self.get_current_flow(self.source, self.sink)

        return AND(self)

    def summary(self, flow_count):
        print("Group size: {size}".format(size=flow_count))
        for edge in self.graph.keys():
            output_value = "{edge}: ".format(edge=edge)
            is_tight = self.graph[edge].is_full()
            if is_tight:
                output_value += "!{capacity}!".format(capacity=self.graph[edge].used_capacity)
            else:
                output_value += "{capacity}".format(capacity=self.graph[edge].used_capacity)
            print(output_value)
        print("Time: {time}".format(time=self._count_time()))

    def _count_time(self):
        group_time = len(self.longest_path)
        flow = self.flow_count()

        try:
            group = self.to_end // flow
        except Exception:
            return 1
        return group + group_time

    def flow_count(self):
        # todo maybe sorted(self.graph.keys())
        ends = [self.graph[edge].used_capacity for edge in sorted(self.graph.keys())
                if self.graph[edge].to_r == self.sink]
        return sum(ends) if ends else 0


def main():
    graph = Graph()
    try:
        graph.load(source=sys.stdin)
        flow = graph.compute_max_flow().And().flow_count()
        graph.summary(flow_count=flow)
    except:
        pass


if __name__ == '__main__':
    sys.exit(main())
