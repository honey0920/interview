
def partition(array, front, end):
    begin = front
    pivot = array[front]
    while front < end :
        while front < end and array[end] >= pivot:
            end = end - 1

        while front < end and array[front] <= pivot:
            front = front + 1

        array[front], array[end] = array[end], array[front]

    array[front], array[begin] = array[begin], array[front]
    #print array
    return front

def quick_sort(a, front, end):
    if front < end:
        middle = partition(a, front, end)
        quick_sort(a,front, middle-1)
        quick_sort(a, middle+1, end)

def get_k(a, front, end, k):
    if front == end:
        return a[front]
    else:
        index = partition(a, front, end)
        if index < k:
            return get_k(a, index+1, end, k)
        elif index > k :
            return get_k(a, front, index+1, k)
        else :
            return a[k]


def bubble_sort(a):
    l = len(a)
    for i in range(l):
        for j in range(i):
            if a[j] > a[i]:
                a[i], a[j] = a[j], a[i]
    return a

def merge_sort(a):
     l = len(a)
     if l <= 1:
         return a
     b = []
     middle = l/2
     left = merge_sort(a[:middle])
     right = merge_sort(a[middle:])
     while left != [] and right != []:
         if left[0] <= right[0]:
             b += [left[0]]
             left.pop(0)
         else:
             b += [right[0]]
             right.pop(0)
     b += left + right
     return b

def adjust_heap(array, start, end):
    while True:
        left_child = 2 * start + 1
        if left_child > end:
            break

        if left_child < end and array[left_child+1]>array[left_child]:
            left_child += 1

        if array[left_child] > array[start]:
            array[start] , array[left_child] = array[left_child], array[start]
            start = left_child
        else:
            break

def heap_sort(a):
    for i in range(len(a)//2 -1, -1, -1):
        adjust_heap(a, i, len(a)-1)

    for j in range(len(a)-1, 0, -1):
        a[0], a[j] = a[j], a[0]
        adjust_heap(a, 0, j-1)
    return a

def b_search(x, target, front,  end):
    if(front > end):
        return -1
    else :
        middle = (front + end)/2
        if x[middle] == target:
            return middle
        elif x[middle] > target :
            return b_search(x, target, front, middle-1)
        else:
            return b_search(x, target, middle+1, end)

def b_search_loop(x, target):
    front = 0
    end = len(a)-1
    while(front <= end):
        middle = (front + end)/2
        if(x[middle] == target):
            return middle
        elif(x[middle] < target):
            front = middle+1
        else:
            end = middle-1
    return -1

def rotate_array(a):
    front = 0
    end = len(a) - 1
    while(front < end):
        middle = (front + end)/2
        if a[front] > a[middle] :
            end = middle
        elif a[middle]> a[end]:
            front = middle
        elif a[front] == a[middle]:
            min = a[front]
            for i in range(front, middle+1):
                if a[i] < min:
                    min = a[i]
            return min
        elif a[middle] == a[end]:
            min = a[middle]
            for i in range(middle, end+1):
                if a[i] < min:
                    min = a[i]
            return min
        else:
            return a[front]
    return a[front]




#a = [1, 0, 2, 3, 0 ,8, 3, 1,6]
#a = [4, 6, 3 ,0 ,1, 2, 6, 7, 9]
#a = [3, 3, 3, 3, 3, 3, 3, 3, 3]
a = [3, 3, 3, 3, 3, 3, 3, 3, 3]

print(a)
print(rotate_array(a))
print(get_k(a, 0, len(a)-1, 2))
print(b_search(a,3,0, len(a)-1))
print(b_search_loop(a, 3))

#print(bubble_sort(a))
#print(merge_sort(a))
#print(heap_sort(a))



