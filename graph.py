import sys
inf = sys.maxint
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
    while 0 in visited:
        cur = target
        min_dis = sys.maxint
        for i in range(len(matrix)):
            if visited[i] == 0:
                last = set[-1]
                dis = distance[last] + matrix[last][i]
                if dis < distance[i]:
                    distance[i] = dis
                if distance[i] < min_dis :
                    min_dis = distance[i]
                    cur = i
        visited[cur] = 1
        distance[cur] = min_dis
        set.append(cur)
    print(distance)

dijstra()


