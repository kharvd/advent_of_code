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


def find_horizontal_axis(pat):
    for i in range(1, len(pat)):
        if does_reflect_horizontal(pat, i):
            return i
    return None


def find_vertical_axis(pat):
    for j in range(1, len(pat[0])):
        if does_reflect_vertical(pat, j):
            return j
    return None


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
for pat in patterns:
    if j := find_vertical_axis(pat):
        num_vert += j
    elif i := find_horizontal_axis(pat):
        num_hor += i

print(num_hor * 100 + num_vert)
