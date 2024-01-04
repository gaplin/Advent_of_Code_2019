import re
from math import lcm

input = open('input2.txt').read().splitlines()

moons = []
for line in input:
    x, y, z = map(int, re.findall('[0-9-]+', line))
    moons.append([x, y, z])

def get_cycle_length(values: list, n: int) -> int:
    states = set()
    velocities = [0 for _ in range(n)]
    step = 0
    while True:
        key = (tuple(values), tuple(velocities))
        if key in states:
            return step
        states.add(key)
        for i in range(n - 1):
            for j in range(i + 1, n):
                diff = 1
                if values[i] > values[j]:
                    diff = -1
                elif values[i] == values[j]:
                    diff = 0
                velocities[i] += diff
                velocities[j] -= diff
        
        for i in range(n):
            values[i] += velocities[i]
        step += 1

n = len(moons)
x_values = [x[0] for x in moons]
y_values = [x[1] for x in moons]
z_values = [x[2] for x in moons]

x_cycle_length = get_cycle_length(x_values, n)
y_cycle_length = get_cycle_length(y_values, n)
z_cycle_length = get_cycle_length(z_values, n)

print(lcm(x_cycle_length, y_cycle_length, z_cycle_length))