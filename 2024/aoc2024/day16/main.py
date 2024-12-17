from collections import deque
from heapq import heappop, heappush
import sys


def read_input():
    field = []
    while line := sys.stdin.readline().strip():
        field.append(list(line))
    return field


def find(field, c):
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == c:
                return (i, j)
    raise RuntimeError("not found")


deltas = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}
rev_deltas = {o: (-di, -dj) for o, (di, dj) in deltas.items()}
clockwise = {">": "v", "v": "<", "<": "^", "^": ">"}
counterclockwise = {o2: o1 for o1, o2 in clockwise.items()}


def neighbors(field, node, reverse=False):
    i, j, o = node
    di, dj = deltas[o] if not reverse else rev_deltas[o]
    if (
        0 <= i + di < len(field)
        and 0 <= j + dj < len(field[0])
        and field[i + di][j + dj] != "#"
    ):
        yield (i + di, j + dj, o), 1

    yield (i, j, clockwise[o]), 1000
    yield (i, j, counterclockwise[o]), 1000


def dijkstra(field, start, end):
    dists = {start: 0}
    pq = [(0, start)]

    while pq:
        d, v = heappop(pq)

        for n, w in neighbors(field, v):
            new_dist = d + w
            if new_dist < dists.get(n, float("inf")):
                dists[n] = new_dist
                heappush(pq, (dists[n], n))

    return min(dists.get((*end, o), float("inf")) for o in deltas.keys()), dists


def count_tiles(field, end, dists, min_dist):
    q = deque()
    visited = set()
    for o in deltas.keys():
        n = (*end, o)
        if dists.get(n) == min_dist:
            q.append(n)
            visited.add(n)

    while q:
        v = q.popleft()

        for n, w in neighbors(field, v, reverse=True):
            if dists.get(n) == dists[v] - w:
                q.append(n)
                visited.add(n)

    return len(set((i, j) for i, j, _ in visited))


def part1():
    field = read_input()
    start = (*find(field, "S"), ">")
    end = find(field, "E")
    print(dijkstra(field, start, end))


def part2():
    field = read_input()
    start = (*find(field, "S"), ">")
    end = find(field, "E")
    min_dist, dists = dijkstra(field, start, end)
    print(count_tiles(field, end, dists, min_dist))


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
