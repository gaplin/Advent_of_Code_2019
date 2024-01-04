input = open('input2.txt').read().splitlines()

n = len(input)
m = len(input[0])

def get_key(x1: int, y1: int, x2: int, y2: int) -> float:
    y_diff = y2 - y1
    x_diff = x2 - x1
    result = [-1, -1, 0]
    if x_diff >= 0:
        result[0] = 1
    if y_diff >= 0:
        result[1] = 1
    if y_diff == 0:
        result[2] = float("inf")
    else:
        result[2] = x_diff / y_diff
    
    return tuple(result)

def get_visible_points(all_points: list, p: tuple) -> int:
    angles = set()
    for point in all_points:
        if point == p:
            continue
        angle = get_key(*p, *point)
        angles.add(angle)
    return len(angles)

points = []
for y in range(n):
    for x in range(m):
        if input[y][x] == '#':
            points.append((x, y))

result = 0
for point in points:
    result = max(result, get_visible_points(points, point))

print(result)