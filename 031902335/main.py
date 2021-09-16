# -*- cod=ing = utf-8 -*-
# @Time ：2021/9/3 13:08
# @Author ：方
# @File ：demo1.py
# @Software：PyCharm
 
def parse():
    f=open(r'C:\Users\44832\Desktop\SensitiveWords_check\article.txt','r',encoding='UTF-8')
    lines=f.readlines()
    f.close()
 
    import re
    punc = '~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}'
    #cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")  # 匹配不是中文、大小写、数字的其他字符
 
    f1=open(r'C:\Users\44832\Desktop\SensitiveWords_check\article2.txt','w',encoding='UTF-8')
    for line in lines:
        string1=re.sub(r"[%s]+" % punc, "", line)
        #line=cop.sub('',line)
        f1.write(string1)
        #f1.write('\n')
    f1.close()
 
if __name__ == "__main__":
    parse()
