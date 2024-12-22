from collections import defaultdict
import sys


def read_input():
    return [int(line) for line in sys.stdin.readlines() if line.strip()]


def compute_hash(x):
    y = x * 64
    x = mix(y, x)
    x = prune(x)

    y = x // 32
    x = mix(y, x)
    x = prune(x)

    y = x * 2048
    x = mix(y, x)
    x = prune(x)

    return x


def mix(y, x):
    return y ^ x


def prune(x):
    return x % 16777216


def iterate_hash(x, k):
    for _ in range(k):
        x = compute_hash(x)
    return x


def scan_hash(x, k):
    res = [x % 10]
    for _ in range(k):
        x = compute_hash(x)
        res.append(x % 10)
    return res


def part1():
    s = 0
    for num in read_input():
        s += iterate_hash(num, 2000)
    print(s)


def diff(xs):
    return [None] + [xs[i] - xs[i - 1] for i in range(1, len(xs))]


def part2():
    secrets = []
    diffs = []
    for num in read_input():
        s = scan_hash(num, 2000)
        secrets.append(s)
        diffs.append(diff(s))

    seq_tups = defaultdict(int)
    for sec, dif in zip(secrets, diffs):
        tups = {}
        for i in range(len(dif) - 4):
            tup = tuple(dif[i : i + 4])
            s = sec[i + 3]
            if tup not in tups:
                tups[tup] = s

        for t, s in tups.items():
            seq_tups[t] += s

    print(max(seq_tups.values()))


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
