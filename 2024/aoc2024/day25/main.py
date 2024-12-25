import sys

num_pins = 5


def read_key_lock():
    line = sys.stdin.readline().strip()
    if not line:
        return None

    is_key = line == "....."
    pat = [0 if is_key else 1] * num_pins
    while line := sys.stdin.readline().strip():
        for i in range(num_pins):
            if line[i] == "#":
                pat[i] += 1

    pat = [p - 1 for p in pat]
    return is_key, pat


def read_input():
    key_locks = []
    while kl := read_key_lock():
        key_locks.append(kl)
    return key_locks


def match(kl1, kl2):
    return all(x + y <= 5 for x, y in zip(kl1[1], kl2[1]))


def part1():
    kls = read_input()
    c = 0
    for i in range(len(kls)):
        for j in range(i + 1, len(kls)):
            if (kls[i][0] ^ kls[j][0]) and match(kls[i], kls[j]):
                c += 1
    print(c)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
