input = map(int, open('input2.txt').read().split(','))

computer = [0 for _ in range(300)]

for idx, value in enumerate(input):
    computer[idx] = value

computer[1] = 12
computer[2] = 2
ip = 0
while computer[ip] != 99:
    opcode = computer[ip]
    if opcode == 1:
        computer[computer[ip + 3]] = computer[computer[ip + 1]] + computer[computer[ip + 2]]
        ip += 4
    elif opcode == 2:
        computer[computer[ip + 3]] = computer[computer[ip + 1]] * computer[computer[ip + 2]]
        ip += 4
    else:
        ip += 1

print(computer[0])