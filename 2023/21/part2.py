from collections import defaultdict
import sys
from typing import List

import tqdm

DELTAS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def neighbors(i, j, field):
    for di, dj in DELTAS:
        new_i = i + di
        new_j = j + dj
        if 0 <= new_i < len(field) and 0 <= new_j < len(field[0]):
            yield (new_i, new_j, 0, 0)
        elif new_i == -1:
            yield (len(field) - 1, j, -1, 0)
        elif new_i == len(field):
            yield (0, j, 1, 0)
        elif new_j == -1:
            yield (i, len(field[0]) - 1, 0, -1)
        elif new_j == len(field[0]):
            yield (i, 0, 0, 1)


def find_reachable_in_one(positions, field):
    new_positions = defaultdict(set)
    for i, j in positions.keys():
        for ni, nj, fi, fj in neighbors(i, j, field):
            if field[ni][nj] != "#":
                old_positions = positions[(i, j)]
                for old_fi, old_fj in old_positions:
                    new_positions[(ni, nj)].add((old_fi + fi, old_fj + fj))

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

positions = {start: {(0, 0)}}
num_iterations = 0
positions_for_iteration = []
for _ in tqdm.trange(2 * 131 + 65):
    new_positions = find_reachable_in_one(positions, field)
    positions = new_positions
    positions_for_iteration.append(sum(len(pos) for pos in positions.values()))
    num_iterations += 1

counts = defaultdict(int)
for i in range(len(field)):
    for j in range(len(field[i])):
        for fi, fj in positions[(i, j)]:
            counts[(fi, fj)] += 1

k = (26501365 - 65) // 131

center_count = counts[(0, 0)] * (k - 1) ** 2
off_center_count = counts[(0, 1)] * k**2
diagonal_count = (
    counts[(1, 1)] + counts[(-1, 1)] + counts[(1, -1)] + counts[(-1, -1)]
) * (k - 1)
exterior_count = (
    counts[(-2, 1)] + counts[(-2, -1)] + counts[(2, 1)] + counts[(2, -1)]
) * k
tip_count = counts[(0, 2)] + counts[(0, -2)] + counts[(2, 0)] + counts[(-2, 0)]

sum_counts = (
    center_count + off_center_count + diagonal_count + exterior_count + tip_count
)
print(sum_counts)
