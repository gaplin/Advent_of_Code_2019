from queue import Queue

def build_graph(maze: list, n: int, m: int, keys: dict, starting_nodes: dict, directions: list) -> dict:
    result = {x: [] for x in starting_nodes.keys()}
    for key in keys.keys():
        result[key] = []
    
    for v, position in starting_nodes.items():
        Q = Queue()
        Q.put((position, 0, set()))
        visited = {position}
        while Q.empty() == False:
            position, distance, doors = Q.get()
            symbol = maze[position[0]][position[1]]
            if symbol != v and symbol != '.':
                if symbol in starting_nodes:
                    result[v].append((symbol, doors, distance))
                else:
                    doors.add(symbol.lower())

            for di, dii in directions:
                new_i, new_ii = position[0] + di, position[1] + dii
                new_position = (new_i, new_ii)
                if maze[new_i][new_ii] != '#' and new_position not in visited:
                    visited.add(new_position)
                    Q.put((new_position, distance + 1, set(doors)))

    return result

def build_state_graph(G: dict, num_of_keys: int) -> dict:
    result = {}
    Q = Queue()
    Q.put(('@', ()))
    visited = {('@', ())}
    result[('@', ())] = []

    while Q.empty() == False:
        v, keys = Q.get()
        if len(keys) == num_of_keys:
            continue

        for s, doors, distance in G[v]:
            if s == '@' or s in keys:
                continue
            if len(doors.intersection(keys)) != len(doors):
                continue
            new_keys = list(keys)
            new_keys.append(s)
            new_keys.sort()
            state = (s, tuple(new_keys))
            if state not in visited:
                result[state] = []
                visited.add(state)
                Q.put(state)
            result[(v, keys)].append((state, distance))

    return result

def get_shortest_paths(G: dict, starting_node: tuple) -> dict:
    result = {}
    result[starting_node] = 0
    Q = Queue()
    Q.put(starting_node)
    while Q.empty() == False:
        u = Q.get()
        current_distance = result[u]
        for v, distance in G[u]:
            new_distance = distance + current_distance
            if v not in result or result[v] > new_distance:
                result[v] = new_distance
                Q.put(v)

    return result

maze = open('input.txt').read().splitlines()
n = len(maze)
m = len(maze[0])
doors = {}
keys = {}
starting_position = ()
for i in range(n):
    for ii in range(m):
        symbol = maze[i][ii]
        if symbol not in '.#':
            if symbol == '@':
                starting_position = (i, ii)
            elif symbol.upper() == symbol:
                doors[symbol] = (i, ii)
            else:
                keys[symbol] = (i, ii)

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
starting_nodes = dict(keys)
starting_nodes['@'] = starting_position

G = build_graph(maze, n, m, keys, starting_nodes, directions)

all_states = build_state_graph(G, len(keys))
shortest_paths = get_shortest_paths(all_states, ('@', ()))

result = 9999999999999999999
for key in all_states.keys():
    if len(key[1]) == len(keys):
        result = min(result, shortest_paths[key])

print(result)