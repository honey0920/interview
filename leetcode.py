def two_sum(array, target):
    result = []
    array.sort()
    front = array[0]
    end = array[-1]
    while front < end:
        if front + end > target:
            end -= 1
        elif front + end < target :
            front += 1
        else:
            result.append((array[front], array[end]))
    return result

def threeSum(nums):
    """
    :type nums: List[int]
    :rtype: List[List[int]]
    """
    if len(nums) < 3:
        return [[]]
    result = []
    nums.sort()
    print(nums)
    target = 0
    for i in range(len(nums) -2):
        front  = i+1
        end =  len(nums) - 1
        print front, end
        while front < end:
            if front < end and (nums[front] + nums[end] > target - nums[i]) :
                end -= 1
            if front < end and (nums[front] + nums[end] < target - nums[i]):
                front += 1
            if front < end and (nums[front] + nums[end] == target - nums[i]):
                result.append((nums[i], nums[front], nums[end]))
                if front < end:
                    front += 1
                while front < end and nums[front] == nums[front+1] :
                    front += 1
                if front < end :
                    end -=1
                while front < end and nums[end] == nums[end - 1]:
                    end -= 1
    return map(list, set(result))

print(threeSum([-1,0,1,2,-1,-4]))