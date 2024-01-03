input = open('input2.txt').read().splitlines()

directions = {
    'U': (-1, 0),
    'R': (0, 1),
    'L': (0, -1),
    'D': (1, 0)
}

first_wire = {}

moves = input[0].split(',')
position = [0, 0]
step = 0
for move in moves:
    di, dii = directions[move[0]]
    steps = int(move[1:])
    for _ in range(steps):
        step += 1
        position[0] += di
        position[1] += dii
        key = tuple(position)
        if key not in first_wire:
            first_wire[key] = step

result = 99999999999
moves = input[1].split(',')
position = [0, 0]
step = 0
for move in moves:
    di, dii = directions[move[0]]
    steps = int(move[1:])
    for _ in range(steps):
        step += 1
        position[0] += di
        position[1] += dii
        key = tuple(position)
        if key in first_wire:
            result = min(result, first_wire[key] + step)

print(result)