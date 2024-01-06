from queue import Queue
from heapq import heappush, heappop

input = open('input2.txt').read().splitlines()

n = len(input)
m = len(input[0])

def build_graph(maze: list, starting_nodes: set, directions: list, teleports: dict) -> dict:
    result = {x: [] for x in starting_nodes}
    n = len(maze)
    m = len(maze[0])
    for pos in starting_nodes:
        Q = Queue()
        Q.put((pos, 0))
        visited = {pos}
        while Q.empty() == False:
            position, distance = Q.get()
            if position != pos and position in starting_nodes:
                result[pos].append((position, distance))

            for di, dii in directions:
                new_i, new_ii = position[0] + di, position[1] + dii
                new_position = (new_i, new_ii)
                if new_position in teleports:
                    new_position = teleports[new_position]
                if maze[new_position[0]][new_position[1]] == '.' and new_position not in visited:
                    visited.add(new_position)
                    Q.put((new_position, distance + 1))
    
    for key, v in teleports.items():
        if key in ['AA', 'ZZ']:
            continue
        if 6 <= v[0][1][0] <= n - 6 and 6 <= v[0][1][1] <= m - 6:
            result[v[0][1]].append((v[1][1], 1, 1))
            result[v[1][1]].append((v[0][1], 1, -1))
        else:
            result[v[0][1]].append((v[1][1], 1, -1))
            result[v[1][1]].append((v[0][1], 1, 1))
    return result


def add_teleport(teleports, tag, position):
    if tag not in teleports:
        teleports[tag] = []
    teleports[tag].append(position)

teleports = {}
end = ()
start = ()
for i in range(n):
    for ii in range(2, m - 1):
        if input[i][ii] == '.':
            if input[i][ii - 1] not in '.#':
                position = ((i, ii - 1), (i, ii))
                tag = input[i][ii - 2:ii]
                add_teleport(teleports, tag, position)
                if tag == 'AA':
                    start = (i, ii)
                elif tag == 'ZZ':
                    end = (i, ii)
            if input[i][ii + 1] not in '.#':
                position = ((i, ii + 1), (i, ii))
                tag = input[i][ii + 1:ii + 3]
                add_teleport(teleports, tag, position)
                if tag == 'AA':
                    start = (i, ii)
                elif tag == 'ZZ':
                    end = (i, ii)

for i in range(m):
    for ii in range(2, n - 1):
        if input[ii][i] == '.':
            if input[ii - 1][i] not in '.#':
                position = ((ii - 1, i), (ii, i))
                tag = input[ii - 2][i] + input[ii - 1][i]
                add_teleport(teleports, tag, position)
                if tag == 'AA':
                    start = (ii, i)
                elif tag == 'ZZ':
                    end = (ii, i)
            if input[ii + 1][i] not in '.#':
                position = ((ii + 1, i), (ii, i))
                tag = input[ii + 1][i] + input[ii + 2][i]
                add_teleport(teleports, tag, position) 
                if tag == 'AA':
                    start = (ii, i)
                elif tag == 'ZZ':
                    end = (ii, i)

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
starting_nodes = {start, end}
for key, positions in teleports.items():
    if len(positions) < 2:
        continue
    
    starting_nodes.add(positions[1][1])
    starting_nodes.add(positions[0][1])

def get_shortest_path(G, source, target, scale) -> int:
    Q = []
    heappush(Q, (0, 0, source))
    distances = {source: 0}

    while len(Q) > 0:
        _, distance, (depth, u) = heappop(Q)
        key = (depth, u)
        if distance != distances[key]:
            continue
        if key == target:
            return distance
        for edge in G[u]:
            v, d = edge[0], edge[1]
            depth_diff = 0
            if len(edge) == 3:
                depth_diff = edge[2]
            new_distance = distance + d
            new_depth = depth + depth_diff
            new_key = (new_depth, v)
            if new_depth < 0:
                continue
            if new_key not in distances or new_distance < distances[new_key]:
                distances[new_key] = new_distance
                heur = scale * new_depth + new_distance
                heappush(Q, (heur, new_distance, new_key))

    raise Exception('target not found')


G = build_graph(input, starting_nodes, directions, teleports)

result = get_shortest_path(G, (0, start), (0, end), n * m + 100)

print(result)