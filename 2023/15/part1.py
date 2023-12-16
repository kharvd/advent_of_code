import sys


def hash_string(s):
    h = 0
    for i in range(len(s)):
        h += ord(s[i])
        h *= 17
        h %= 256
    return h


strings = sys.stdin.readline().strip().split(",")
hashes = [hash_string(s) for s in strings]
print(sum(hashes))
