import sys

from src.Graph import Graph


def main():
    graph = Graph()
    graph.load(sys.stdin)
    graph.max_flow()
    flow = graph.flow_count()
    graph.summary(flow_count=flow)

if __name__ == '__main__':
    main()
