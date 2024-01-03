low, high = tuple(map(int, open('input2.txt').read().split('-')))

def valid_number(num: int) -> bool:
    num_str = str(num)
    group_of_two = False
    n = len(num_str)
    group = num_str[0]
    group_size = 1
    for i in range(1, n):
        if num_str[i] < num_str[i - 1]:
            return False
        if num_str[i] == group:
            group_size += 1
        else:
            if group_size == 2:
                group_of_two = True
            group_size = 1
            group = num_str[i]
    else:
        if group_size == 2:
            group_of_two = True

    return group_of_two

result = 0
for i in range(low, high + 1):
    if valid_number(i):
        result += 1

print(result)