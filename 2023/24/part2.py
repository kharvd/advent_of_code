from dataclasses import dataclass
from sympy import solve, var
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

    def x_at(self, t):
        return self.pos.x + self.vel.x * t

    def y_at(self, t):
        return self.pos.y + self.vel.y * t

    def z_at(self, t):
        return self.pos.z + self.vel.z * t


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


points = read_points()
x, y, z, vx, vy, vz, t0, t1, t2 = var("x,y,z,vx,vy,vz,t0,t1,t2")

init_point = Point(Vec(x, y, z), Vec(vx, vy, vz))

solutions = solve(
    [
        init_point.x_at(t0) - points[0].x_at(t0),
        init_point.y_at(t0) - points[0].y_at(t0),
        init_point.z_at(t0) - points[0].z_at(t0),
        init_point.x_at(t1) - points[1].x_at(t1),
        init_point.y_at(t1) - points[1].y_at(t1),
        init_point.z_at(t1) - points[1].z_at(t1),
        init_point.x_at(t2) - points[2].x_at(t2),
        init_point.y_at(t2) - points[2].y_at(t2),
        init_point.z_at(t2) - points[2].z_at(t2),
    ],
    [x, y, z, vx, vy, vz, t0, t1, t2],
)

assert isinstance(solutions, list)
assert len(solutions) == 1

sol = solutions[0]
print(sol[0] + sol[1] + sol[2])
