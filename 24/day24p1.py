def to_key(grid: list):
    str_key = ''
    for row in grid:
        str_key += ''.join(row)
    
    return str_key

def get_next_state(state: list, n: int, directions: list) -> list:
    result = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for ii in range(n):
            neighbours = 0
            for di, dii in directions:
                new_i, new_ii = i + di, ii + dii
                if 0 <= new_i < n and 0 <= new_ii < n and state[new_i][new_ii] == '#':
                    neighbours += 1
            if state[i][ii] == '#':
                if neighbours == 1:
                    result[i][ii] = '#'
                else:
                    result[i][ii] = '.'
            else:
                if neighbours == 1 or neighbours == 2:
                    result[i][ii] = '#'
                else:
                    result[i][ii] = '.'
    return result

def get_rating(grid: list):
    result = 0
    pow = 1
    for row in grid:
        for value in row:
            if value == '#':
                result += pow
            pow <<= 1

    return result

input = open('input2.txt').read().splitlines()
grid = [[x for x in row] for row in input]
current_state = grid
visited_states = set(to_key(current_state))
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
n = len(grid)
while True:
    current_state = get_next_state(current_state, n, directions)
    state_key = to_key(current_state)
    if state_key in visited_states:
        break
    visited_states.add(state_key)

result = get_rating(current_state)
print(result)