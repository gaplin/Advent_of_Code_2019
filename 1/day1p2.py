input = list(map(int, open('input2.txt').read().splitlines()))

result = 0

for num in input:
    num = num // 3 - 2
    while num > 0:
        result += num 
        num = num // 3 - 2

print(result)