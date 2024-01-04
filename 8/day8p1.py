input = list(map(int, open('input2.txt').read().strip()))

n = 6
m = 25
layer_size = n * m

layers = []
current_layer = ''
idx = 0
for value in input:
    if idx == 0:
        current_layer = [[0 for _ in range(m)] for _ in range(n)]
        layers.append(current_layer)
    i = idx // m
    ii = idx % m
    current_layer[i][ii] = value
    idx = (idx + 1) % layer_size

def get_result_for_layer(layer: list) -> tuple:
    occurences = [0, 0, 0]
    for row in layer:
        for value in row:
            if value <= 2:
                occurences[value] += 1

    return (occurences[0], occurences[1] * occurences[2])

result = 0
min_zeros = layer_size
for layer in layers:
    zeros, value = get_result_for_layer(layer)
    if zeros <= min_zeros:
        result = value
        min_zeros = zeros

print(result)