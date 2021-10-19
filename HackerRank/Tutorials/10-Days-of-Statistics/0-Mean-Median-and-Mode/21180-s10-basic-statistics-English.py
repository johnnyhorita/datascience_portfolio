n = input()
x = input()

def _mean(arr, n):
    return (sum(arr) / int(n))

def _median(arr):
    arr.sort()
    mid = len(arr) // 2
    return ((arr[mid] + arr[~mid]) / 2)

def _mode(arr):
    most = max(list(map(arr.count, arr)))
    if most == 1:
        arr.sort()
        mode = sort(arr)
    else:
        mode = (min(set(arr), key=arr.count))
    return mode

arr = list(map(int, x.split()))
mean = _mean(arr, n)
median = _median(arr)
mode = _mode(arr)

print(mean)
print(median)
print(mode)
