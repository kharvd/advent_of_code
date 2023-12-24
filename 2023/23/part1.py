from functools import cache
import sys

sys.setrecursionlimit(100000)
field = [list(line.strip()) for line in sys.stdin]
start = (0, 1)
end = (len(field) - 1, len(field[0]) - 2)


@cache
def longest_path(i, j, came_from):
    if (i, j) == start:
        return 0

    max_path = -float("inf")
    for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
        if (ni, nj) == came_from:
            continue
        if ni < 0 or nj < 0 or ni >= len(field) or nj >= len(field[0]):
            continue
        if field[ni][nj] == ">" and (ni, nj) != (i, j - 1):
            continue
        if field[ni][nj] == "<" and (ni, nj) != (i, j + 1):
            continue
        if field[ni][nj] == "^" and (ni, nj) != (i + 1, j):
            continue
        if field[ni][nj] == "v" and (ni, nj) != (i - 1, j):
            continue
        if field[ni][nj] == "#":
            continue
        max_path = max(max_path, longest_path(ni, nj, (i, j)))
    return max_path + 1


print(longest_path(*end, None))
