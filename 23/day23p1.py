from queue import Queue
from copy import deepcopy

input = map(int, open('input2.txt').read().split(','))

mem = [0 for _ in range(10000)]
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

def step(program: list, message_queues: list) -> int:
    mem, ip, offset, id, status, outgoing_message = program
    my_q = message_queues[id]
    operation = mem[ip]
    opcode = operation % 100
    if opcode == 99:
        return False
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
        if my_q.empty() == True:
            value = -1
        else:
            value = my_q.get()
        save_value(mem, modes[0], ip + 1, offset, value)
        ip += 2
    elif opcode == 4: # output
        modes = get_modes(operation, 1)
        output_value = get_value(mem, modes[0], ip + 1, offset)
        outgoing_message.append(output_value)
        if len(outgoing_message) == 3:
            target_q = message_queues[outgoing_message.pop(0)]
            target_q.put(outgoing_message.pop(0))
            target_q.put(outgoing_message.pop(0))
        ip += 2
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
    return True

def to_ASCII(instructions: list) -> list:
    result = []
    for instruction in instructions:
        for char in instruction:
            result.append(ord(char))
        result.append(ord('\n'))
    return result


N = 50
queues_limit = 1000
target = 255
# 0 - mem 
# 1 - ip
# 2 - offset
# 3 - id
# 4 - status
# 5 - outgoing_message
computers = [[list(mem), 0, 0, id, True, []] for id in range(N)]
message_queue = [Queue() for _ in range(queues_limit)]
for id in range(N):
    message_queue[id].put(id)

result = 0

while True:
    for computer in computers:
        if computer[4] == True:
            computer[4] = step(computer, message_queue)
            if message_queue[target].empty() == False:
                x = message_queue[target].get()
                y = message_queue[target].get()
                result = y
                break
    else:
        continue
    break
print(result)