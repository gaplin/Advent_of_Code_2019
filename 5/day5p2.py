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

def get_value(mem: list, mode: int, addr: int) -> int:
    return mem[addr] if mode == 1 else mem[mem[addr]]


def simulate(mem: list, input_value: int) -> int:
    ip = 0
    while True:
        operation = mem[ip]
        opcode = operation % 100
        if opcode == 99:
            break
        operation //= 100
        if opcode == 1:
            modes = get_modes(operation, 2)
            result = get_value(mem, modes[0], ip + 1) + get_value(mem, modes[1], ip + 2)
            mem[mem[ip + 3]] = result
            ip += 4
        elif opcode == 2:
            modes = get_modes(operation, 2)
            result = get_value(mem, modes[0], ip + 1) * get_value(mem, modes[1], ip + 2)
            mem[mem[ip + 3]] = result
            ip += 4
        elif opcode == 3:
            mem[mem[ip + 1]] = input_value
            ip += 2
        elif opcode == 4:
            modes = get_modes(operation, 1)
            print(get_value(mem, modes[0], ip + 1))
            ip += 2
        elif opcode == 5:
            modes = get_modes(operation, 2)
            if get_value(mem, modes[0], ip + 1) != 0:
                ip = get_value(mem, modes[1], ip + 2)
            else:
                ip += 3
        elif opcode == 6:
            modes = get_modes(operation, 2)
            if get_value(mem, modes[0], ip + 1) == 0:
                ip = get_value(mem, modes[1], ip + 2)
            else:
                ip += 3
        elif opcode == 7:
            modes = get_modes(operation, 2)
            if get_value(mem, modes[0], ip + 1) < get_value(mem, modes[1], ip + 2):
                mem[mem[ip + 3]] = 1
            else:
                mem[mem[ip + 3]] = 0
            ip += 4
        elif opcode == 8:
            modes = get_modes(operation, 2)
            if get_value(mem, modes[0], ip + 1) == get_value(mem, modes[1], ip + 2):
                mem[mem[ip + 3]] = 1
            else:
                mem[mem[ip + 3]] = 0
            ip += 4
        else:
            ip += 1
    return mem[0]

simulate(mem, 5)