import sys
import numpy as np


def extrapolate(seq):
    diff = np.diff(seq)
    if (diff == 0.0).all():
        return seq[0]

    extrapolate_diff = extrapolate(diff)
    return seq[0] - extrapolate_diff


seqs = [[int(x) for x in line.strip().split()] for line in sys.stdin]
extrapolations = [extrapolate(seq) for seq in seqs]
print(sum(extrapolations))
