from collections import defaultdict
import sys


def read_input():
    return [list(l.strip()) for l in sys.stdin.readlines()]


def validate(field, point):
    i, j = point
    return 0 <= i < len(field) and 0 <= j < len(field[i])


def part1():
    field = read_input()
    pos = defaultdict(list)
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] != ".":
                pos[field[i][j]].append((i, j))

    nodes = set()
    for f, points in pos.items():
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                p1 = points[i]
                p2 = points[j]
                n1 = (2 * p2[0] - p1[0], 2 * p2[1] - p1[1])
                n2 = (2 * p1[0] - p2[0], 2 * p1[1] - p2[1])
                if validate(field, n1):
                    nodes.add(n1)
                if validate(field, n2):
                    nodes.add(n2)
    print(len(nodes))


def part2():
    field = read_input()
    pos = defaultdict(list)
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] != ".":
                pos[field[i][j]].append((i, j))

    nodes = set()
    for f, points in pos.items():
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                p1 = points[i]
                p2 = points[j]
                for k in range(-71, 72):
                    n = (k * (p2[0] - p1[0]) + p2[0], k * (p2[1] - p1[1]) + p2[1])
                    if validate(field, n):
                        print(f, n)
                        nodes.add(n)

    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "." and (i, j) in nodes:
                print("#", end="")
            else:
                print(field[i][j], end="")
        print()
    print(len(nodes))


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
