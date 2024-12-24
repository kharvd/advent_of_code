import sys


def read_input():
    inputs = {}
    while line := sys.stdin.readline().strip():
        name, value = line.split(": ")
        value = bool(int(value))
        inputs[name] = value

    outputs = {}
    while line := sys.stdin.readline().strip():
        x, rest = line.split(" ", 1)
        op, rest = rest.split(" ", 1)
        y, res = rest.split(" -> ")
        outputs[res] = (op, x, y)
    return inputs, outputs


def compute(inputs, outputs, name):
    if name in inputs:
        return inputs[name]

    op, a, b = outputs[name]
    a_val = compute(inputs, outputs, a)
    b_val = compute(inputs, outputs, b)
    if op == "XOR":
        return a_val ^ b_val
    if op == "OR":
        return a_val or b_val
    if op == "AND":
        return a_val and b_val


def bits_to_int(bits):
    x = 0
    for i in range(64):
        x = x | (bits.get(i, 0) << i)
    return x


def part1():
    inputs, outputs = read_input()
    z_values = {}
    for name in outputs.keys():
        if name[0] == "z":
            z_values[int(name[1:])] = compute(inputs, outputs, name)
    print(bits_to_int(z_values))


def part2():
    pass


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
