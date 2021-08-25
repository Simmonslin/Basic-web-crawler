import requests
from bs4 import BeautifulSoup
import pandas as pd

req=requests.get("http://jwlin.github.io/py-scraping-analysis-book/ch2/blog/blog.html")

soup=BeautifulSoup(req.text,"lxml")

div_data=soup.find_all("h4",{"class":"card-title"})

headers=pd.Series(([[i.text for i in div_data[i].find_all("a")]for i in range(len(div_data))]))



#%%
intro_data=soup.find_all("div",{"class":"content"})

intro=pd.Series([i.p.text.strip() for i in intro_data ])

intro=intro.str.replace("Read More","").str.replace("(","").str.replace(")","").str.replace("[1-6]","")

#%%
# concat --> series 排列  join--> DataFrame排列
content=pd.concat([headers,intro],axis=1)
content.columns=["主題","標題"]
content["主題"]=content["主題"].astype(str).str.replace("[|[|'|]|]|]","")
#%%
content["領域"]=pd.Series([i.h6.text.strip() for i in intro_data])



#%%   <h>標籤資料抓取
req_h=requests.get("https://www.dotblogs.com.tw/YiruAtStudio")
soup_h=BeautifulSoup(req_h.text,"lxml")

# 也可用 re + regex  --> .find_all(re.compile("h[1-6]"))
h_data=soup_h.find_all(["h1","h2","h3","h4","h5","h6"])

title=[]
for i in range(len(h_data)):
    print(i)
    title.append(h_data[i].text)
    
title_2=[i.text for i in h_data]
    
#%%  抓取圖片
req_img=requests.get("https://www.cakenobel.com.tw",verify=False)
soup_img=BeautifulSoup(req_img.text,"lxml")


# image_data=soup_img.find_all("img",{"src":re.compile(".jpg")})
# 若為結尾含h2-pic-02.png圖片 , 則.find_all("img",{"src":re.compile(".jpg")})
image_data=soup_img.find_all("img")

for i in image_data:
    if "src" in i.attrs:
        if i["src"].endswith(".png"):
            print(i["src"])
            
            
#%% 爬出網頁<table>內資料

req_table=requests.get("http://blog.castman.net/py-scraping-analysis-book/ch2/table/table.html")
soup_table=BeautifulSoup(req_table.text,"lxml",)
print(req_table.status_code)
thead=soup_table.find("thead").find("tr").find_all("th")

thead=[i.text for i in thead]
thead=thead[0:3]
tbody=soup_table.find("tbody").find_all("tr")

tbody_price=pd.Series([i.find_all("td")[2].text for i in tbody])
tbody_level=pd.Series([i.find_all("td")[1].text for i in tbody])
tbody_course=pd.Series([i.find_all("td")[0].text for i in tbody])
tbody_table=pd.DataFrame(pd.concat([tbody_course,tbody_level,tbody_price],axis=1))
tbody_table.columns=thead

#%%
import re
t_link=soup_table.find("tbody").find_all("a",{"href":re.compile(".com")})

for i in t_link:
    # dict 取法
    print(i["href"])
    
t_src=soup_table.find("tbody").find_all("img",{"src": re.compile(".png")})

for i in t_src:
    print(i["alt"])
    
#%% 爬取本周電影資訊

req_movie=requests.get("https://movies.yahoo.com.tw/movie_thisweek.html?guccounter=1")
soup_movie=BeautifulSoup(req_movie.text,"lxml")

movie_intro=soup_movie.find_all("div",{"class":"release_movie_name"})
movie_leveltext=soup_movie.find_all("div",{"class":"leveltext"})
movie_time=soup_movie.find_all("div",{"class":"release_movie_time"})
movie_content=soup_movie.find_all("div",{"class":"release_text"})

movie_title=pd.Series([i.find_all("a")[0].text.strip() for i in movie_intro])
movie_level=pd.Series([i.find_all("span")[0].text.strip() for i in movie_leveltext])
movie_release=pd.Series([i.text for i in movie_time])
movie_content=pd.Series([i.find_all("span")[0].text.strip() for i in movie_content])
new_movie_df=pd.concat([movie_title,movie_level,movie_release,movie_content],axis=1)
new_movie_df.columns=["片名","好感度","上映日期","電影簡介"]

