input = open('input2.txt').read().strip() * 10000

def FFT(nums: list, n: int) -> None:
    prefix_sum = [0 for _ in range(n)]
    prefix_sum[0] = nums[0]
    for i in range(1, n):
        prefix_sum[i] = prefix_sum[i - 1] + nums[i]

    all_sum = prefix_sum[n - 1]
    nums[0] = all_sum % 10
    for idx in range(1, n):
        nums[idx] = (all_sum - prefix_sum[idx - 1]) % 10

nums = [int(x) for x in input]
offset = int(''.join(map(str, nums[:7])))
nums = nums[offset:]
n = len(nums)
for i in range(0, 100):
    FFT(nums, n)

print(''.join(map(str, nums[:8])))