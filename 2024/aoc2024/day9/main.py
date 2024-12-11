import sys


def read_input():
    return sys.stdin.readline().strip()


def part1():
    inp = read_input()
    fb = [int(c) for c in inp[::2]]
    sp = [int(c) for c in inp[1::2]]
    cs = 0
    i = 0
    c = 0
    while i < len(fb):
        fbi = fb[i]
        for j in range(c, c + fbi):
            cs += j * i
            fb[i] -= 1

        c += fbi

        for j in range(c, c + sp[i]):
            while len(fb) > 0 and fb[-1] == 0:
                fb.pop()
            if len(fb) == 0:
                break
            fb[-1] -= 1
            idx = len(fb) - 1
            cs += j * idx
        c += sp[i]

        i += 1
    print(cs)


def part2():
    inp = read_input()
    fb = [int(c) for c in inp[::2]]
    sp = [int(c) for c in inp[1::2]]

    sp_pos = []
    new_pos = []
    c = 0
    for i in range(len(fb)):
        new_pos.append(c)
        c += fb[i]
        if i < len(sp):
            sp_pos.append(c)
            c += sp[i]

    for fi in range(len(fb) - 1, -1, -1):
        for si in range(fi):
            if sp[si] >= fb[fi]:
                new_pos[fi] = sp_pos[si]
                sp[si] -= fb[fi]
                sp_pos[si] += fb[fi]
                break

    cs = 0
    for i in range(len(fb)):
        for j in range(new_pos[i], new_pos[i] + fb[i]):
            cs += i * j
    print(cs)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
