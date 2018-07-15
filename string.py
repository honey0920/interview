def transform(s):
    ss = '#'
    for i in s:
        ss += i
        ss += '#'
    return ss

def manacher(s):
    ss = transform(s)
    res = [0] * len(ss)
    right_index = 0
    center_index = 0
    ans = 0
    index = 0
    for i in range(len(ss)):
        if(right_index > i):
            res[i] = min(right_index - i, res[2* center_index - i])
        else:
            res[i] = 1

        while(i - res[i] >= 0 and i + res[i] < len(ss) and ss[i - res[i]] == ss[i + res[i]]):
            res[i] += 1

        if(i + res[i] > right_index):
            center_index = i
            right_index = i + res[i]

        if(res[i] > ans):
            ans = res[i]
            index = i

    return ss[index-ans+1 : index+ans].replace('#','')

def dp(s):
    ans = 1
    index = 0
    l = len(s)
    record = [[False for col in range(l)] for raw in range(l)]
    for i in range(l):
        record[i][i] = True
        if(s[i-1] == s[i]):
            record[i-1][i] = True
            record[i][i-1] = True

    for i in range(l):
        for j in range(i+1):
            if( j-1>=0 and i+1 < l and record[j][i] and s[j-1] == s[i+1]):
                record[j-1][i+1] = True
                if(i+1 - j +1 +1 > ans):
                    ans = i-j+3
                    index = j-1



    return s[index:index+ans]

string = "abcbad"
print(dp(string))
print(manacher(string))
