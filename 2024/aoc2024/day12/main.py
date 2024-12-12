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


def get(field, i, j):
    if 0 <= i < len(field) and 0 <= j < len(field[i]):
        return field[i][j]
    return None


def find_side(field, region, start, normal):
    side = {(start, normal)}
    i, j = start
    ndi, ndj = normal
    if ndi == 0:
        di, dj = 1, 0
    else:
        di, dj = 0, 1

    ii, jj = i + di, j + dj
    while (
        0 <= ii < len(field)
        and 0 <= jj < len(field[0])
        and (ii, jj) in region
        and (
            (
                (get(field, i + ndi, j + ndj) is None)
                and (get(field, ii + ndi, jj + ndj) is None)
            )
            or (
                (get(field, i + ndi, j + ndj) != field[i][j])
                and (get(field, ii + ndi, jj + ndj) != field[i][j])
            )
        )
    ):
        side.add(((ii, jj), normal))
        ii, jj = ii + di, jj + dj

    ii, jj = i - di, j - dj
    while (
        0 <= ii < len(field)
        and 0 <= jj < len(field[0])
        and (ii, jj) in region
        and (
            (
                (get(field, i + ndi, j + ndj) is None)
                and (get(field, ii + ndi, jj + ndj) is None)
            )
            or (
                (get(field, i + ndi, j + ndj) != field[i][j])
                and (get(field, ii + ndi, jj + ndj) != field[i][j])
            )
        )
    ):
        side.add(((ii, jj), normal))
        ii, jj = ii - di, jj - dj
    return side


def num_sides(field, region):
    excluded = set()
    p = 0
    for i, j in region:
        for di, dj in deltas:
            if ((i, j), (di, dj)) in excluded:
                continue

            if (
                not (0 <= i + di < len(field) and 0 <= j + dj < len(field[0]))
                or field[i][j] != field[i + di][j + dj]
            ):
                side = find_side(field, region, (i, j), (di, dj))
                # print(side)
                p += 1
                excluded = excluded | side
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


def part2():
    field = read_input()
    visited = set()
    total = 0
    for i in range(len(field)):
        for j in range(len(field[0])):
            if (i, j) not in visited:
                region = bfs(field, (i, j))
                # print(field[i][j], num_sides(field, region))
                total += len(region) * num_sides(field, region)
                visited = visited | region
    print(total)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
