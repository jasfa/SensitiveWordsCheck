# -*- cod=ing = utf-8 -*-
# @Time ：2021/9/11 22:11
# @Author ：方
# @File ：Sensitive_Words.py
# @Software：PyCharm
 
import time
time1=time.time()
class SensitiveWords:
    # 初始化
    def __init__(self):
        self.SenWordMap = {}  # 敏感词链表
        self.delimit = '\x00'  # 限定
 
    #创建敏感词树
    def Create_SensitiveWordsMsp(self,senwords):
        words= senwords.strip() #敏感词去除首尾空格和换行
        if not words:   #敏感词为空
            return
        nowmap=self.SenWordMap
        length=len(words)
        for i in range(length):#遍历敏感词中的每个字
            #如果这个字已经存在于链表中就进入子字典
            if words[i] in nowmap:
                nowmap=nowmap[words[i]]
            #如果不存在，就建立新表
            else:
                #判断当前对象是不是字典类型，如果是则返回True，否则返回False
                if not isinstance(nowmap,dict):
                    break
                for j in range(i,length):
                    nowmap[words[j]]={}
                    nextmap=nowmap
                    nextwords=words[j]
                    nowmap=nowmap[words[j]]
 
                nextmap[nextwords]={self.delimit: 0}
                break
        if i==length-1:
            nowmap[self.delimit]=0
 
    #分析每行
    def analyze(self,path):
        with open(path,encoding='utf-8') as f:
            for line in f:
                self.Create_SensitiveWordsMsp(str(line).strip())
        print(self.SenWordMap)
 
  
    #匹配敏感词
    def Match_SensitiveWords(self, text):
        ptr = 0
        #i=0
        while ptr < len(text):
            #print("i=%d"%i)
            #i+=1
            cnt = 0
            nowmap = self.SenWordMap
            matchword = []
            flag=0
            #j=0
            for char in text[ptr:]:
                #print("j=%d"%j)
                #j+=1
                # 如果该字符在链表中
                if char in nowmap:
                    cnt += 1
                    if self.delimit not in nowmap[char]:
                        nowmap=nowmap[char]
                        matchword.append(char)
                    else:#到词尾了
                        flag=1
                        ptr+=cnt-1
                        matchword.append(char)
                        break
                else:
                    matchword = []
                    break
            if flag==1:
                for word in matchword:
                    print(word,end="")
                print(end='\n')
            ptr+=1
   
 
if __name__ == "__main__":
    sw=SensitiveWords()
    wordspath=r'C:\Users\44832\Desktop\SensitiveWords_check\words.txt'
    sw.analyze(wordspath)
    textpath=r'C:\Users\44832\Desktop\SensitiveWords_check\texttest.txt'
    #sw.Match_SensitiveWords(textpath)
    #print(text)
    with open(textpath,encoding='utf-8') as f:
        lines=f.readlines()
        for line in lines:
            sw.Match_SensitiveWords(line)
 
    time2=time.time()
    print(str(time2-time1))
