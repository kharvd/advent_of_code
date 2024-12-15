import sys


def read_input():
    field = []
    while line := sys.stdin.readline().strip():
        field.append(list(line))

    moves = []
    while line := sys.stdin.readline().strip():
        moves.extend(list(line))
    return field, moves


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
            if field[i][j] == "O":
                s += 100 * i + j
    return s


def part1():
    field, moves = read_input()
    pos = find_robot(field)

    for move in moves:
        _, pos = try_move(field, pos, deltas[move])

    print_field(field)
    print(compute_score(field))


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
