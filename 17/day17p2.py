import re

input = map(int, open('input2.txt').read().split(','))

mem = [0 for _ in range(300000)]
for idx, value in enumerate(input):
    mem[idx] = value

def get_modes(mask: int, count: int) -> list:
    result = []
    for _ in range(count):
        result.append(mask % 10)
        mask //= 10

    return result

def get_value(mem: list, mode: int, addr: int, offset: int) -> int:
    if mode == 0:
        return mem[mem[addr]]
    elif mode == 1:
        return mem[addr]
    elif mode == 2:
        return mem[mem[addr] + offset]
    else:
        raise Exception('invalid read mode: {}'.format(mode))

def save_value(mem: list, mode: int, addr: int, offset: int, value: int):
    if mode == 0:
        mem[mem[addr]] = value
    elif mode == 2:
        mem[mem[addr] + offset] = value
    else:
        raise Exception('invalid write mode: {}'.format(mode))

def simulate(program: list, input_value: list) -> int:
    mem, ip, offset = program
    output_value = None
    while True:
        operation = mem[ip]
        opcode = operation % 100
        if opcode == 99:
            break
        operation //= 100
        if opcode == 1: # add
            modes = get_modes(operation, 3)
            result = get_value(mem, modes[0], ip + 1, offset) + get_value(mem, modes[1], ip + 2, offset)
            save_value(mem, modes[2], ip + 3, offset, result)
            ip += 4
        elif opcode == 2: # mult
            modes = get_modes(operation, 3)
            result = get_value(mem, modes[0], ip + 1, offset) * get_value(mem, modes[1], ip + 2, offset)
            save_value(mem, modes[2], ip + 3, offset, result)
            ip += 4
        elif opcode == 3: # input
            modes = get_modes(operation, 1)
            value = input_value.pop(0)
            save_value(mem, modes[0], ip + 1, offset, value)
            ip += 2
        elif opcode == 4: # output
            modes = get_modes(operation, 1)
            output_value = get_value(mem, modes[0], ip + 1, offset)
            ip += 2
            break
        elif opcode == 5: # JNZERO
            modes = get_modes(operation, 2)
            if get_value(mem, modes[0], ip + 1, offset) != 0:
                ip = get_value(mem, modes[1], ip + 2, offset)
            else:
                ip += 3
        elif opcode == 6: #  JZERO
            modes = get_modes(operation, 2)
            if get_value(mem, modes[0], ip + 1, offset) == 0:
                ip = get_value(mem, modes[1], ip + 2, offset)
            else:
                ip += 3
        elif opcode == 7: # LESS
            modes = get_modes(operation, 3)
            result = 0
            if get_value(mem, modes[0], ip + 1, offset) < get_value(mem, modes[1], ip + 2, offset):
                result = 1
            save_value(mem, modes[2], ip + 3, offset, result)
            ip += 4
        elif opcode == 8: # Equal
            modes = get_modes(operation, 3)
            result = 0
            if get_value(mem, modes[0], ip + 1, offset) == get_value(mem, modes[1], ip + 2, offset):
                result = 1
            save_value(mem, modes[2], ip + 3, offset, result)
            ip += 4
        elif opcode == 9: # Offset modification
            modes = get_modes(operation, 1)
            offset += get_value(mem, modes[0], ip + 1, offset)
            ip += 2
        else:
            ip += 1

    program[1] = ip
    program[2] = offset
    return output_value

def get_map(mem: list) -> list:
    result = [[]]

    program = [mem, 0, 0]
    while True:
        output = simulate(program, None)
        if output == None:
            break
        symbol = chr(output)
        if symbol == '\n':
            result.append([])
        else:
            result[-1].append(symbol)

    while result[-1] == []:
        result.pop()
    
    return result

grid = get_map(list(mem))
n = len(grid)
m = len(grid[0])
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

starting_position = ()
for i in range(n):
    for ii in range(m):
        if grid[i][ii] == '^':
            starting_position = (i, ii)
            break
    else:
        continue
    break

left_turn = lambda x: (-x[1], x[0])
right_turn = lambda x: (x[1], -x[0])
turns = ((left_turn, 'L'), (right_turn, 'R'))
current_direction = (-1, 0)
position = starting_position
current_steps = 0
all_moves = []
while True:
    new_i, new_ii = position[0] + current_direction[0], position[1] + current_direction[1]
    if new_i < 0 or new_i >= n or new_ii < 0 or new_ii >= m or grid[new_i][new_ii] != '#':
        for turn, label in turns:
            new_direction = turn(current_direction)
            new_i, new_ii = position[0] + new_direction[0], position[1] + new_direction[1]
            if 0 <= new_i < n and 0 <= new_ii < m and grid[new_i][new_ii] == '#':
                if current_steps > 0:
                    all_moves.append(current_steps)
                all_moves.append(label)
                current_steps = 1
                position = (new_i, new_ii)
                current_direction = new_direction
                break
        else:
            all_moves.append(current_steps)
            break
    else:
        current_steps += 1
        position = (new_i, new_ii)


def get_function(text: str) -> str:
    result = text[0] + ','
    for symbol in text[1:]:
        if symbol in 'RL':
            result += ',' + symbol + ','
        else:
            result += symbol
    return result

text = ''.join(map(str, all_moves)) 
regex = r'^(?P<A>[RL][RL0-9]{9,15}[0-9])\1*(?P<B>[RL][RL0-9]{1,15}[0-9])(?:\1|\2)*(?P<C>[RL][RL0-9]{5,15}[0-9])(?:\1|\2|\3){1,10}$'
f = re.fullmatch(regex, text)
groups = [(f.group('A'), 'A'), (f.group('B'), 'B'), (f.group('C'), 'C')]
main_routine = []
while len(text) > 0:
    for group, label in groups:
        if text.startswith(group):
            main_routine.append(label)
            text = text.removeprefix(group)
            break

A = get_function(groups[0][0]) + '\n'
B = get_function(groups[1][0]) + '\n'
C = get_function(groups[2][0]) + '\n'
routine_str = ','.join(main_routine) + '\n'

def get_result(mem: list, A: str, B: str, C: str, main_routine: str) -> int:
    program = [mem, 0, 0]
    input_to_process = [main_routine, A, B, C]
    input = []
    for value in input_to_process:
        for char in value:
            input.append(ord(char))
    input.append(ord('n'))
    input.append(ord('\n'))
    result = 0
    while True:
        part = simulate(program, input)
        if part == None:
            break
        result = part

    return result

mem[0] = 2
result = get_result(mem, A, B, C, routine_str)
print(result)