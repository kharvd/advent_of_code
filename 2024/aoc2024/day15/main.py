import sys


def read_input():
    field = []
    while line := sys.stdin.readline().strip():
        field.append(list(line))

    moves = []
    while line := sys.stdin.readline().strip():
        moves.extend(list(line))
    return field, moves


def blowup(field):
    new_field = []
    for line in field:
        new_line = []
        for c in line:
            if c == "#":
                new_line.append("#")
                new_line.append("#")
            elif c == "O":
                new_line.append("[")
                new_line.append("]")
            elif c == ".":
                new_line.append(".")
                new_line.append(".")
            elif c == "@":
                new_line.append("@")
                new_line.append(".")
        new_field.append(new_line)
    return new_field


def try_move(field, pos, delta):
    i, j = pos
    ty = field[i][j]
    if ty == "#":
        return False, (i, j)
    if ty == ".":
        return True, (i, j)

    di, dj = delta
    ni, nj = i + di, j + dj
    if try_move(field, (ni, nj), delta)[0]:
        field[i][j] = "."
        field[ni][nj] = ty
        return True, (ni, nj)
    return False, (i, j)


deltas = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}


def find_robot(field):
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "@":
                return (i, j)
    raise RuntimeError("no robot")


def print_field(field):
    for line in field:
        for c in line:
            print(c, end="")
        print()


def compute_score(field):
    s = 0
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == "O" or field[i][j] == "[":
                s += 100 * i + j

    return s


def part1():
    field, moves = read_input()
    pos = find_robot(field)

    for move in moves:
        _, pos = try_move(field, pos, deltas[move])

    print_field(field)
    print(compute_score(field))


def can_move(field, pos, delta):
    i, j = pos
    ty = field[i][j]
    di, dj = delta
    ni, nj = i + di, j + dj

    if ty == "#":
        return False
    if ty == ".":
        return True

    if (ty == "[" or ty == "]") and dj == 0:
        mi, mj = (i, j + 1) if ty == "[" else (i, j - 1)
        if not can_move(field, (mi + di, mj + dj), delta):
            return False

    return can_move(field, (ni, nj), delta)


complement = {"[": "]", "]": "["}


def apply_move(field, pos, delta):
    i, j = pos
    ty = field[i][j]
    di, dj = delta
    ni, nj = i + di, j + dj

    if ty == "#":
        raise RuntimeError("cannot move wall")
    if ty == ".":
        return (i, j)

    if (ty == "[" or ty == "]") and dj == 0:
        mi, mj = (i, j + 1) if ty == "[" else (i, j - 1)
        apply_move(field, (mi + di, mj + dj), delta)
        field[mi][mj] = "."
        field[mi + di][mj + dj] = complement[ty]

    apply_move(field, (ni, nj), delta)
    field[i][j] = "."
    field[ni][nj] = ty
    return (ni, nj)


def part2():
    field, moves = read_input()
    field = blowup(field)
    pos = find_robot(field)

    for move in moves:
        movable = can_move(field, pos, deltas[move])
        if movable:
            pos = apply_move(field, pos, deltas[move])

    print_field(field)
    print(compute_score(field))


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
