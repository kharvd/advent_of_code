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
    d1, d2, n = state
    clicked1, clicked2, clicked3 = None, None, None
    nd1, clicked1 = advance_field(directional, d1, inp)
    if nd1 is None:
        return None, clicked1, clicked2, clicked3
    if clicked1 is None:
        return (nd1, d2, n), clicked1, clicked2, clicked3

    nd2, clicked2 = advance_field(directional, d2, clicked1)
    if nd2 is None:
        return None, clicked1, clicked2, clicked3
    if clicked2 is None:
        return (nd1, nd2, n), clicked1, clicked2, clicked3

    nn, clicked3 = advance_field(numerical, n, clicked2)
    if nn is None:
        return None, clicked1, clicked2, clicked3
    if clicked3 is None:
        return (nd1, nd2, nn), clicked1, clicked2, clicked3

    return (nd1, nd2, nn), clicked1, clicked2, clicked3


def decode_field(field, d):
    return field[d[0]][d[1]]


def decode_state(state):
    d1, d2, n = state
    return (
        decode_field(directional, d1),
        decode_field(directional, d2),
        decode_field(numerical, n),
    )


def neighbors(state):
    for inp in delta_dir.keys():
        new_state, c1, c2, c3 = advance(state, inp)
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


def encode_num(num):
    ni, nj = None, None
    for i in range(len(numerical)):
        for j in range(len(numerical[0])):
            if numerical[i][j] == num:
                ni, nj = i, j
                break
    return (dir_start, dir_start, (ni, nj))


def execute_program(state, program):
    clicked1 = []
    clicked2 = []
    clicked3 = []
    for c in program:
        state, c1, c2, c3 = advance(state, c)
        if c1:
            clicked1.append(c1)
        if c2:
            clicked2.append(c2)
        if c3:
            clicked3.append(c3)
    return state, (clicked1, clicked2, clicked3)


def find_sequence(nums):
    seq = []
    state = (dir_start, dir_start, num_start)
    for num in nums:
        end = encode_num(num)
        seq.extend(bfs(state, end))
        seq.append("A")
        state = end
    return seq


def part1():
    total = 0
    for code in read_input():
        seq = find_sequence(code)
        complexity = len(seq) * int(code[:3])
        total += complexity

    print(total)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
