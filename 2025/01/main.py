import sys


def advance(fro, steps, direction):
    if direction == "L":
        zero_crossings = (steps - fro) // 100 + 1 if steps >= fro else 0
        if fro == 0:
            zero_crossings = max(zero_crossings - 1, 0)
        sign = -1
    else:
        zero_crossings = (steps - (100 - fro)) // 100 + 1 if steps >= 100 - fro else 0
        sign = 1

    to = (fro + sign * steps) % 100
    return to, zero_crossings


def read_input():
    for line in sys.stdin.readlines():
        if line.strip():
            yield line[0], int(line[1:])


if __name__ == "__main__":
    if sys.argv[1] == "1":
        ans = 0
        pos = 50
        for direction, steps in read_input():
            pos, _ = advance(pos, steps, direction)
            if pos == 0:
                ans += 1
        print(ans)
    else:
        ans = 0
        pos = 50
        for direction, steps in read_input():
            pos, zero_crossings = advance(pos, steps, direction)
            ans += zero_crossings
        print(ans)
