def inv_stack(coefs: tuple) -> tuple:
    return (-coefs[0], -coefs[1] - 1)

def inv_cut(coefs: tuple, c) -> tuple:
    return (coefs[0], coefs[1] + c)

def inv_increment(coefs: list, c: int) -> tuple:
    inv = pow(c, -1, N)
    return (inv * coefs[0], inv * coefs[1])


N = 119315717514047
M = 101741582076661
position = 2020
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

coefs = (1, 0)
for operation in reversed(operations):
    if operation[0] == 'stack':
        coefs = inv_stack(coefs)
    elif operation[0] == 'cut':
        coefs = inv_cut(coefs, operation[1])
    elif operation[0] == 'increment':
        coefs = inv_increment(coefs, operation[1])
    else:
        raise Exception('unknown operation {}'.format(operation))

result = (pow(coefs[0], M, N) * position + (1 - pow(coefs[0], M, N)) * pow(1 - coefs[0], -1, N) * coefs[1]) % N
print(result)