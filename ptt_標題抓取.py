# 文件抓取


from bs4 import BeautifulSoup
import requests
import json

url="https://od.cdc.gov.tw/eic/Day_Confirmation_Age_County_Gender_19CoV.json"

req=requests.get(url)

print(req.text)

data=json.loads(req.text)

#%%
import pandas as pd
data=pd.DataFrame(data)

#%%  ptt 八卦版實例

# class 有階層劃分

# 以ppt 八卦版標題欄為例   class: "r-ent" --> "nrec" --> "title" --> "meta"

url_ptt="https://www.ptt.cc/bbs/Gossiping/index.html"
headers={'cookie': 'over18=1'}
req_ptt=requests.get(url_ptt,headers=headers)
print(req_ptt.text)

#%%  單頁面資料爬取

from bs4 import BeautifulSoup

# 用於解析原始碼  再使用標籤與 text 取出內容
soup=BeautifulSoup(req_ptt.text,"lxml")

titles=soup.find_all("div","title")

list_title=[]
for t in titles:
    list_title.append(t.text)
    print(t.text)

# 也可以使用 map() 直接進行整體修改  map( function, iterable --> 指定進行替換的變數)
#  --> list_title_2= list(map(lambda x: x.text, titles))
# map() 執行速度較快

#%%  ptt多頁面資料爬取  --> 利用網址編號特性
import time
import numpy as np

def get_one_page(url):
    import requests
    from bs4 import BeautifulSoup
    headers={'cookie': 'over18=1'}
    req=requests.get(url,headers=headers)
    soup=BeautifulSoup(req.text,"lxml")
    titles=soup.find_all("div","title")
    titles=list(map(lambda x : x.text,titles))
    return titles
    
 
    # 去除空白
    


start=39335
number=10
end=start-number

list_title_ppt=[]
for i in range(start,end,-1):
    url="https://www.ptt.cc/bbs/Gossiping/index"+str(i)+".html"
    list_title_ppt.append(get_one_page(url))
    time.sleep(1)
    

    


#%%

from tkinter import _flatten

list_title_ppt=pd.DataFrame((_flatten(list_title_ppt)))

#%%

print(list_title_ppt[list_title_ppt.iloc[:,0].str.contains("本文已被刪除")].index)

# 以 index 設定需刪除資料
list_title_ppt=list_title_ppt.drop(index=list_title_ppt[list_title_ppt.iloc[:,0].str.contains("本文已被刪除")].index)
def ptt_replace(a,b):
    list_title_ppt.iloc[:,0]=list_title_ppt.iloc[:,0].str.replace(a,b)
    
ptt_replace("\n","")
ptt_replace("\t","")
ptt_replace("\nRe","")
ptt_replace("\u3000","")

#%%
























