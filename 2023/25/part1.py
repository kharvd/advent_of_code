import sys
from collections import defaultdict, deque

sys.setrecursionlimit(100000)


graph = defaultdict(set)
edges = set()
for line in sys.stdin:
    fro, to = line.strip().split(": ")
    to = to.split(" ")

    for t in to:
        if (fro, t) not in edges and (t, fro) not in edges:
            edges.add((fro, t))

        graph[fro].add(t)
        graph[t].add(fro)


def max_flow(s, t):
    flow = 0
    edge_flow = defaultdict(int)

    def find_path(s, t):
        visited = set()
        prev = {}
        queue = deque([s])
        while len(queue) > 0:
            node = queue.popleft()
            if node == t:
                break
            for n in graph[node]:
                if n not in visited and edge_flow[(node, n)] < 1:
                    visited.add(n)
                    prev[n] = node
                    queue.append(n)

        if t not in prev:
            return None

        path = []
        node = t
        while node != s:
            path.append((prev[node], node))
            node = prev[node]

        return path

    def augment(path):
        for fro, to in path:
            edge_flow[(fro, to)] += 1
            edge_flow[(to, fro)] -= 1
        return 1

    while True:
        path = find_path(s, t)
        if path is None:
            break
        flow += augment(path)
    return flow


s = next(iter(graph.keys()))
s_component = {s}
for t in graph.keys():
    if t == s:
        continue

    flow = max_flow(s, t)
    if flow != 3:
        s_component.add(t)

print(len(s_component) * (len(graph) - len(s_component)))
