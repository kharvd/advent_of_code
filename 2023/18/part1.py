import sys

DIRECTIONS = {"L": (0, -1), "R": (0, 1), "U": (-1, 0), "D": (1, 0)}

pos = (0, 0)
vertices = [pos]
commands = []
for line in sys.stdin:
    direction, distance, color = line.strip().split()
    distance = int(distance)
    color = color[1:-1]
    commands.append((direction, distance, color))

    direction = DIRECTIONS[direction]

    pos = (pos[0] + direction[0] * distance, pos[1] + direction[1] * distance)
    vertices.append(pos)

vertices.append(vertices[0])

min_x = min(vertices, key=lambda x: x[1])[1]
max_x = max(vertices, key=lambda x: x[1])[1]
min_y = min(vertices, key=lambda x: x[0])[0]
max_y = max(vertices, key=lambda x: x[0])[0]


grid = [["." for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]
for (y_start, x_start), (y_end, x_end) in zip(vertices, vertices[1:]):
    y0 = min(y_start, y_end)
    y1 = max(y_start, y_end)
    x0 = min(x_start, x_end)
    x1 = max(x_start, x_end)

    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            grid[y - min_y][x - min_x] = "#"


def is_horizontal(y, x, field):
    if field[y][x] != "#":
        return False

    return x > 0 and field[y][x - 1] == "#"


def is_inside(y, x, field):
    if field[y][x] != ".":
        return True

    c = 0
    for i in range(y, -1, -1):
        c += is_horizontal(i, x, field)
    return c % 2 == 1


c = 0
for y in range(len(grid)):
    for x in range(len(grid[y])):
        if is_inside(y, x, grid):
            c += 1

print(c)
