import sys
from tqdm import trange


def read_input():
    return [list(line.strip()) for line in sys.stdin.readlines() if line.strip()]


def find_start(field):
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "^":
                return i, j
    raise RuntimeError("start not found")


deltas = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
turns = {"^": ">", ">": "v", "v": "<", "<": "^"}


def validated(field, i, j):
    if 0 <= i < len(field) and 0 <= j < len(field[0]):
        return i, j
    return None


def advance(field, pointer, i, j):
    di, dj = deltas[pointer]
    return validated(field, i + di, j + dj)


def print_field(field):
    for line in field:
        print("".join(line))


def traverse(field):
    i, j = find_start(field)
    cur_pointer = "^"
    visited_pos = {(i, j)}
    visited_state = {(i, j, "^")}

    while (new_pos := advance(field, cur_pointer, i, j)) is not None:
        new_i, new_j = new_pos

        if (new_i, new_j, cur_pointer) in visited_state:
            return None

        if field[new_i][new_j] != "#":
            visited_pos.add(new_pos)
            visited_state.add((new_i, new_j, cur_pointer))
            i, j = new_pos
        else:
            cur_pointer = turns[cur_pointer]

    return visited_pos


def part1():
    field = read_input()
    visited = traverse(field)

    print(len(visited))


def part2():
    field = read_input()

    k = 0
    for i in trange(len(field)):
        for j in trange(len(field[i]), leave=False):
            if field[i][j] == ".":
                field[i][j] = "#"
                visited = traverse(field)
                if visited is None:
                    k += 1
                field[i][j] = "."

    print(k)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
