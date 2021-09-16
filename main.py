# -*- cod=ing = utf-8 -*-
# @Time ：2021/9/11 22:11
# @Author ：方
# @File ：Sensitive_Words.py
# @Software：PyCharm

import time
import pypinyin
import sys
time1 = time.time()
# 字典SenWordDict，用来存组合后的拼音与原汉字的对应关系，key:拼音，value:汉字，因为汉字对应的拼音不唯一
SenWordDict = {}
# 特殊符号集sign
sign = r'~!@#$%^&*()_+`-={}|[]\:";\'<>?,./-*~！@#￥%……&*（）——+·-={}|【】、：“；‘《》？，。、 '
letter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
answer = []


class SensitiveWords:
    # 初始化
    def __init__(self):
        self.SenWordMap = {}  # 敏感词链表
        self.delimit = 'isEnd'  # 叶子节点
        self.totalwords = 0  # 累计匹配到的敏感词总数

    # 分析每行敏感词
    def analyze(self, path, bspath):
        with open(path, encoding='utf-8') as f0:
            # 处理敏感词文档中的每一行
            for eachline in f0:
                self.handle_sensitivewords(str(eachline).strip(), bspath)
            # print(SenWordDict)
            # 将字典中的每一个key值，即拼音分别存入trie树中
            for key, value in SenWordDict.items():
                self.create_sensitivewordsmap(key)
            # 输出trie树
            # print(self.SenWordMap)

    # 处理敏感词，先匹配中文部首再获取拼音并组合
    def handle_sensitivewords(self, line0, bushoupath1):
        words = line0.strip()  # 敏感词去除首尾空格和换行
        bushou = []
        bsflag = 0      # 标志是中文，有部首
        if words[0] not in letter:
            bsflag = 1
            with open(bushoupath1, encoding='utf-8') as fb:
                txt = fb.read()
                txtlist = list(txt)
                for ch in words:
                    for i in range(len(txtlist)):
                        if ch == txtlist[i]:
                            str1 = ""
                            for j in range(i + 1, i + 3):
                                str1 += txtlist[j]
                            bushou.append(str1)
                # print(bushou)
        self.transform(words, bushou, bsflag)

    # 将每个敏感词转化为拼音，并进行排列组合
    def transform(self, words, bs, bsflag):
        senwordlist = []
        i = 0
        # 遍历每个敏感词中的每一个字符
        for char in words:
            complete = ""
            initials = ""
            for item1 in pypinyin.pinyin(char, style=pypinyin.NORMAL):    # 不带声调的拼音
                initials += "".join(item1[0][0])  # 存入首字母
                complete += "".join(item1)     # 存入完整拼音
                if bsflag == 0:     # 是英文
                    senwordlist.append([complete, initials, complete])
                else:       # 是中文
                    # print("bs[%d]=%s"%(i,bs[i]))
                    senwordlist.append([complete, initials, bs[i]])
                    i += 1
        # print(senwordlist)
        if not words:
            return
        self.combine_char(0, len(words), '', words, senwordlist)

    # 通过递归将完整拼音和首字母做排列组合，得到类似['xiej','xjiao']
    def combine_char(self, cnt, wordslen, ch, value, swlist):
        # cnt：计数
        # wordslen：保留每个词的总长度
        # ch：当前累计的字符
        # value：原汉语
        # swlist：本行的敏感词列表
        if cnt == wordslen:
            SenWordDict[ch] = value
            # print(SenWordDict)
            return
        str1 = ch + swlist[cnt][0]
        # print("str1=%s"%str1)
        self.combine_char(cnt + 1, wordslen, str1, value, swlist)
        str2 = ch + swlist[cnt][1]
        # print("str2=%s"%str2)
        self.combine_char(cnt + 1, wordslen, str2, value, swlist)
        str3 = ch + swlist[cnt][2]
        # print("str3=%s" % str3)
        self.combine_char(cnt + 1, wordslen, str3, value, swlist)

    # 创建敏感词树trie
    def create_sensitivewordsmap(self, words):
        if not words:   # 敏感词为空
            return
        # print("words=%s"%words)
        nowmap = self.SenWordMap
        nextmap = {}
        nextwords = ""
        length = len(words)
        # print(length)
        for i in range(length):  # 遍历敏感词中的每个字符
            # 如果这个字已经存在于链表中就进入子字典
            if words[i] in nowmap:
                nowmap = nowmap[words[i]]
            # 如果不存在，就建立新表
            else:
                j = i
                while j < length:
                    # print("words[%d]=%s"%(j,words[j]))
                    if words[j] in letter:      # 如果是拼音或英文
                        nowmap[words[j]] = {}
                        nextmap, nextwords = nowmap, words[j]
                        nowmap = nowmap[words[j]]
                        j += 1
                    else:       # 如果是中文，说明是偏旁部首，占两个
                        s = words[j]+words[j+1]
                        # print("%d:%s"%(j,s))
                        nowmap[s] = {}
                        nextmap, nextwords = nowmap, s
                        nowmap = nowmap[s]
                        j += 2
                    if j >= length:
                        break
                nextmap[nextwords] = {self.delimit: 0}
                break
        nowmap[self.delimit] = 0
        # print(self.SenWordMap)

    # 匹配敏感词
    def match_sensitivewords(self, text, linecnt1):
        # text = text.strip()  # 敏感词去除首尾空格和换行
        ptr = 0     # 索引
        # 整行
        while ptr < len(text):
            nowmap = self.SenWordMap
            signflag = 0  # 判断符号是否夹在敏感词中
            swwords = ""  # 存入敏感词词库中的value
            cnt = 0
            # print("cnt===%d" % cnt)
            exitflag = 0
            # 对整行处理
            # print(text[ptr:])
            for char in text[ptr:]:     # 遍历每个词
                pinyinstr = ""
                for item0 in pypinyin.pinyin(char, style=pypinyin.NORMAL):
                    pinyinstr += "".join(item0)
                # print("ptr=%d,string=%s" % (ptr, pinyinstr))

                # 符号夹在敏感词中
                if signflag == 1 and pinyinstr[0] in sign:
                    cnt += 1
                    # print("cnt==%d" % cnt)
                    continue
                # 数字夹在夹在敏感词中
                if signflag == 1 and pinyinstr[0].isdigit():
                    cnt += 1
                    # print("cnt==%d" % cnt)
                    continue

                start = ptr     # 记录下敏感词在原文中匹配到的起始位置
                for ch in pinyinstr:
                    ch = ch.lower()     # 若碰到大写，先转化为小写
                    # 如果该字符在链表中
                    if ch in nowmap:
                        signflag = 1
                        swwords += ch
                        # 如果匹配到不是词尾，就进入子链表
                        if self.delimit not in nowmap[ch]:
                            nowmap = nowmap[ch]
                        # 如果匹配到是词尾，就退出循环
                        else:
                            self.totalwords += 1  # 敏感词总数加一
                            ptr += cnt  # 更新索引
                            end = ptr + 1   # 记录下敏感词在原文中匹配到的终止位置
                            textswwords = text[start:end]  # 原文敏感词
                            # 将三个值存为一行字符串，便于输出
                            answer.append("Line%d: <%s>%s" % (linecnt1, SenWordDict[swwords], textswwords))
                            signflag = 0
                            exitflag = 1
                            break
                    # 如果该字符不在,就不匹配，退出循环
                    else:
                        # swwords = ""
                        exitflag = 1
                        break
                if exitflag == 1:
                    break
                cnt += 1
            ptr += 1
        return self.totalwords


if __name__ == "__main__":
    '''  
    sys.argv[1]     # 敏感词文件
    sys.argv[2]     # 待检测文件
    sys.argv[3]     # 答案文件  
    '''
    sw = SensitiveWords()
    sw.analyze(sys.argv[1], "bushou.txt")
    with open(sys.argv[2], encoding='utf-8') as f:
        lines = f.readlines()
        linecnt = 0
        total = 0
        for line in lines:
            linecnt += 1
            total = sw.match_sensitivewords(line, linecnt)
    with open(sys.argv[3], "w+", encoding='utf-8') as f1:
        f1.write("Total: %d\n" % total)
        # print("Total: %d"%total)
        for item in answer:
            f1.write(item)
            f1.write('\n')
            # print(item)

    time2 = time.time()
    print("耗时：%ss" % str(time2-time1))
