from queue import Queue

input = open('input2.txt').read().splitlines()

n = len(input)
m = len(input[0])


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
teleport_fields = {}
for key, positions in teleports.items():
    if len(positions) < 2:
        continue
    
    teleport_fields[positions[0][0]] = positions[1][1]
    teleport_fields[positions[1][0]] = positions[0][1]

def get_shortest_path(maze: list, teleports: dict, source: tuple(), target: tuple(), directions: list) -> int:
    visited = {source}
    Q = Queue()
    Q.put((source, 0))

    while Q.empty() == False:
        position, distance = Q.get()
        if position == target:
            return distance
        
        for di, dii in directions:
            new_i, new_ii = position[0] + di, position[1] + dii
            new_position = (new_i, new_ii)
            if new_position in teleports:
                new_position = teleports[new_position]
            
            if new_position not in visited and maze[new_position[0]][new_position[1]] == '.':
                visited.add(new_position)
                Q.put((new_position, distance + 1))

    raise Exception('target not found')

result = get_shortest_path(input, teleport_fields, start, end, directions)

print(result)