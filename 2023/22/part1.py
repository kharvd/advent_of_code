from dataclasses import dataclass
import sys


@dataclass
class Point:
    x: int
    y: int
    z: int


@dataclass
class Brick:
    id: int
    start: Point
    end: Point


def read_bricks():
    bricks = []
    for i, line in enumerate(sys.stdin):
        start, end = line.strip().split("~")
        start_point = Point(*map(int, start.split(",")))
        end_point = Point(*map(int, end.split(",")))
        if start_point.z > end_point.z:
            start_point, end_point = end_point, start_point
        bricks.append(Brick(i, start_point, end_point))
    return bricks


def can_place_brick(brick, start_z, space, ignore_brick=None):
    for x in range(brick.start.x, brick.end.x + 1):
        for y in range(brick.start.y, brick.end.y + 1):
            if (
                space[start_z][x][y] is not None
                and space[start_z][x][y] != ignore_brick
            ):
                return False
    return True


def place_brick(brick, space):
    new_start_z = brick.start.z
    new_end_z = brick.end.z
    for z in range(brick.start.z - 1, 0, -1):
        if not can_place_brick(brick, z, space):
            break
        new_start_z = z
        new_end_z = z + brick.end.z - brick.start.z
    for z in range(new_start_z, new_end_z + 1):
        for x in range(brick.start.x, brick.end.x + 1):
            for y in range(brick.start.y, brick.end.y + 1):
                space[z][x][y] = brick
    brick.start.z = new_start_z
    brick.end.z = new_end_z


def arrange_bricks(bricks):
    bricks.sort(key=lambda brick: brick.start.z)
    max_x = max(bricks, key=lambda brick: brick.end.x).end.x
    max_y = max(bricks, key=lambda brick: brick.end.y).end.y
    max_z = max(bricks, key=lambda brick: brick.end.z).end.z

    space = [
        [[None for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for _ in range(max_z + 1)
    ]

    for brick in bricks:
        place_brick(brick, space)

    return space


def can_disintegrate(brick, space):
    if brick.start.z == len(space) - 1:
        return True
    for x in range(brick.start.x, brick.end.x + 1):
        for y in range(brick.start.y, brick.end.y + 1):
            brick_above = space[brick.end.z + 1][x][y]
            if brick_above is not None:
                if can_place_brick(brick_above, brick.end.z, space, ignore_brick=brick):
                    return False
    return True


bricks = read_bricks()
space = arrange_bricks(bricks)

count = 0
for brick in bricks:
    if can_disintegrate(brick, space):
        count += 1
print(count)

# print(space)

# for x in range(len(space[0])):
#     print(f"{x:>4}", end="|")
# print()
# for z in range(len(space) - 1, -1, -1):
#     for x in range(len(space[0])):
#         c = "."
#         for y in range(len(space[0][0])):
#             if space[z][x][y] is not None:
#                 c = str(space[z][x][y].id)
#                 break
#         print(f"{c:>4}", end="|")
#     print("", z)
