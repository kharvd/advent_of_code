from dataclasses import dataclass
import sys

WIDTH = 101
HEIGHT = 103


@dataclass
class Robot:
    p: tuple[int, int]
    v: tuple[int, int]


def read_input():
    robots = []
    while line := sys.stdin.readline().strip():
        p, v = line.split(" ")
        p = tuple(int(x) for x in p[2:].split(","))
        v = tuple(int(x) for x in v[2:].split(","))
        robots.append(Robot(p, v))
    return robots


def evolve(robot, steps):
    i = (robot.p[1] + robot.v[1] * steps) % HEIGHT
    j = (robot.p[0] + robot.v[0] * steps) % WIDTH
    return Robot((j, i), robot.v)


def render_pos(pos):
    field = [[0] * WIDTH for _ in range(HEIGHT)]
    for j, i in pos:
        field[i][j] += 1
    return field


def print_pos(pos):
    field = render_pos(pos)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            print("." if field[i][j] == 0 else field[i][j], end="")
        print()


def check_pos(pos):
    field = render_pos(pos)
    for i in range(HEIGHT):
        line = "".join(str(x) for x in field[i])
        if "1111111111" in line:
            return True
    return False


def part1():
    robots = read_input()
    final_pos = [evolve(r, 100) for r in robots]
    q = [[0, 0], [0, 0]]
    for r in final_pos:
        j, i = r.p
        if i != HEIGHT // 2 and j != WIDTH // 2:
            q[i > HEIGHT // 2][j > WIDTH // 2] += 1
    print(q[0][0] * q[0][1] * q[1][0] * q[1][1])


def part2():
    robots = read_input()
    for i in range(1, WIDTH * HEIGHT + 1):
        robots = [evolve(r, 1) for r in robots]
        pos = [r.p for r in robots]
        if check_pos(pos):
            print_pos(pos)
            print(i)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
