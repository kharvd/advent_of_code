import sys

DIRECTIONS = {"2": (0, -1), "0": (0, 1), "3": (-1, 0), "1": (1, 0)}

dirs = {"2": "L", "0": "R", "3": "U", "1": "D"}

pos = (0, 0)
vertices = [pos]
horizontal_segments = []
commands = []
for line in sys.stdin:
    _, _, color = line.strip().split()
    color = color[2:-1]

    distance_hex = color[:5]
    direction_hex = color[-1]

    distance = int(distance_hex, 16)
    direction = DIRECTIONS[direction_hex]
    print(distance, dirs[direction_hex])

    new_pos = (pos[0] + direction[0] * distance, pos[1] + direction[1] * distance)

    if direction[0] == 0:
        x_start = min(pos[1], new_pos[1])
        x_end = max(pos[1], new_pos[1])
        horizontal_segments.append((x_start, x_end, pos[0]))

    pos = new_pos

    vertices.append(pos)

vertices.append(vertices[0])

print(horizontal_segments)
if vertices[-1][0] == vertices[-2][0]:
    x_start = min(vertices[-1][1], vertices[-2][1])
    x_end = max(vertices[-1][1], vertices[-2][1])
    horizontal_segments.append((x_start, x_end, vertices[-1][0]))

xs = sorted(list(set(v[1] for v in vertices)))
ys = sorted(list(set(v[0] for v in vertices)))

field = [[False for _ in range(len(xs) + 1)] for _ in range(len(ys) + 1)]
for i in range(len(ys)):
    field[i][0] = False
    field[i][len(xs)] = False
for j in range(len(xs)):
    field[0][j] = False
    field[len(ys)][j] = False


def is_inside(i, j, field):
    assert i > 0 and j > 0 and i < len(field) - 1 and j < len(field[0]) - 1

    x = (xs[j - 1] + xs[j]) / 2
    y = (ys[i - 1] + ys[i]) / 2
    c = 0
    for x0, x1, y0 in horizontal_segments:
        if y0 < y and x0 < x < x1:
            c += 1
    return c % 2 == 1


s = 0
for i in range(1, len(ys)):
    for j in range(1, len(xs)):
        if is_inside(i, j, field):
            s += (xs[j] - xs[j - 1]) * (ys[i] - ys[i - 1])
            field[i][j] = True

p = 0
for (start_y, start_x), (end_y, end_x) in zip(vertices, vertices[1:]):
    area = abs(start_y - end_y) + abs(start_x - end_x)
    p += area


for i in range(len(ys) + 1):
    for j in range(len(xs) + 1):
        if field[i][j]:
            print("#", end="")
        else:
            print(".", end="")
    print()

print(s + p // 2 + 1)
