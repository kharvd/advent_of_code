from dataclasses import dataclass
import sys


def read_input():
    pats = sys.stdin.readline().strip().split(", ")
    sys.stdin.readline()
    designs = [s.strip() for s in sys.stdin.readlines()]
    return pats, designs


def assemble(pats, design):
    a = [0] * (len(design) + 1)
    a[0] = 1
    for i in range(1, len(design) + 1):
        for pat in pats:
            if len(pat) <= i:
                slc = design[i - len(pat) : i]
                assert len(slc) == len(pat)
                if slc == pat:
                    a[i] += a[i - len(pat)]
    return a[-1]


def part1():
    pats, designs = read_input()
    c = 0
    for design in designs:
        if assemble(pats, design) > 0:
            c += 1
    print(c)


def part2():
    pats, designs = read_input()
    c = 0
    for design in designs:
        c += assemble(pats, design)
    print(c)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
