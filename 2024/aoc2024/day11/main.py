# import functools
from collections import Counter
import sys
from tqdm import trange


def read_input():
    return [int(x.strip()) for x in sys.stdin.readline().split(" ")]


def evolve(x):
    if x == 0:
        yield 1
        return

    s = str(x)
    k = len(s)
    if k % 2 == 0:
        yield from (int(s[: k // 2]), int(s[k // 2 :]))
        return

    yield x * 2024


memo = {}


def evolve_n(nums: Counter[int], n):
    for i in trange(n):
        new_nums = Counter()
        for x in nums:
            for y in evolve(x):
                new_nums[y] += nums[x]
        nums = new_nums
    return nums


def part1():
    nums = evolve_n(Counter(read_input()), 25)
    s = sum(nums[x] for x in nums)
    print(s)


def part2():
    nums = evolve_n(Counter(read_input()), 75)
    s = sum(nums[x] for x in nums)
    print(s)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
