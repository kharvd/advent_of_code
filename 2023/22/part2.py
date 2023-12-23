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
    return Brick(
        brick.id,
        Point(brick.start.x, brick.start.y, new_start_z),
        Point(brick.end.x, brick.end.y, new_end_z),
    )


def arrange_bricks(bricks):
    bricks = sorted(bricks, key=lambda brick: brick.start.z)
    max_x = max(bricks, key=lambda brick: brick.end.x).end.x
    max_y = max(bricks, key=lambda brick: brick.end.y).end.y
    max_z = max(bricks, key=lambda brick: brick.end.z).end.z

    space = [
        [[None for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for _ in range(max_z + 1)
    ]

    new_bricks = []
    moved_bricks_count = 0
    for brick in bricks:
        new_brick = place_brick(brick, space)
        if new_brick.start.z != brick.start.z:
            moved_bricks_count += 1
        new_bricks.append(new_brick)

    return space, new_bricks, moved_bricks_count


space, bricks, _ = arrange_bricks(read_bricks())

count = 0
for brick in bricks:
    _, _, moved_bricks_count = arrange_bricks([b for b in bricks if b != brick])
    count += moved_bricks_count
print(count)
