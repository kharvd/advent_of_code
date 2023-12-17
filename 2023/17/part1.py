import sys


def neighbors(node, field):
    (i, j, delta_i, delta_j, num_steps) = node
    deltas = [
        (delta_j, -delta_i, 0),
        (-delta_j, delta_i, 0),
    ]
    if num_steps <= 1:
        deltas.append((delta_i, delta_j, num_steps + 1))

    return [
        (i + delta_i, j + delta_j, delta_i, delta_j, num_steps)
        for delta_i, delta_j, num_steps in deltas
        if 0 <= i + delta_i < len(field) and 0 <= j + delta_j < len(field[0])
    ]


def find_min(queue, dists):
    min_dist = float("inf")
    min_node = None
    for node in queue:
        if dists[node] < min_dist:
            min_dist = dists[node]
            min_node = node
    return min_node


def find_distances(field):
    start = (0, 0, 0, 1, 0)
    dists = {start: field[0][0]}
    queue = [start]
    visited = set()
    prev = {}
    while True:
        node = find_min(queue, dists)
        if node is None:
            raise Exception("No path found")
        if node[0] == len(field) - 1 and node[1] == len(field[0]) - 1:
            return dists[node], prev

        queue.remove(node)
        visited.add(node)
        for neighbor in neighbors(node, field):
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
                dists[neighbor] = dists[node] + field[neighbor[0]][neighbor[1]]
                prev[(neighbor[0], neighbor[1])] = node[:2]
            elif (
                neighbor in queue
                and dists[neighbor] > dists[node] + field[neighbor[0]][neighbor[1]]
            ):
                dists[neighbor] = dists[node] + field[neighbor[0]][neighbor[1]]
                prev[(neighbor[0], neighbor[1])] = node[:2]


field = [
    [int(c) for c in line.strip()] for line in sys.stdin.readlines() if line.strip()
]
dist, prev = find_distances(field)
PREVS = {
    (0, 1): ">",
    (0, -1): "<",
    (1, 0): "v",
    (-1, 0): "^",
}

print("Distance:", dist)
# print("Path:", prev)

# prev1 = {}
# node = (len(field) - 1, len(field[0]) - 1)
# while node != (0, 0):
#     prev1[node] = prev[node]
#     node = prev[node]


# for i in range(len(field)):
#     for j in range(len(field[i])):
#         c = field[i][j]
#         if (i, j) in prev1:
#             prev_i, prev_j = prev1[(i, j)]
#             c = PREVS[(i - prev_i, j - prev_j)]
#         print(c, end="")

#     print()
