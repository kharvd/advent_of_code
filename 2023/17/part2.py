import sys
from fibheap import Fheap, Node


def neighbors(node, field):
    (i, j, delta_i, delta_j, num_steps) = node
    deltas = []
    if num_steps >= 4:
        deltas.extend(
            [
                (delta_j, -delta_i, 1),
                (-delta_j, delta_i, 1),
            ]
        )
    if num_steps < 10:
        deltas.append((delta_i, delta_j, num_steps + 1))

    return [
        (i + delta_i, j + delta_j, delta_i, delta_j, num_steps)
        for delta_i, delta_j, num_steps in deltas
        if 0 <= i + delta_i < len(field) and 0 <= j + delta_j < len(field[0])
    ]


def find_distances(field):
    start = (0, 0, 0, 1, 0)
    dists = {start: field[0][0]}
    queue = Fheap()
    nodes = {start: Node((dists[start], start))}
    queue.insert(nodes[start])

    visited = set()
    while True:
        _, node = queue.extract_min().key
        if node[0] == len(field) - 1 and node[1] == len(field[0]) - 1 and node[-1] >= 4:
            return dists[node]

        visited.add(node)
        for neighbor in neighbors(node, field):
            new_dist = dists[node] + field[neighbor[0]][neighbor[1]]
            if neighbor not in visited and neighbor not in dists:
                dists[neighbor] = new_dist
                nodes[neighbor] = Node((new_dist, neighbor))
                queue.insert(nodes[neighbor])
            elif neighbor in dists and dists[neighbor] > new_dist:
                dists[neighbor] = new_dist
                queue.decrease_key(nodes[neighbor], (new_dist, neighbor))


field = [
    [int(c) for c in line.strip()] for line in sys.stdin.readlines() if line.strip()
]
dist = find_distances(field)

print("Distance:", dist - field[0][0])
