def lengthOfLIS(self, nums: list[int]) -> int:
    if not nums:
        return 0

    n = len(nums)
    temp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                temp[i] = max(temp[i], temp[j] + 1)

    #return max(temp)

    print(temp)
    return max(temp)