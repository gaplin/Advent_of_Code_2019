input = open('input2.txt').read().splitlines()

wires = [set(), set()]
directions = {
    'U': (-1, 0),
    'R': (0, 1),
    'L': (0, -1),
    'D': (1, 0)
}
for idx, line in enumerate(input):
    moves = line.split(',')
    position = [0, 0]
    for move in moves:
        di, dii = directions[move[0]]
        steps = int(move[1:])
        for _ in range(steps):
            position[0] += di
            position[1] += dii
            wires[idx].add(tuple(position))

intersection = wires[0].intersection(wires[1])

result = 99999999
for i, ii in intersection:
    distance = abs(i) +  abs(ii)
    result = min(result, distance)

print(result)