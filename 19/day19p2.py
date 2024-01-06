from queue import Queue
from copy import deepcopy

input = map(int, open('input2.txt').read().split(','))

mem = [0 for _ in range(3000)]
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

def simulate(program: list, input_values: list) -> int:
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
            value = input_values.pop(0)
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

n = 50
grid = [['.' for _ in range(n)] for _ in range(n)]
program = [mem, 0, 0]
result = 0
for i in range(n):
    for ii in range(n):
        position = [ii, i]
        res = simulate(deepcopy(program), position)
        if res == 1:
            result += 1
            grid[i][ii] = '#'

def get_beam_count_for_row(program, y):
    x = y
    position = [x, y]
    while simulate(deepcopy(program), position) == 0:
        x -= 1
        position = [x, y]

    x -= 1
    result = 1
    position = [x - 1, y]
    while simulate(deepcopy(program), position) == 1:
        result += 1
        x -= 1
        position = [x, y]
    
    return result
def get_first_beam_position_for_row(program, y):
    x = y
    position = [x, y]
    while simulate(deepcopy(program), position) == 0:
        x -= 1
        position = [x, y]

    x -= 1
    position = [x - 1, y]
    while simulate(deepcopy(program), position) == 1:
        x -= 1
        position = [x, y]
    
    return x + 1

l, r = 8, 8
n = 100
target_beams = 2 * n - 3

while True:
    if get_beam_count_for_row(program, r) > target_beams:
        r -= 1
        break
    l = r
    r <<= 1

r += 1
while l < r:
    m = (l + r) // 2
    beams = get_beam_count_for_row(program, m)
    if beams >= target_beams:
        r = m
    else:
        l = m + 1
ul_y = l - n + 1
ul_x = get_first_beam_position_for_row(program, l)

print(10000 * ul_x + ul_y)