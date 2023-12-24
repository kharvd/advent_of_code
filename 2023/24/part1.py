from dataclasses import dataclass
import sys


@dataclass
class Vec:
    x: int
    y: int
    z: int


@dataclass
class Point:
    pos: Vec
    vel: Vec


def read_points():
    points = []
    for line in sys.stdin:
        pos, vel = line.strip().split(" @ ")
        pos = pos.split(", ")
        vel = vel.split(", ")
        pos = Vec(*(int(x) for x in pos))
        vel = Vec(*(int(x) for x in vel))
        points.append(Point(pos, vel))
    return points


def intersect(point1, point2):
    det = -point1.vel.x * point2.vel.y + point2.vel.x * point1.vel.y
    if det == 0:
        return None
    det_1 = -(point2.pos.x - point1.pos.x) * point2.vel.y + point2.vel.x * (
        point2.pos.y - point1.pos.y
    )
    det_2 = (
        point1.vel.x * (point2.pos.y - point1.pos.y)
        - (point2.pos.x - point1.pos.x) * point1.vel.y
    )
    t_1 = det_1 / det
    t_2 = det_2 / det
    if t_1 < 0 or t_2 < 0:
        return None
    print(t_1, t_2)
    return (point1.pos.x + point1.vel.x * t_1, point1.pos.y + point1.vel.y * t_1)


points = read_points()

boundaries = (200000000000000, 400000000000000)

num_intersections = 0
for i, p1 in enumerate(points):
    for j, p2 in enumerate(points):
        if j <= i:
            continue
        p0 = intersect(p1, p2)
        if (
            p0
            and boundaries[0] <= p0[0] <= boundaries[1]
            and boundaries[0] <= p0[1] <= boundaries[1]
        ):
            num_intersections += 1

print(num_intersections)
