import sys


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


instructions = sys.stdin.readline().strip()
sys.stdin.readline()

graph = {}
while line := sys.stdin.readline().strip():
    fro, to = line.strip().split(" = ")
    to = to[1:-1].split(", ")
    graph[fro] = to

start_nodes = [node for node in graph if node.endswith("A")]
loop_lengths = []
for node in start_nodes:
    num_steps = 0
    curr_i = 0
    while not node.endswith("Z"):
        node = graph[node][0 if instructions[curr_i] == "L" else 1]
        curr_i += 1
        curr_i %= len(instructions)
        num_steps += 1
    loop_lengths.append(num_steps)


min_total_length = loop_lengths[0]
for i in range(len(loop_lengths)):
    min_total_length = lcm(min_total_length, loop_lengths[i])

print(min_total_length)
