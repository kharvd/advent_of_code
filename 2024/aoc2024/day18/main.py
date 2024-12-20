from collections import defaultdict, deque
from heapq import heappop, heappush
import sys


WIDTH = 71
HEIGHT = 71


def read_input():
    result = []
    while line := sys.stdin.readline().strip():
        x, y = (int(s) for s in line.split(","))
        result.append((x, y))
    return result


def make_field(bytes, limit):
    field = defaultdict(lambda: True)
    for i in range(limit):
        field[bytes[i]] = False

    assert len(field) == limit
    return field


def print_field(field):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print("." if field[(x, y)] else "#", end="")
        print()


deltas = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def neighbors(field, node):
    x, y = node
    for dx, dy in deltas:
        if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT and field[(x + dx, y + dy)]:
            yield (x + dx, y + dy)


def bfs(field, start, end):
    dists = {start: 0}
    q = deque()
    q.append(start)

    while q:
        v = q.popleft()

        for n in neighbors(field, v):
            if n not in dists:
                dists[n] = dists[v] + 1
                q.append(n)

    return dists.get(end, float("inf"))


def part1():
    field = make_field(read_input(), limit=1024)
    print_field(field)
    start = (0, 0)
    end = (WIDTH - 1, HEIGHT - 1)
    print(bfs(field, start, end))


def part2():
    bytes = read_input()

    start = (0, 0)
    end = (WIDTH - 1, HEIGHT - 1)

    for limit in range(1024, len(bytes)):
        dist = bfs(make_field(bytes, limit), start, end)
        if dist == float("inf"):
            print(bytes[limit - 1])
            break


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
