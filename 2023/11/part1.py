import sys

field = [list(line.strip()) for line in sys.stdin]
empty_rows = set(i for i, row in enumerate(field) if row.count("#") == 0)
empty_cols = set(
    i for i in range(len(field[0])) if [row[i] for row in field].count("#") == 0
)

galaxies_pos = [
    (i, j) for i, row in enumerate(field) for j, char in enumerate(row) if char == "#"
]

sum_dists = 0
for g1 in range(len(galaxies_pos)):
    for g2 in range(g1 + 1, len(galaxies_pos)):
        i1, j1 = galaxies_pos[g1]
        i2, j2 = galaxies_pos[g2]
        d = abs(i1 - i2) + abs(j1 - j2)
        for k in range(min(i1, i2), max(i1, i2) + 1):
            if k in empty_rows:
                d += 1000000 - 1
        for k in range(min(j1, j2), max(j1, j2) + 1):
            if k in empty_cols:
                d += 1000000 - 1
        sum_dists += d

print(sum_dists)
