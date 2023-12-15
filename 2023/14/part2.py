import sys
import tqdm


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


def tilt_west(field):
    return [shift_row(row) for row in field]


def tilt_north(field):
    transposed = transpose(field)
    new_field = tilt_west(transposed)
    return transpose(new_field)


def tilt_east(field):
    return [shift_row(row[::-1])[::-1] for row in field]


def tilt_south(field):
    transposed = transpose(field)
    new_field = tilt_east(transposed)
    return transpose(new_field)


def count_load(field):
    load = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "O":
                load += len(field) - i
    return load


def hash_field(field):
    o_pos = tuple(
        (i, j)
        for i in range(len(field))
        for j in range(len(field[i]))
        if field[i][j] == "O"
    )
    return hash(o_pos)


field = [list(line.strip()) for line in sys.stdin.readlines() if line.strip()]

seen_fields = set()
loads = []
loop_start = None
loop_end = None
for i in tqdm.trange(1000):
    field = tilt_north(field)
    field = tilt_west(field)
    field = tilt_south(field)
    field = tilt_east(field)
    field_hash = hash_field(field)
    load = count_load(field)
    loads.append((field_hash, load))

    if field_hash in seen_fields:
        loop_start = loads.index((field_hash, load))
        loop_end = i
        print("Loop detected", loop_start, loop_end)
        break
    seen_fields.add(field_hash)

assert loop_start is not None
assert loop_end is not None
loop_length = loop_end - loop_start
index = 1000000000 - 1
print(loads[loop_start + (index - loop_start) % loop_length][1])
