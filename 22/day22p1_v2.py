def inv_stack(position: int, N: int) -> int:
    return (-position - 1) % N

def inv_cut(position: int, c: int, N: int) -> int:
    return (position + c) % N

def inv_increment(position: int, c: int, N: int) -> int:
    inv = pow(c, -1, N)
    return position * inv % N


N = 10007
input = open('input2.txt').read().splitlines()
operations = []
for line in input:
    if line.startswith('cut'):
        num = int(line.split(' ')[-1])
        operations.append(('cut', num))
    elif 'increment' in line:
        num = int(line.split(' ')[-1])
        operations.append(('increment', num))
    else:
        operations.append(('stack', 0))



position = 2496
for operation in reversed(operations):
    if operation[0] == 'stack':
        position = inv_stack(position, N)
    elif operation[0] == 'cut':
        position = inv_cut(position, operation[1], N)
    elif operation[0] == 'increment':
        position = inv_increment(position, operation[1], N)
    else:
        raise Exception('unknown operation {}'.format(operation))

print(position)