#%%
import time
def get_movie_schedule(url):
    import requests
    from bs4 import BeautifulSoup
    req_movie=requests.get(url)
    soup_movie=BeautifulSoup(req_movie.text,"lxml")

    
    movie_intro=soup_movie.find_all("div",{"class":"release_movie_name"})
    movie_leveltext=soup_movie.find_all("div",{"class":"leveltext"})
    movie_time=soup_movie.find_all("div",{"class":"release_movie_time"})
    movie_content=soup_movie.find_all("div",{"class":"release_text"})
    
    movie_title=pd.Series([i.find_all("a")[0].text.strip() for i in movie_intro])
    movie_level=pd.Series([i.find_all("span")[0].text.strip() for i in movie_leveltext])
    movie_release=pd.Series([i.text for i in movie_time])
    movie_content=pd.Series([i.find_all("span")[0].text.strip() for i in movie_content])
    new_movie_df=pd.concat([movie_title,movie_level,movie_release,movie_content],axis=1)
    new_movie_df.columns=["片名","好感度","上映日期","電影簡介"]
    
    return movie_title,movie_level,movie_release,movie_content,new_movie_df
    
for i in range(1,3):
    movie=get_movie_schedule("https://movies.yahoo.com.tw/movie_thisweek.html?page="+str(i))
    time.sleep(1)
    


#%%

import time


movie_title=[]
movie_level=[]
movie_release=[]
movie_content=[]
    
    


def get_movie_schedule(url):
    import requests
    from bs4 import BeautifulSoup
    

    
    
    req_movie=requests.get(url)
    soup_movie=BeautifulSoup(req_movie.text,"lxml")
    
    movie_intro=soup_movie.find_all("div",{"class":"release_movie_name"})
    movie_leveltext=soup_movie.find_all("div",{"class":"leveltext"})
    movie_time=soup_movie.find_all("div",{"class":"release_movie_time"})
    movie_content_find=soup_movie.find_all("div",{"class":"release_text"})
    
    for i in movie_intro:
        movie_title.append(i.find_all("a")[0].text.strip())
        
    for i in movie_leveltext:
        movie_level.append(i.find_all("span")[0].text.strip())
    
    for i in movie_time:
        movie_release.append(i.text)

    for i in movie_content_find:
        movie_content.append(i.find_all("span")[0].text.strip())  
        
    return movie_title,movie_level,movie_release,movie_content


for i in range(1,3):
     get_movie_schedule("https://movies.yahoo.com.tw/movie_thisweek.html?page="+str(i))
     time.sleep(1)
     
#%%

def movie_DataFrame(list_1,list_2,list_3,list_4):
    list_1=pd.Series(list_1)
    list_2=pd.Series(list_2)
    list_3=pd.Series(list_3)
    list_4=pd.Series(list_4)
    
    new_movie_df=pd.concat([list_1,list_2,list_3,list_4],axis=1)
    new_movie_df.columns=["片名","好感度","上映日期","電影簡介"]
    return new_movie_df 

new_movie_df=movie_DataFrame(movie_title,movie_level,movie_release,movie_content)
    

   

#%%  爬取股票資訊

import requests
from bs4 import BeautifulSoup
#網址後方加上個股資訊. ex中華電信: TPE: 2412
def stock_info(stock_code):
    targetURL = "https://www.google.com/search?q=TPE:%20"+str(stock_code)
    headers={"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/66.0.3359.181 Safari/537.36'}
    req_stock=requests.get(targetURL,headers=headers)
    soup_stock=BeautifulSoup(req_stock.text,"lxml")
    
    soup_stock=soup_stock.find_all("div",{"class":"ZSM8k"})
    
    stock_key=[]
    stock_value=[]
    for i in soup_stock:
        for j in range(0,5,2):
            stock_key.append(i.find_all("td")[j].text)
        
    for i in soup_stock:
        for j in range(1,6,2):
            stock_value.append(i.find_all("td")[j].text)
            
    chunghua_telecom=pd.Series(index=stock_key,data=stock_value)
    
    return chunghua_telecom

if __name__ == '__main__':
    tsmc_stock=stock_info(2330)
    


#%%










    





