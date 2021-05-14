import re

from src.Edge import Edge


class Graph(object):
    first_line_pattern = '(?P<name>.*):\s(?P<cost>\d*)'
    main_pattern = '(?P<name>.*):\s(?P<from>.*)\s>\s(?P<to>.*)\s(?P<cost>\d*)'

    def __init__(self):
        self.graph = dict()
        self.start_vertex = None
        self.end_vertex = 'EXIT'
        self.longest_path = list()
        self.to_end = None

    @staticmethod
    def _strip_all(source):
        return [s.strip() for s in source]

    def load(self, source):
        source = self._strip_all(source.readlines())
        first_line, source = source[0], source[1:]

        name, cost = re.match(self.first_line_pattern, first_line).groups()
        self.start_vertex = name
        self.to_end = int(cost)

        for line in source:
            name, _from, to, capacity = re.match(self.main_pattern, line).groups()
            self.graph[name] = Edge(capacity, _from, to)

    def get_vertex_edges(self, name):
        return [v for v in sorted(self.graph.keys()) if self.graph[v].from_r == name]

    def get_current_flow(self, start, end, path=None, visited=None):
        if visited is None:
            visited = list()
        if path is None:
            path = list()

        if start == end:
            return path

        for edge in self.get_vertex_edges(start):
            capacity_diff = self.graph[edge].get_capacity_difference()
            if edge not in path and capacity_diff > 0:
                if self.graph[edge].to_r not in visited:
                    path.extend([edge])
                    visited.extend([visited])

                    flow = self.get_current_flow(self.graph[edge].to_r, end, path, visited)
                    if flow:
                        return flow

    def get_path_flow(self, flow):
        return min([self.graph[edge].get_capacity_difference() for edge in flow])

    def add_flow(self, path, size):
        for edge in path:
            self.graph[edge].add_used_capacity(int(size))

    def max_flow(self):
        flow = self.get_current_flow(start=self.start_vertex, end=self.end_vertex)
        if not flow:
            return

        try:
            while flow:
                if len(flow) > len(self.longest_path):
                    self.longest_path = flow
                f = self.get_path_flow(flow)
                self.add_flow(flow, f)
                flow = self.get_current_flow(start=self.start_vertex, end=self.end_vertex)
        except:
            return

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


    def flow_count(self):
        #todo maybe sorted(self.graph.keys())
        ends = [self.graph[edge].used_capacity for edge in sorted(self.graph.keys())
                if self.graph[edge].to_r == self.end_vertex]
        return sum(ends) if ends else 0
