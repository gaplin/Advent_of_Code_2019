nums = [int(x) for x in open('input2.txt').read().strip()]

n = len(nums)
def get_value_at_idx(idx, pattern, prefix_sum, k, n):
    j = idx + 1
    occurs = [j for _ in range(k)]
    occurs[0] -= 1
    idx = 0
    res = 0
    curr_pattern = 0
    while idx < n:
        pattern_value = pattern[curr_pattern]
        r = min(n - 1, idx + occurs[curr_pattern] - 1)
        if pattern_value != 0:
            l_value = prefix_sum[idx - 1] if idx > 0 else 0
            r_value = prefix_sum[r]
            res += pattern_value * (r_value - l_value)

        curr_pattern = (curr_pattern + 1) % k
        occurs[curr_pattern] = j
        idx = r + 1

    res = abs(res) % 10
    return res


def FFT(nums: list, pattern: list, n: int) -> None:
    prefix_sum = [0 for _ in range(n)]
    prefix_sum[0] = nums[0]
    for i in range(1, n):
        prefix_sum[i] = prefix_sum[i - 1] + nums[i]
    k = len(pattern)

    result = [get_value_at_idx(i, pattern, prefix_sum, k, n) for i in range(n)]

    for i in range(n):
        nums[i] = result[i]

for _ in range(100):
    FFT(nums, [0, 1, 0, -1], n)

print(''.join(map(str, nums[:8])))