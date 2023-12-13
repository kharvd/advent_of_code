import sys
import tqdm


def count_options(pat, groups):
    num_qs = pat.count("?")
    num_matches = 0
    for i in range(2**num_qs):
        bits = bin(i)[2:].zfill(num_qs)

        result = []
        j = 0
        for i, c in enumerate(pat):
            if c == "?":
                result.append("#" if bits[j] == "1" else ".")
                j += 1
            else:
                result.append(c)

        group_counts = []
        last_group_count = 0
        for c in result:
            if c == "#":
                last_group_count += 1
            else:
                if last_group_count > 0:
                    group_counts.append(last_group_count)
                last_group_count = 0
        if last_group_count > 0:
            group_counts.append(last_group_count)

        if group_counts == groups:
            num_matches += 1

    return num_matches


s = 0
for line in tqdm.tqdm(sys.stdin.readlines()):
    pat, xs = line.strip().split()
    xs = [int(x) for x in xs.split(",")]
    s += count_options(pat, xs)
print(s)
