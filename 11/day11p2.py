input = map(int, open('input2.txt').read().split(','))

mem = [0 for _ in range(3000000)]
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


def simulate(program: list, input_value: int) -> int:
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
            save_value(mem, modes[0], ip + 1, offset, input_value)
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

white_tiles = {(0, 0)}
painted_tiles = set()
current_tile = [0, 0]
program = [mem, 0, 0]
current_direction = [-1, 0]


grid = [['.' for _ in range(50)] for _ in range(50)]
l = 0
while True:
    color_to_paint = 0
    position_key = tuple(current_tile)
    if position_key in white_tiles:
        color_to_paint = simulate(program, 1)
    else:
        color_to_paint = simulate(program, 0)
    
    if color_to_paint == None:
        break

    painted_tiles.add(position_key)
    if color_to_paint == 1:
        grid[current_tile[0]][current_tile[1]] = '#'
        white_tiles.add(position_key)
    elif position_key in white_tiles:
        grid[current_tile[0]][current_tile[1]] = '.'
        white_tiles.remove(tuple(current_tile))

    direction = simulate(program, None)
    if direction == None:
        break
    if direction == 0: #turn left
        current_direction[0], current_direction[1] = -current_direction[1], current_direction[0]
    else:
        current_direction[0], current_direction[1] = current_direction[1], -current_direction[0]

    current_tile[0] += current_direction[0]
    current_tile[1] += current_direction[1]
    l += 1
    if l % 1000000 == 0:
        print(l)

for row in grid:
    for value in row:
        print(value, end='')
    print()