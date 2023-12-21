import sys
from typing import List

DELTAS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def neighbors(i, j, field):
    for di, dj in DELTAS:
        if 0 <= i + di < len(field) and 0 <= j + dj < len(field[0]):
            yield (i + di, j + dj)


def find_reachable_in_one(positions, field) -> set[tuple[int, int]]:
    new_positions = set()
    for i, j in positions:
        for ni, nj in neighbors(i, j, field):
            if field[ni][nj] != "#":
                new_positions.add((ni, nj))
    return new_positions


def find_start(field):
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "S":
                return (i, j)


field = [list(line.strip()) for line in sys.stdin]
print(len(field), len(field[0]))
start = find_start(field)
print(start)
positions = {start}
for _ in range(64):
    positions = find_reachable_in_one(positions, field)

print(len(positions))
