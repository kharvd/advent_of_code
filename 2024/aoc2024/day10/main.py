from collections import defaultdict, deque
import sys


def read_input():
    return [[int(c) for c in line.strip()] for line in sys.stdin.readlines()]


deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def neighbors(field, pos):
    i, j = pos
    for di, dj in deltas:
        if (
            0 <= i + di < len(field)
            and 0 <= j + dj < len(field[0])
            and field[i + di][j + dj] == field[i][j] + 1
        ):
            yield (i + di, j + dj)


def bfs(field, pos):
    q = deque()
    q.append(pos)

    visited = set()
    count = 0

    while len(q) > 0:
        i, j = q.popleft()
        if field[i][j] == 9:
            count += 1

        for ii, jj in neighbors(field, (i, j)):
            if (ii, jj) not in visited:
                q.append((ii, jj))
                visited.add((ii, jj))

    return count


def part1():
    field = read_input()
    total = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 0:
                score = bfs(field, (i, j))
                total += score
    print(total)


def bfs2(field, pos):
    q = deque()
    q.append(pos)

    visited = set()
    ratings = defaultdict(int)
    ratings[pos] = 1
    ends = set()

    while len(q) > 0:
        i, j = q.popleft()
        if field[i][j] == 9:
            ends.add((i, j))

        for ii, jj in neighbors(field, (i, j)):
            ratings[(ii, jj)] += ratings[(i, j)]
            if (ii, jj) not in visited:
                q.append((ii, jj))
                visited.add((ii, jj))

    count = sum(ratings[pos] for pos in ends)

    return count


def part2():
    field = read_input()
    total = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 0:
                score = bfs2(field, (i, j))
                total += score
    print(total)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
