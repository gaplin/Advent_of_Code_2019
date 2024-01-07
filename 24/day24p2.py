def get_next_state(bugs: set, n: int, directions: list) -> list:
    result = set()
    neighbours = {}
    mid = n // 2
    for i, ii, depth in bugs:
        for di, dii in directions:
            new_i, new_ii, new_depth = i + di, ii + dii, depth
            if new_i < 0:
                new_i = mid - 1
                new_ii = mid
                new_depth -= 1
            elif new_i >= n:
                new_i = mid + 1
                new_ii = mid
                new_depth -= 1
            elif new_ii < 0:
                new_ii = mid - 1
                new_i = mid
                new_depth -= 1
            elif new_ii >= n:
                new_ii = mid + 1
                new_i = mid
                new_depth -= 1
            elif new_i == mid and new_ii == mid:
                if di == 1:
                    for k in range(n):
                        key = (0, k, depth + 1)
                        if key not in neighbours:
                            neighbours[key] = 1
                        else:
                            neighbours[key] += 1
                elif di == -1:
                    for k in range(n):
                        key = (n - 1, k, depth + 1)
                        if key not in neighbours:
                            neighbours[key] = 1
                        else:
                            neighbours[key] += 1
                elif dii == 1:
                    for k in range(n):
                        key = (k, 0, depth + 1)
                        if key not in neighbours:
                            neighbours[key] = 1
                        else:
                            neighbours[key] += 1
                elif dii == -1:
                    for k in range(n):
                        key = (k, n - 1, depth + 1)
                        if key not in neighbours:
                            neighbours[key] = 1
                        else:
                            neighbours[key] += 1
                else:
                    raise Exception()
                continue
            
            key = (new_i, new_ii, new_depth)
            if key not in neighbours:
                neighbours[key] = 1
            else:
                neighbours[key] += 1

    for position, count in neighbours.items():
        if position in bugs:
            if count == 1:
                result.add(position)
        elif count in (1, 2):
            result.add(position)

    return result

input = open('input2.txt').read().splitlines()
n = len(input)
bugs = set()
for i in range(n):
    for ii in range(n):
        if input[i][ii] == '#':
            bugs.add((i, ii, 0))

iterations = 200
current_state = bugs
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

for _ in range(iterations):
    current_state = get_next_state(current_state, n, directions)

result = len(current_state)
print(result)