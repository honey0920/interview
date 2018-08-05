import sys
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

def re(string, pattern):
    if string == '' and pattern == '':
        return True
    if string != '' and pattern == '':
        return False

    if len(pattern) == 1:
        if  string[0] == pattern[0] and len(string) == 1:
            return True
        elif pattern[0] == '.' and len(string) == 1 :
            return True
        else :
            return False
    else:
        if pattern[1] == '*':
           if pattern[0] == string[0] or pattern[0] == '.':
               return re(string[1:], pattern[2:]) or re(string, pattern[2:]) or re(string[1:], pattern)
           else :
               return re(string, pattern[2:])
        if string[0] == pattern[0] or pattern[0] == '.':
            return re(string[1:], pattern[1:])
    return False

def atoi(s):
    sign = 1
    if s[0] == '-':
        sign = -1
        s = s[1:]
    elif s[0] == '+':
        s = s[1:]
    num = 0
    for i in s:
        if i >= '0' and i <= '9':
            num = num * 10 + (ord(i) - ord('0'))
            if (sign and num > sys.maxsize) or (sign == -1 and num < -sys.maxsize - 1 ):
                num = 0
                break
        else :
            num = 0
            break
    return int(num*sign)


string = "aacbad"
pattern = ".*cbad"
print(atoi("-123"))
print(re(string, pattern))
print(dp(string))
print(manacher(string))
