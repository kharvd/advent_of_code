import sys


def read_input():
    eqs = []
    while line := sys.stdin.readline():
        lhs, rhs = line.split(":")
        lhs = int(lhs)
        rhs = [int(s) for s in rhs.strip().split(" ")]
        eqs.append((lhs, rhs))
    return eqs


def print_expr(rhs, ops_mask):
    print(rhs[0], end="")
    for i in range(len(rhs) - 1):
        if (ops_mask << i) & 1 == 0:
            print(f"+{rhs[i+1]}", end="")
        else:
            print(f"*{rhs[i+1]}", end="")


def print_expr3(rhs, ops):
    print(rhs[0], end="")
    for i in range(len(rhs) - 1):
        if ops[i] == 0:
            print(f"+{rhs[i+1]}", end="")
        elif ops[i] == 1:
            print(f"*{rhs[i+1]}", end="")
        else:
            print(f"||{rhs[i+1]}", end="")


def compute_result(rhs, ops_mask):
    res = rhs[0]
    for i in range(len(rhs) - 1):
        if (ops_mask >> i) & 1 == 0:
            res += rhs[i + 1]
        else:
            res *= rhs[i + 1]
    return res


def compute_result3(rhs, ops):
    res = rhs[0]
    for i in range(len(rhs) - 1):
        if ops[i] == 0:
            res += rhs[i + 1]
        elif ops[i] == 1:
            res *= rhs[i + 1]
        else:
            res = int(str(res) + str(rhs[i + 1]))
    return res


def next_ops(ops):
    carry = 1
    for i in range(len(ops)):
        carry, ops[i] = (ops[i] + carry) // 3, (ops[i] + carry) % 3

    if carry == 1:
        return False
    return True


def part1():
    eqs = read_input()
    result = 0
    for lhs, rhs in eqs:
        for mask in range(0, 2 ** (len(rhs) - 1)):
            if lhs == compute_result(rhs, mask):
                print_expr(rhs, mask)
                print(f"={lhs}")
                result += lhs
                break
    print(result)


def part2():
    eqs = read_input()
    result = 0
    for lhs, rhs in eqs:
        ops = [0] * (len(rhs) - 1)
        while True:
            if lhs == compute_result3(rhs, ops):
                print_expr3(rhs, ops)
                print(f"={lhs}")
                result += lhs
                break
            if not next_ops(ops):
                break

    print(result)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
