import re
import sys
from collections import defaultdict

NUM_REGEX = re.compile(r"[0-9]+")


def find_stars(arr, match_i, match_start_j, match_end_j):
    start_i = max(0, match_i - 1)
    end_i = min(len(arr) - 1, match_i + 1)
    start_j = max(0, match_start_j - 1)
    end_j = min(len(arr[0]) - 1, match_end_j)

    star_poss = []

    for i in range(start_i, end_i + 1):
        for j in range(start_j, end_j + 1):
            if arr[i][j] == "*":
                star_poss.append((i, j))
    return star_poss


arr = sys.stdin.readlines()
star_poss = defaultdict(list)
for i, line in enumerate(arr):
    all_nums = re.finditer(NUM_REGEX, line)
    for match in all_nums:
        stars = find_stars(arr, i, match.start(), match.end())
        for star in stars:
            star_poss[star].append(int(match.group()))

s = 0
for star, nums in star_poss.items():
    if len(nums) == 2:
        s += nums[0] * nums[1]

print(s)
