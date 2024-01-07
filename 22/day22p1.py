def deal_into_new_stack(deck: list) -> list:
    return [x for x in reversed(deck)]

def cut(deck: list, N: int) -> list:
    bottom = deck[-N:]
    top = deck[:-N]
    result = bottom + top
    return result

def deal_with_increment(deck: list, N: int) -> list:
    n = len(deck)
    result = [0 for _ in range(n)]
    m = n - 1
    for i in reversed(range(n)):
        result[m] = deck[i]
        m = (m - N) % n
    return result

N = 10007
deck = [x for x in reversed(range(N))]
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

for operation in operations:
    if operation[0] == 'stack':
        deck = deal_into_new_stack(deck)
    elif operation[0] == 'cut':
        deck = cut(deck, operation[1])
    elif operation[0] == 'increment':
        deck = deal_with_increment(deck, operation[1])
    else:
        raise Exception('unknown operation {}'.format(operation))

result = deck.index(2019)
result = N - result - 1
print(result)
