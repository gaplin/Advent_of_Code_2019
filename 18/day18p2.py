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

def build_state_graph(G: dict, num_of_keys: int, starting_configuration: tuple) -> dict:
    result = {}
    Q = Queue()
    Q.put((starting_configuration, ()))
    visited = {(starting_configuration, ())}
    result[(starting_configuration, ())] = []

    while Q.empty() == False:
        robots, keys = Q.get()
        if len(keys) == num_of_keys:
            continue
        
        for idx, v in enumerate(robots):
            for s, doors, distance in G[v]:
                if s in starting_configuration or s in keys:
                    continue
                if len(doors.intersection(keys)) != len(doors):
                    continue
                new_keys = list(keys)
                new_keys.append(s)
                new_keys.sort()
                new_robots = list(robots)
                new_robots[idx] = s
                state = (tuple(new_robots), tuple(new_keys))
                if state not in visited:
                    result[state] = []
                    visited.add(state)
                    Q.put(state)
                result[(robots, keys)].append((state, distance))

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

maze = open('input2.txt').read().splitlines()
n = len(maze)
m = len(maze[0])
for i in range(n):
    maze[i] = [x for x in maze[i]]
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

i, ii = starting_position
starting_positions = [(i - 1, ii - 1), (i - 1, ii + 1), (i + 1, ii - 1), (i + 1, ii + 1)]
for x in range(3):
    maze[i - 1 + x][ii] = '#'
    maze[i][ii - 1 + x] = '#'

starting_positions_symbols = ['@', '$', '%', '!']
for idx, (i, ii) in enumerate(starting_positions):
    maze[i][ii] = starting_positions_symbols[idx]

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
starting_nodes = dict(keys)
for idx, symbol in enumerate(starting_positions_symbols):
    starting_nodes[symbol] = starting_positions[idx]

G = build_graph(maze, n, m, keys, starting_nodes, directions)
all_states = build_state_graph(G, len(keys), tuple(starting_positions_symbols))
shortest_paths = get_shortest_paths(all_states, (tuple(starting_positions_symbols), ()))

result = 9999999999999999999
for key in all_states.keys():
    if len(key[1]) == len(keys):
        result = min(result, shortest_paths[key])

print(result)