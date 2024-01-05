from heapq import heappop, heappush
import math

input = open('input2.txt').read().splitlines()

source = 'ORE'
target = 'FUEL'
G = {}
productions = {}
productions[source] = None
weights = {}
for line in input:
    left, right = line.split(' => ')
    right = right.split(' ')
    pp = [z for z in left.split(', ')]
    input_chemicals = [(int(x[0]), x[1]) for x in [z.split(' ') for z in left.split(', ')]]
    output_quantity = int(right[0])
    output_chemical = right[1]
    productions[output_chemical] = (output_quantity, input_chemicals)
    if not output_chemical in G:
        G[output_chemical] = []
    for _, v in input_chemicals:
        if v not in G:
            G[v] = []
        G[v].append(output_chemical)

def fill_ranks(G, v, visited, output, current_rank):
    visited.add(v)

    for u in G[v]:
        if u not in visited:
            fill_ranks(G, u, visited, output, current_rank)
    
    output[v] = current_rank[0]
    current_rank[0] += 1

ranks = {}
fill_ranks(G, source, set(), ranks, [0])

Q = []
heappush(Q, (ranks[target], 1, target))

Quantities = {}

while len(Q) > 0:
    current_item = list(heappop(Q))
    while len(Q) > 0:
        if Q[0][2] == current_item[2]:
            _, quantity, _ = heappop(Q)
            current_item[1] += quantity
        else:
            break
    Quantities[current_item[2]] = current_item[1]
    production = productions[current_item[2]]
    if production is None:
        continue

    needed_quantity = current_item[1]
    output_quantity = production[0]
    num_of_applications = math.ceil(needed_quantity / output_quantity)
    for needed_quantity, chemical in production[1]:
        heappush(Q, (ranks[chemical], needed_quantity * num_of_applications, chemical))
    
print(Quantities[source])