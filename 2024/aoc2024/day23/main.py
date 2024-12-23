from collections import defaultdict, deque
from heapq import heappop, heappush
import networkx as nx
import sys


def read_input():
    graph = defaultdict(set)
    while line := sys.stdin.readline().strip():
        fro, to = line.split("-")
        graph[fro].add(to)
        graph[to].add(fro)
    return graph


def read_input2():
    edges = []
    while line := sys.stdin.readline().strip():
        fro, to = line.split("-")
        edges.append((fro, to))
    graph = nx.Graph()
    graph.add_edges_from(edges)
    return graph


def find_3_clique(graph):
    cliques = set()
    for v1 in graph.keys():
        for v2 in graph[v1]:
            for v3 in graph[v2]:
                if v3 in graph[v1] and (v1[0] == "t" or v2[0] == "t" or v3[0] == "t"):
                    clique = sorted([v1, v2, v3])
                    cliques.add(tuple(clique))
    return cliques


def part1():
    graph = read_input()
    print(len(find_3_clique(graph)))


def part2():
    graph = read_input2()
    clique = max(nx.find_cliques(graph), key=len)
    print(",".join(sorted(clique)))


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
