from queue import Queue

input = open('input2.txt').read().splitlines()

G = {}
for line in input:
    v, u = line.split(')')
    if u not in G:
        G[u] = []
    if v not in G:
        G[v] = []

    G[u].append(v)
    G[v].append(u)

def shortest_path(G, source, target):
    visited = set()
    q = Queue()
    q.put((source, 0))
    visited.add(source)

    while q.empty() == False:
        u, dist = q.get()
        if u == target:
            return dist
        for v in G[u]:
            if v not in visited:
                visited.add(v)
                q.put((v, dist + 1))
    
source = 'YOU'
target = 'SAN'
result = shortest_path(G, source, target) - 2

print(result)