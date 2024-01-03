input = list(map(int, open('input2.txt').read().splitlines()))

result = sum([x // 3 - 2 for x in input])

print(result)