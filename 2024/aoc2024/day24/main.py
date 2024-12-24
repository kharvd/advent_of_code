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


def draw_circuit(outputs):
    from graphviz import Digraph

    dot = Digraph(comment="Simple Graph Example")
    for out, (op, a, b) in outputs.items():
        dot.node(out, f"{out} ({op})")
        dot.edge(a, out)
        dot.edge(b, out)
    dot.render("graph", format="svg", cleanup=True)


def compute_z(inputs, outputs):
    z_values = {}
    for name in outputs.keys():
        if name[0] == "z":
            z_values[int(name[1:])] = compute(inputs, outputs, name)
    return bits_to_int(z_values)


def part1():
    inputs, outputs = read_input()
    print(compute_z(inputs, outputs))


def encode_input(x, y):
    inputs = {}
    for i in range(45):
        inputs[f"x{i:02}"] = bool(x & (1 << i))
        inputs[f"y{i:02}"] = bool(y & (1 << i))
    return inputs


def part2():
    inputs, outputs = read_input()
    # draw_circuit(outputs)

    outputs["svm"], outputs["nbc"] = outputs["nbc"], outputs["svm"]
    outputs["z15"], outputs["kqk"] = outputs["kqk"], outputs["z15"]
    outputs["z23"], outputs["cgq"] = outputs["cgq"], outputs["z23"]
    outputs["z39"], outputs["fnr"] = outputs["fnr"], outputs["z39"]

    # check single bit additions
    for i in range(45):
        x = 1 << i
        y = 1 << i
        inputs = encode_input(x, y)
        z = compute_z(inputs, outputs)
        if x + y != z:
            print(i, x, y, z)
            # print(compute(inputs, outputs, "z06"))

    print(",".join(sorted(["svm", "nbc", "z15", "kqk", "z23", "cgq", "z39", "fnr"])))


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
