from collections import deque
import sys

DELTAS_SPLIT = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
}


def neighbor_deltas(cell_type, delta):
    if (
        cell_type == "."
        or (cell_type == "|" and delta[1] == 0)
        or (cell_type == "-" and delta[0] == 0)
    ):
        return [delta]

    if cell_type == "|" or cell_type == "-":
        return DELTAS_SPLIT[cell_type]

    if cell_type == "\\" or cell_type == "/":
        mult = 1 if cell_type == "\\" else -1
        d_mirror = (delta[1] * mult, delta[0] * mult)
        return [d_mirror]

    return []


def neighbors(node, field):
    (i, j), delta = node
    deltas = neighbor_deltas(field[i][j], delta)
    return [
        ((i + d[0], j + d[1]), d)
        for d in deltas
        if 0 <= i + d[0] < len(field) and 0 <= j + d[1] < len(field[0])
    ]


def bfs(field, start):
    queue = deque([start])
    visited = set([start])

    while queue:
        node = queue.popleft()

        for neighbor in neighbors(node, field):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    visited_cells = {n for n, _ in visited}
    return len(visited_cells)


field = [list(line.strip()) for line in sys.stdin.readlines() if line.strip()]

start_node = ((0, 0), (0, 1))
print(bfs(field, start_node))
