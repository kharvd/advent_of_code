import functools
import sys


directional = [["#", "^", "A"], ["<", "v", ">"]]

numerical = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["#", "0", "A"]]

delta_dir = {"v": (1, 0), ">": (0, 1), "<": (0, -1), "^": (-1, 0), "A": (0, 0)}


def read_input():
    return [l.strip() for l in sys.stdin.readlines()]


def find_last_directional_transitions(nums):
    seqs = [[]]
    num = "A"
    for n in nums:
        new_seqs = [seq + nt + ["A"] for seq in seqs for nt in ntransitions[(num, n)]]
        seqs = new_seqs
        num = n

    return seqs


def manhattan(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def build_transitions(field, a, b):
    def neighbors(node):
        i, j = node
        for dir, (di, dj) in delta_dir.items():
            ni, nj = i + di, j + dj
            if (
                0 <= ni < len(field)
                and 0 <= nj < len(field[0])
                and manhattan((ni, nj), b) < manhattan(node, b)
                and field[ni][nj] != "#"
            ):
                yield (ni, nj), dir

    def dfs(node):
        if node == b:
            return [[]]
        paths = []
        for n, dr in neighbors(node):
            paths_node = dfs(n)
            paths.extend([[dr] + p for p in paths_node])
        return paths

    return dfs(a)


def single_step_transitions(field):
    ntransitions = {}
    for i in range(len(field)):
        for j in range(len(field[0])):
            for k in range(len(field)):
                for l in range(len(field[0])):
                    n1 = field[i][j]
                    n2 = field[k][l]
                    if n1 == "#" or n2 == "#":
                        continue

                    ntransitions[(n1, n2)] = build_transitions(field, (i, j), (k, l))
    return ntransitions


ntransitions = single_step_transitions(numerical)
transitions = {
    k: [t + ["A"] for t in tr] for k, tr in single_step_transitions(directional).items()
}


@functools.cache
def transition_length(fro, to, depth):
    if depth == 1:
        min_length = len(transitions[(fro, to)][0])
        return min_length

    min_length = float("inf")
    for trans in transitions[(fro, to)]:
        s = 0
        state = "A"
        for num in trans:
            s += transition_length(state, num, depth - 1)
            state = num
        min_length = min(min_length, s)

    return min_length


def solve(num_directional):
    total = 0
    for code in read_input():
        min_l = float("inf")
        for seq in find_last_directional_transitions(code):
            l = 0
            state = "A"
            for num in seq:
                l += transition_length(state, num, num_directional)
                state = num
            min_l = min(min_l, l)

        print(code, min_l)
        complexity = min_l * int(code[:3])
        total += complexity

    print(total)


def part1():
    solve(2)


def part2():
    solve(25)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
