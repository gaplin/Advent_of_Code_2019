low, high = tuple(map(int, open('input2.txt').read().split('-')))

def valid_number(num: int) -> bool:
    num_str = str(num)
    same_pair = False
    n = len(num_str)
    for i in range(1, n):
        if num_str[i] < num_str[i - 1]:
            return False
        if num_str[i] == num_str[i - 1]:
            same_pair = True

    return same_pair

result = 0
for i in range(low, high + 1):
    if valid_number(i):
        result += 1

print(result)