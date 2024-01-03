input = open('input2.txt').read().splitlines()

G = {}
for line in input:
    v, u = line.split(')')
    if u not in G:
        G[u] = []
    if v not in G:
        G[v] = []

    G[u].append(v)

def DFS(G, u, cache):
    if u in cache:
        return cache[u]
    result = 0
    for v in G[u]:
        result += DFS(G, v, cache) + 1
    
    cache[u] = result
    return result

result = 0
cache = {}
for u in G.keys():
    result += DFS(G, u, cache)

print(result)