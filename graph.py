import sys
inf = sys.maxsize
matrix = [
    [0, 6, 3, inf, inf, inf],
    [6, 0, 2, 5, inf, inf],
    [3, 2, 0, 3, 4, inf],
    [inf, 5, 3, 0, 2, 3],
    [inf, inf, 4, 2, 0, 5],
    [inf, inf, inf, 3, 5, 0],
]
def dijstra():
    visited = len(matrix) * [0]
    target = 0
    visited[target] = 1
    distance = matrix[target]
    set = [target]
    path = [[target] for i in range(len(matrix))]

    for i in range(len(matrix)):
        if distance[i] != inf:
            path[i].append(i)

    while 0 in visited:
        cur = target
        min_dis = sys.maxsize

        for i in range(len(matrix)):
            if visited[i] == 0:
                last = set[-1]
                dis = distance[last] + matrix[last][i]
                if dis < distance[i]:
                    distance[i] = dis
                    path[i] = path[last] + [ i ]
                if distance[i] < min_dis :
                    min_dis = distance[i]
                    cur = i


        visited[cur] = 1
        distance[cur] = min_dis
        set.append(cur)

    print(distance)
    print(path)

p = [ [0,1,2,3,4,5] for i in range(len(matrix))]



def floyd():
    target = 0
    for temp in range(len(matrix)):
        for col in range(len(matrix)):
            for row in range(len(matrix)):
                if matrix[col][temp] == inf or matrix[temp][row] == inf:
                    dis = inf
                else :
                    dis =  matrix[col][temp] + matrix[temp][row]
                if dis < matrix[col][row]:
                    matrix[col][row] = dis
                    p[col][row] = p[temp][row]
    print (matrix[target])

dijstra()
#floyd()



