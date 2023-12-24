import sys

sys.setrecursionlimit(100000)

DELTAS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def neighbors(i, j):
    for di, dj in DELTAS:
        new_i = i + di
        new_j = j + dj
        if (
            0 <= new_i < len(field)
            and 0 <= new_j < len(field[0])
            and field[new_i][new_j] != "#"
        ):
            yield (new_i, new_j)


def build_graph(field):
    graph = {}

    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "#":
                continue
            graph[(i, j)] = set()
            for n in neighbors(i, j):
                graph[(i, j)].add((n, 1))

    return graph


def reduce_graph(graph):
    vertices_to_remove = set()
    for v in graph:
        # collapse vertices with degree 2
        if len(graph[v]) == 2:
            (n1, d1), (n2, d2) = graph[v]
            graph[n1].add((n2, d1 + d2))
            graph[n2].add((n1, d1 + d2))
            graph[n1].remove((v, d1))
            graph[n2].remove((v, d2))
            vertices_to_remove.add(v)

    for v in vertices_to_remove:
        del graph[v]


def print_graphviz(graph):
    print("graph {")
    seen_edges = set()
    for v in graph:
        for n, d in graph[v]:
            if (v, n) in seen_edges or (n, v) in seen_edges:
                continue
            print(f'"{v}" -- "{n}" [label="{d}"];')
            seen_edges.add((v, n))
    print("}")


def longest_path(node, graph, visited):
    if node == end:
        return 0

    max_path = -float("inf")
    visited.add(node)
    for n, d in graph[node]:
        if n in visited:
            continue
        next_len = longest_path(n, graph, visited) + d
        max_path = max(max_path, next_len)
    visited.remove(node)

    return max_path


field = [list(line.strip()) for line in sys.stdin]
start = (0, 1)
end = (len(field) - 1, len(field[0]) - 2)

graph = build_graph(field)
reduce_graph(graph)
# print_graphviz(graph)

max_len = longest_path(start, graph, set())
print(max_len)
