input = open('input2.txt').read().splitlines()

n = len(input)
m = len(input[0])

def get_key(x1: int, y1: int, x2: int, y2: int) -> float:
    y_diff = y2 - y1
    x_diff = x2 - x1
    f = 0
    if y_diff != 0 or x_diff != 0:
        f = y_diff / (abs(x_diff) + abs(y_diff))
    if x_diff < 0:
        f = 2 - f
    elif y_diff < 0:
        f += 4

    return f    

def get_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return (y2 - y1) ** 2 + (x2 - x1) ** 2 

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

max_visible_points = 0
station = ()
for point in points:
    visible_points = get_visible_points(points, point)
    if visible_points > max_visible_points:
        max_visible_points = visible_points
        station = point

def sorted_points(points: dict) -> list:
    result = []
    sections = [[], [], [], []]

    for angle, point in points.items():
        sections[int(angle // 1)].append((angle, point))

    for i in range(4):
        sections[i].sort(key=lambda x: x[0])
    
    for point in sections[3]:
        result.append(point[1])

    for i in range(3):
        for point in sections[i]:
            result.append(point[1])
    
    return result

points.remove(station)
removed_points = 0
removed_point = ()
while True:
    angles = {}
    end = False
    for point in points:
        angle = get_key(*station, *point)
        if angle in angles:
            previous_point = angles[angle]
            d1, d2 = get_distance(*station, *previous_point), get_distance(*station, *point)
            if d2 < d1:
                angles[angle] = point
        else:
            angles[angle] = point
    
    pts_to_remove = sorted_points(angles)
    for point in pts_to_remove:
        points.remove(point)
        removed_point = point
        removed_points += 1
        if removed_points == 200:
            end = True
            break

    if end == True:
        break

print(100 * removed_point[0] + removed_point[1])