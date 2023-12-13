import functools
import sys
import tqdm


@functools.cache
def count_options(pat, groups, pat_i, groups_i):
    if pat[pat_i] == "e":
        if groups[groups_i] == "x":
            return 1
        else:
            return 0

    if groups[groups_i] == "x":
        if pat[pat_i] == "#":
            return 0
        else:
            return count_options(pat, groups, pat_i - 1, groups_i)

    if groups[groups_i] == "y":
        if pat[pat_i] == "#":
            return count_options(pat, groups, pat_i, groups_i - 1)
        else:
            return count_options(pat, groups, pat_i - 1, groups_i) + count_options(
                pat, groups, pat_i, groups_i - 1
            )
    if groups[groups_i] == "#":
        if pat[pat_i] == "#" or pat[pat_i] == "?":
            return count_options(pat, groups, pat_i - 1, groups_i - 1)
        else:
            return 0
    if groups[groups_i] == ".":
        if pat[pat_i] == "." or pat[pat_i] == "?":
            return count_options(pat, groups, pat_i - 1, groups_i - 1) + count_options(
                pat, groups, pat_i - 1, groups_i
            )
        else:
            return 0
    assert False


s = 0
multiplier = 5
for line in tqdm.tqdm(sys.stdin.readlines()):
    pat, xs = line.strip().split()
    xs = [int(x) for x in xs.split(",")]
    s1 = "e" + ("?".join([pat] * multiplier))
    s2 = "x" + ".".join([".".join(["#" * x for x in xs])] * multiplier) + "y"
    c = count_options(s1, s2, len(s1) - 1, len(s2) - 1)
    s += c
print(s)
