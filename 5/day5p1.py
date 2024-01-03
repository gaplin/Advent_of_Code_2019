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

def apply_operation(mem, op, modes, ip, initial_value):
    result = initial_value
    addresses = range(ip + 1, ip + len(modes) + 1)
    for mode, addr in zip(modes, addresses):
        if mode == 0:
            result = op(result, mem[mem[addr]])
        else:
            result = op(result, mem[addr])
    
    return result


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
            result = apply_operation(mem, int.__add__, modes, ip, 0)
            mem[mem[ip + 3]] = result
            ip += 4
        elif opcode == 2:
            modes = get_modes(operation, 2)
            result = apply_operation(mem, int.__mul__, modes, ip, 1)
            mem[mem[ip + 3]] = result
            ip += 4
        elif opcode == 3:
            mem[mem[ip + 1]] = input_value
            ip += 2
        elif opcode == 4:
            modes = get_modes(operation, 1)
            if modes[0] == 0:
                print(mem[mem[ip + 1]])
            else:
                print(mem[ip + 1])
            ip += 2
        else:
            ip += 1
    return mem[0]

simulate(mem, 1)