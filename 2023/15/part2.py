import sys


def hash_string(s):
    h = 0
    for i in range(len(s)):
        h += ord(s[i])
        h *= 17
        h %= 256
    return h


class LensHash:
    def __init__(self):
        self.boxes = [[] for i in range(256)]

    def set(self, key, value):
        h = hash_string(key)
        box = self.boxes[h]
        for lens in box:
            if lens[0] == key:
                lens[1] = value
                return
        box.append([key, value])

    def remove(self, key):
        h = hash_string(key)
        box = self.boxes[h]
        for i in range(len(box)):
            if box[i][0] == key:
                box.pop(i)
                return

    def focusing_power(self):
        s = 0
        for i, box in enumerate(self.boxes):
            for j, lens in enumerate(box):
                s += (i + 1) * (j + 1) * lens[1]
        return s


strings = sys.stdin.readline().strip().split(",")
hash_table = LensHash()
for str in strings:
    if "=" in str:
        key, value = str.split("=")
        hash_table.set(key, int(value))
    else:
        hash_table.remove(str[:-1])
print(hash_table.focusing_power())
