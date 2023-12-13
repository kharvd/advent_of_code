import sys
from collections import defaultdict

NEIGHBORS = {
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    "7": [(1, 0), (0, -1)],
    "-": [(0, 1), (0, -1)],
    "|": [(-1, 0), (1, 0)],
}


def make_graph(field):
    graph = defaultdict(set)
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] in NEIGHBORS:
                for di, dj in NEIGHBORS[field[i][j]]:
                    if 0 <= i + di < len(field) and 0 <= j + dj < len(field[i + di]):
                        graph[(i, j)].add((i + di, j + dj))
    start = [
        (i, j)
        for i, row in enumerate(field)
        for j, char in enumerate(row)
        if char == "S"
    ][0]
    graph[start] = set()
    for node in graph:
        for neighbor in graph[node]:
            if neighbor == start:
                graph[start].add(node)

    start_neighbors = {(i - start[0], j - start[1]) for i, j in graph[start]}
    start_letter = None
    for letter, neighbors in NEIGHBORS.items():
        if set(neighbors) == start_neighbors:
            start_letter = letter
            break

    assert start_letter is not None

    field[start[0]][start[1]] = start_letter

    return graph, start


def neighbors_not_in_loop(i, j, dists):
    return [
        (i + di, j + dj)
        for di, dj in [(-1, 0), (0, 1), (1, 0), (0, -1)]
        if (i + di, j + dj) not in dists
        and 0 <= i + di < len(field)
        and 0 <= j + dj < len(field[i + di])
    ]


def bfs(graph, start):
    queue = [start]
    dist = {start: 0}
    while queue:
        node = queue.pop(0)
        for neighbor in graph[node]:
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist


def check_inside(node, field, dists):
    i, j = node
    count = 0
    for k in range(i - 1, -1, -1):
        if field[k][j] in ["-", "F", "L"] and (k, j) in dists:
            count += 1
    return count % 2 == 1


field = [list(line.strip()) for line in sys.stdin]
graph, start = make_graph(field)

dists = bfs(graph, start)

print("Part 1:", max(dists.values()))

s_i = 0
for i in range(len(field)):
    for j in range(len(field[0])):
        if (i, j) not in dists and check_inside((i, j), field, dists):
            s_i += 1

print("Part 2:", s_i)
