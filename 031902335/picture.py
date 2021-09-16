# -*- cod=ing = utf-8 -*-
# @Time ：2021/9/16 22:43
# @Author ：方
# @File ：picture.py
# @Software：PyCharm

import matplotlib.pyplot as plt
import sys
'''
sys.argv[1]     # wordspath
sys.argv[2]     # anspath
'''

# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

picdict = {}
with open(sys.argv[1], encoding='utf-8') as fw:
    lines = fw.readlines()
    for line in lines:
        line = line.strip()
        picdict[line] = 0
with open(sys.argv[2], encoding='utf-8') as fa:
    anslines = fa.readlines()
    for ansline in anslines:
        if not ansline:
            break
        string = ""
        flag = 0        # 是否遍历到敏感词中
        for ch in ansline:
            if ch == '<':
                flag = 1
            elif ch == '>':
                flag = 0
            elif flag == 1:
                string += ch
        if len(string):
            picdict[string] += 1

words = ()
wordscnt = []
for item in picdict:
    words += (item,)
    wordscnt.append(picdict[item])

plt.bar(words, wordscnt)
plt.title('敏感词频率')

plt.show()
