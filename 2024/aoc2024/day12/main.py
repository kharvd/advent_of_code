from collections import deque
import sys


def read_input():
    return [list(line.strip()) for line in sys.stdin.readlines()]


deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def neighbors(field, pos):
    i, j = pos
    for di, dj in deltas:
        if (
            0 <= i + di < len(field)
            and 0 <= j + dj < len(field[0])
            and field[i + di][j + dj] == field[i][j]
        ):
            yield (i + di, j + dj)


def bfs(field, start):
    q = deque()
    q.append(start)
    visited = {start}

    while len(q) > 0:
        n = q.popleft()

        for next in neighbors(field, n):
            if next not in visited:
                visited.add(next)
                q.append(next)

    return visited


def perimeter(field, region):
    p = 0
    for i, j in region:
        for di, dj in deltas:
            if (
                not (0 <= i + di < len(field) and 0 <= j + dj < len(field[0]))
                or field[i][j] != field[i + di][j + dj]
            ):
                p += 1
    return p


def part1():
    field = read_input()
    visited = set()
    total = 0
    for i in range(len(field)):
        for j in range(len(field[0])):
            if (i, j) not in visited:
                region = bfs(field, (i, j))
                total += len(region) * perimeter(field, region)
                visited = visited | region
    print(total)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
