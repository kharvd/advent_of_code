from collections import Counter, defaultdict, deque
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


deltas = [(0, -1), (-1, 0), (1, 0), (0, 1)]


def neighbors(field, node, cheat=False):
    i, j = node
    for di, dj in deltas:
        if (
            0 <= i + di < len(field)
            and 0 <= j + dj < len(field[0])
            and (field[i + di][j + dj] != "#" or cheat)
        ):
            yield (i + di, j + dj)


def cheat_neighbors(field, node):
    for n in neighbors(field, node, cheat=True):
        for m in neighbors(field, n):
            yield m


def big_cheat_neighbors(field, node, max_dist):
    q = deque()
    q.append(node)
    dists = {node: 0}

    while q:
        v = q.popleft()

        if dists[v] > max_dist:
            break

        if field[v[0]][v[1]] != "#":
            yield v, dists[v]

        for n in neighbors(field, v, cheat=True):
            if n not in dists:
                dists[n] = dists[v] + 1
                q.append(n)


def bfs(field, start, end):
    dists = {start: 0}
    pq = deque()
    pq.append(start)
    paths = {}
    paths[start] = [start]

    while pq:
        v = pq.popleft()

        for n in neighbors(field, v):
            if n not in dists:
                dists[n] = dists[v] + 1
                pq.append(n)
                paths[n] = paths[v] + [n]

    return paths[end]


def part1():
    field = read_input()
    start = find(field, "S")
    end = find(field, "E")
    path = bfs(field, start, end)

    dists = {x: len(path) - i for i, x in enumerate(path)}

    normal_time = len(path) - 1

    counter = Counter()
    for i in range(len(path)):
        node = path[i]
        for n, d in big_cheat_neighbors(field, node, max_dist=2):
            time = i + dists[n] + d - 1
            if time < normal_time:
                saved = normal_time - time
                counter[saved] += 1

    total = 0
    for s, c in counter.items():
        if s >= 100:
            total += c
    print(total)


def part2():
    field = read_input()
    start = find(field, "S")
    end = find(field, "E")
    path = bfs(field, start, end)

    dists = {x: len(path) - i for i, x in enumerate(path)}

    normal_time = len(path) - 1

    counter = Counter()
    for i in range(len(path)):
        node = path[i]
        for n, d in big_cheat_neighbors(field, node, max_dist=20):
            time = i + dists[n] + d - 1
            if time < normal_time:
                saved = normal_time - time
                if saved >= 50:
                    counter[saved] += 1

    print(counter)
    total = 0
    for s, c in counter.items():
        if s >= 100:
            total += c
    print(total)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
