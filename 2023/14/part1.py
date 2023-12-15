import sys


def transpose(field):
    return [[row[i] for row in field] for i in range(len(field[0]))]


def shift_row(row):
    groups = []
    curr_group = {
        "O": 0,
        ".": 0,
    }
    for i in range(len(row)):
        if row[i] == "O":
            curr_group["O"] += 1
        elif row[i] == ".":
            curr_group["."] += 1
        elif row[i] == "#":
            if curr_group["O"] > 0 or curr_group["."] > 0:
                groups.append(curr_group)

            groups.append({"#": 1})
            curr_group = {
                "O": 0,
                ".": 0,
            }
    if curr_group["O"] > 0 or curr_group["."] > 0:
        groups.append(curr_group)

    new_row = []
    for group in groups:
        if "#" in group:
            new_row.append("#")
        else:
            new_row.extend(["O"] * group["O"] + ["."] * group["."])
    assert len(new_row) == len(row)
    return new_row


def tilt(field):
    transposed = transpose(field)
    new_field = [shift_row(row) for row in transposed]
    return transpose(new_field)


def count_load(field):
    load = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "O":
                load += len(field) - i
    return load


field = [list(line.strip()) for line in sys.stdin.readlines() if line.strip()]

print(count_load(tilt(field)))
