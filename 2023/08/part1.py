import sys


instructions = sys.stdin.readline().strip()
sys.stdin.readline()

graph = {}
while line := sys.stdin.readline().strip():
    fro, to = line.strip().split(" = ")
    to = to[1:-1].split(", ")
    graph[fro] = to


current_node = "AAA"
num_steps = 0
curr_i = 0
while current_node != "ZZZ":
    current_node = graph[current_node][0 if instructions[curr_i] == "L" else 1]
    curr_i += 1
    curr_i %= len(instructions)
    num_steps += 1

print(num_steps)
