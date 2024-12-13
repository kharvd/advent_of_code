from dataclasses import dataclass
from sympy import solve
from sympy.abc import a, b
import sys


@dataclass
class Eq:
    xa: int
    xb: int
    ya: int
    yb: int
    x: int
    y: int


def read_input():
    eqs = []
    while lineA := sys.stdin.readline().strip():
        lineB = sys.stdin.readline().strip()
        lineP = sys.stdin.readline().strip()
        sys.stdin.readline()

        xa, ya = lineA.split(", Y+")
        xa = int(xa.split("+")[1])
        ya = int(ya)

        xb, yb = lineB.split(", Y+")
        xb = int(xb.split("+")[1])
        yb = int(yb)

        x, y = lineP.split(", Y=")
        x = int(x.split("=")[1])
        y = int(y)

        eqs.append(Eq(xa, xb, ya, yb, x, y))

    return eqs


def solve_eq(eq):
    solution = solve(
        (eq.xa * a + eq.xb * b - eq.x, eq.ya * a + eq.yb * b - eq.y), (a, b)
    )

    if not solution:
        return None

    sa = solution[a]
    sb = solution[b]

    if not (sa.is_integer and sb.is_integer and sa >= 0 and sb >= 0):
        return None

    return sa, sb


def part1():
    eqs = read_input()
    result = 0
    for eq in eqs:
        solution = solve_eq(eq)
        if solution:
            a, b = solution
            result += a * 3 + b
    print(result)


def part2():
    eqs = read_input()
    result = 0
    for eq in eqs:
        solution = solve_eq(
            Eq(eq.xa, eq.xb, eq.ya, eq.yb, eq.x + 10000000000000, eq.y + 10000000000000)
        )
        if solution:
            a, b = solution
            result += a * 3 + b
    print(result)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
