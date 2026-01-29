try:
    import requests

    dummydata = open("test_data.txt", "r").read().splitlines()
    dummydata.reverse()

    def input():
        return dummydata.pop()
except:
    pass

N = int(input())
nums = list(map(lambda x: int(x), input().split(" ")))
target = sum(nums)/len(nums)*2

if (target % 1 != 0):
    print(-1)
    exit()

nums.sort()

# print(nums, target)

used = set()


for i in range(len(nums)):
    if (i in used): continue
    
    n = nums[i]
    
    for i2 in range(len(nums)):
        if (i2 in used or i2 == i): continue
        
        # i2 = len(nums) - i2 - 1
        # print(n, nums[i2], used)
        
        if (n + nums[i2] == target):
            # print("HIT")
            used.add(i)
            used.add(i2)
            
            print(i + 1, i2 + 1)
            break
