import time
t1 = time.time()
import re

def backward_segment(text, dic):
    word_list = []
    i = len(text) - 1
    while i >= 0:                                   # 掃描位置作為終點
        longest_word = text[i]                      # 掃描位置的單字
        for j in range(0, i):                       # 遍歷[0, i]區間作為待查詢詞語的起點
            word = text[j: i + 1]                   # 取出[j, i]區間作為待查詢單詞
            if word in dic:  
                if len(word) > len(longest_word):   # 越長優先順序越高
                    longest_word = word
                    
        dic[longest_word] +=1        
        word_list.insert(0, longest_word)           # 逆向掃描，所以越先查出的單詞在位置上越靠後
        i -= len(longest_word)
    return word_list

def forward_segment(text, dic):
    word_list = []
    i = 0
    while i < len(text):
        longest_word = text[i]                      # 當前掃描位置的單字
        for j in range(i + 1, len(text) + 1):       # 所有可能的結尾
            word = text[i:j]                        # 從當前位置到結尾的連續字串
            if word in dic:   # 在詞典中
                
                if len(word) > len(longest_word):   # 並且更長
                    longest_word = word             # 則更優先輸出
                   
        dic[longest_word] += 1          
        word_list.append(longest_word)              # 輸出最長詞
        i += len(longest_word)                      # 正向掃描
    return word_list
def to_region(segmentation: str) -> list:
    """
    將分詞結果轉換為區間
    :param segmentation: 商品 和 服務
    :return: [(0, 2), (2, 3), (3, 5)]
    """
    region = []
    start = 0
    for word in re.compile("\\s+").split(segmentation.strip()):
        end = start + len(word)
        region.append((start, end))
        start = end
    return region
  
with open('lexicon1_raw_nosil.txt', encoding='UTF-8',mode = "r") as f:
  fdic={}
  bdic={}
  lines=f.read().splitlines()
  for i in range(len(lines)):
      lines[i]=lines[i].split(" ")[0:1]         #去除破音字
      lines[i] = "".join( lines[i])             
  
  for i in lines:
      fdic[i] = 0    
      bdic[i] = 0

with open('GigaWord_text_lm.txt', encoding='UTF-8',mode = "r") as q,open('GigaWord_text_lm.txt', encoding='UTF-8',mode = "r") as t:
    A_size, B_size, A_cap_B_size = 0, 0, 0
    for i in q:
        line = i.replace(" ", "").replace("\n", "") 
        
        line1 = i.replace("\n", "") 
        a = forward_segment(line, fdic)
        a = " ".join(a)
        
        A=set(to_region(line1))             #計算P、R、F1
        B=set(to_region(a))                 #計算P、R、F1
        A_size += len(A)                    #計算P、R、F1
        B_size += len(B)                    #計算P、R、F1
        A_cap_B_size += len(A & B)          #計算P、R、F1
    p, r = A_cap_B_size / B_size * 100, A_cap_B_size / A_size * 100  #計算P、R、F1
    f1=2 * p * r / (p + r)                                           #計算P、R、F1
    print('P:'"%.2f" % p+'R:'+"%.2f" % r+'F1:'+"%.2f" % f1)     
    A_size, B_size, A_cap_B_size = 0, 0, 0
    for j in t:
       
       bline = j.replace(" ", "").replace("\n", "")
       line1 = j.replace("\n", "") 
       ba = backward_segment(bline, bdic)
       ba = " ".join(ba)
       
       A=set(to_region(line1))             #計算P、R、F1
       B=set(to_region(ba))                #計算P、R、F1
       A_size += len(A)                    #計算P、R、F1 
       B_size += len(B)                    #計算P、R、F1
       A_cap_B_size += len(A & B)          #計算P、R、F1
    p, r = A_cap_B_size / B_size * 100, A_cap_B_size / A_size * 100    #計算P、R、F1
    f1=2 * p * r / (p + r)                                             #計算P、R、F1 
    print('P:'"%.2f" % p+'R:'+"%.2f" % r+'F1:'+"%.2f" % f1)          


fso = sorted(fdic.items(), key=lambda x:x[1], reverse=True)
fwe = open("testwf.csv","w")
for i in range(100):
    fwe.write(str(fso[i][0])+","+str(fso[i][1])+"\n")               #寫入數量最多的前100個詞
bso = sorted(bdic.items(), key=lambda x:x[1], reverse=True)
bwe = open("testwb.csv","w")
for i in range(100):
    bwe.write(str(bso[i][0])+","+str(bso[i][1])+"\n")               #寫入數量最多的前100個詞
bwe.close()
fwe.close()
t2 = time.time()
print('time elapsed: ' + str(round(t2-t1, 2)) + ' seconds')
print('time elapsed: ' + str(t2-t1) + ' seconds')