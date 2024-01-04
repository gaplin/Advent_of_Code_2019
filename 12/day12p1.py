import re
from functools import reduce

input = open('input.txt').read().splitlines()

moons = []
for line in input:
    x, y, z = map(int, re.findall('[0-9-]+', line))
    moons.append(([x, y, z], [0, 0, 0]))

for i in range(1000):
    for idx, moon_a in enumerate(moons):
        for moon_b in moons[:idx]:
            x1, y1, z1 = moon_a[0]
            x2, y2, z2 = moon_b[0]
            dvx = 1
            dvy = 1
            dvz = 1
            if x1 > x2:
                dvx = -1
            elif x1 == x2:
                dvx = 0
            if y1 > y2:
                dvy = -1
            elif y1 == y2:
                dvy = 0
            if z1 > z2:
                dvz = -1
            elif z1 == z2:
                dvz = 0
            moon_a[1][0] += dvx
            moon_a[1][1] += dvy
            moon_a[1][2] += dvz
            moon_b[1][0] -= dvx
            moon_b[1][1] -= dvy
            moon_b[1][2] -= dvz
    for position, velocity in moons:
        position[0] += velocity[0]
        position[1] += velocity[1]
        position[2] += velocity[2]

result = 0
for position, velocity in moons:
    p_energy = reduce(lambda x, y: x + abs(y), position, 0)
    k_energy = reduce(lambda x, y: x + abs(y), velocity, 0)
    result += p_energy * k_energy

print(result)