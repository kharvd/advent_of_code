from collections import deque
from heapq import heappop, heappush
import sys


directional = [["#", "^", "A"], ["<", "v", ">"]]
dir_start = (0, 2)

numerical = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["#", "0", "A"]]
num_start = (3, 2)

delta_dir = {"v": (1, 0), ">": (0, 1), "<": (0, -1), "^": (-1, 0), "A": (0, 0)}


def advance_field(field, d, inp):
    if inp == "A":
        return d, field[d[0]][d[1]]

    i, j = d
    di, dj = delta_dir[inp]
    ni, nj = i + di, j + dj
    if 0 <= ni < len(field) and 0 <= nj < len(field[0]) and field[ni][nj] != "#":
        return (ni, nj), None
    return None, None


def advance(state, inp):
    ds = list(state)
    clickeds = [None] * len(ds)

    last_clicked = inp
    for i in range(len(ds)):
        ndi, clicked_i = advance_field(
            directional if i < len(ds) - 1 else numerical, ds[i], last_clicked
        )
        if ndi is None:
            return None, None
        ds = ds[:i] + [ndi] + ds[i + 1 :]
        if clicked_i is None:
            return tuple(ds), clickeds
        clickeds[i] = clicked_i
        last_clicked = clicked_i

    return tuple(ds), clickeds


def decode_field(field, d):
    return field[d[0]][d[1]]


def decode_state(state):
    res = []
    for d in state[:-1]:
        res.append(decode_field(directional, d))
    res.append(decode_field(numerical, state[-1]))

    return tuple(res)


def neighbors(state):
    for inp in delta_dir.keys():
        new_state, _ = advance(state, inp)
        if new_state is not None:
            yield inp, new_state


def bfs(start, end):
    q = deque()
    paths = {}
    q.append(start)
    paths[start] = []

    while q:
        v = q.popleft()

        for inp, n in neighbors(v):
            if n not in paths:
                paths[n] = paths[v] + [inp]
                q.append(n)
    # print({decode_state(n): "".join(p) for n, p in paths.items()})

    return paths[end]


def read_input():
    return [l.strip() for l in sys.stdin.readlines()]


def encode_num(num, num_directional):
    ni, nj = None, None
    for i in range(len(numerical)):
        for j in range(len(numerical[0])):
            if numerical[i][j] == num:
                ni, nj = i, j
                break
    return tuple([*([dir_start] * num_directional), (ni, nj)])


def execute_program(state, program):
    clicked = []
    for c in program:
        state, cl = advance(state, c)
        if cl is not None:
            print(cl)
        if cl is not None and cl[-1] is not None:
            clicked.extend(cl[-1])
    return state, clicked


def find_sequence(nums, num_directional):
    seq = []
    state = encode_num("A", num_directional)
    for num in nums:
        end = encode_num(num, num_directional)
        seq.extend(bfs(state, end))
        seq.append("A")
        state = end
    return seq


def part1():
    total = 0
    for code in read_input():
        seq = find_sequence(code, 2)
        complexity = len(seq) * int(code[:3])
        total += complexity

    print(total)


def part2():
    total = 0
    for code in read_input():
        seq = find_sequence(code, 25)
        complexity = len(seq) * int(code[:3])
        total += complexity

    print(total)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
