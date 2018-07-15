#!/usr/bin/python
# -*- coding: UTF-8 -*-

def dp(weights, values, limit):
    n = len(weights)
    m = limit
    weights.insert(0,0)
    values.insert(0,0)
    optp = [[0 for col in range(m + 1)] for raw in range(n + 1)]

    for i in range(1, n+1):
        for j in range(1, m+1):
            if(weights[i] <= j):
                optp[i][j] = max(optp[i-1][j], optp[i-1][j-weights[i]] + values[i])
            else:
                optp[i][j] = optp[i-1][j]

    return optp[n][m]

w = [ 1, 4, 3, 1]   #n个物体的重量(w[0]无用)
p = [1500, 3000, 2000, 2000]   #n个物体的价值(p[0]无用)
m = 4   #背包的载重量
#print(dp(w,p,m))

lis = [2 ,1, 5, 3, 6 ,4 ,8 ,9, 7, 10, 11]

def lis(s):
    d = [1]*len(s)
    res = 1
    for i in range(len(lis)):
        for j in range(i):
            if lis[j] <= lis[i] and d[i] < d[j]+1:
                d[i] = d[j]+1
            if d[i] >  res:
                res = d[i]
    return res

def lcs(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    record = [[0 for col in range(l2+1)] for raw in range(l1+1)]
    for i in range(1, l1+1):
        for j in range(1, l2+1):
            if(s1[i] == s2[j]):
                record[i][j] = record[i-1][j-1] + 1
            else :
                record[i][j] = max(record[i-1][j] , record[i][j-1])
    return record[l1][l2]

def n_sum(numbers, sum):
    n = len(numbers)
    numbers.insert(0,0)
    record = [[1] + [0] * sum for i in range(n + 1)]
    for i in range(1, n+1):
        for j in range(1, sum+1):
            if(j >= numbers[i]):
                record[i][j] = record[i-1][j] + record[i-1][j-numbers[i]]
            else:
                record[i][j] = record[i-1][j]
    return record[-1][-1]