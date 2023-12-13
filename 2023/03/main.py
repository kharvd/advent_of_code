import re
import sys

NUM_REGEX = re.compile(r"[0-9]+")


def should_count(arr, match_i, match_start_j, match_end_j):
    start_i = max(0, match_i - 1)
    end_i = min(len(arr) - 1, match_i + 1)
    start_j = max(0, match_start_j - 1)
    end_j = min(len(arr[0]) - 1, match_end_j)

    for i in range(start_i, end_i + 1):
        for j in range(start_j, end_j + 1):
            if arr[i][j].isdigit():
                continue
            if arr[i][j] == "\n":
                continue
            if arr[i][j] != ".":
                return True
    return False


arr = sys.stdin.readlines()
s = 0
for i, line in enumerate(arr):
    all_nums = re.finditer(NUM_REGEX, line)
    for match in all_nums:
        if should_count(arr, i, match.start(), match.end()):
            s += int(match.group())

print(s)
