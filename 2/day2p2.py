input = map(int, open('input2.txt').read().split(','))

mem = [0 for _ in range(300)]
for idx, value in enumerate(input):
    mem[idx] = value

def simulate_and_get_value_at_0(mem: list) -> int:
    ip = 0
    while mem[ip] != 99:
        opcode = mem[ip]
        if opcode == 1:
            mem[mem[ip + 3]] = mem[mem[ip + 1]] + mem[mem[ip + 2]]
            ip += 4
        elif opcode == 2:
            mem[mem[ip + 3]] = mem[mem[ip + 1]] * mem[mem[ip + 2]]
            ip += 4
        else:
            ip += 1
    return mem[0]

result = 0
target = 19690720
for noun in range(0, 100):
    for verb in range(0, 100):
        mem_copy = list(mem)
        mem_copy[1] = noun
        mem_copy[2] = verb
        mem_0 = simulate_and_get_value_at_0(mem_copy)
        if mem_0 == target:
            result = 100 * noun + verb
            break
    else:
        continue
    break

print(result)