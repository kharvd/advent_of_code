import sys


def does_reflect_vertical(pat, axis_j):
    for i in range(len(pat)):
        left = pat[i][:axis_j]
        right = pat[i][axis_j:]
        min_len = min(len(left), len(right))
        if left[::-1][:min_len] != right[:min_len]:
            return False

    return True


def transpose(pat):
    return ["".join([pat[i][j] for i in range(len(pat))]) for j in range(len(pat[0]))]


def does_reflect_horizontal(pat, axis_i):
    return does_reflect_vertical(transpose(pat), axis_i)


def find_horizontal_axis(pat, ignore=None):
    for i in range(1, len(pat)):
        if ignore is not None and i == ignore:
            continue
        if does_reflect_horizontal(pat, i):
            return i
    return None


def find_vertical_axis(pat, ignore=None):
    for j in range(1, len(pat[0])):
        if ignore is not None and j == ignore:
            continue
        if does_reflect_vertical(pat, j):
            return j
    return None


def find_reflection_axis(pat, ignore=None):
    if i := find_horizontal_axis(
        pat, ignore[1] if ignore and ignore[0] == "h" else None
    ):
        return ("h", i)
    if j := find_vertical_axis(pat, ignore[1] if ignore and ignore[0] == "v" else None):
        return ("v", j)
    return None


def mutate(pat):
    for i in range(len(pat)):
        for j in range(len(pat[i])):
            old_line = pat[i]
            line = list(pat[i])
            line[j] = "." if line[j] == "#" else "#"
            pat[i] = "".join(line)
            yield pat
            pat[i] = old_line


patterns = []
current_pattern = []

for line in sys.stdin.readlines():
    if line.strip() == "":
        patterns.append(current_pattern)
        current_pattern = []
        continue
    current_pattern.append(line.strip())

patterns.append(current_pattern)

num_vert = 0
num_hor = 0
for i, pat in enumerate(patterns):
    axis = find_reflection_axis(pat)

    for mutated_pat in mutate(pat):
        axis_new = find_reflection_axis(mutated_pat, axis)
        if axis_new is None:
            continue

        if axis_new[0] == "h":
            num_hor += axis_new[1]
        else:
            num_vert += axis_new[1]

        break


print(num_hor * 100 + num_vert)
