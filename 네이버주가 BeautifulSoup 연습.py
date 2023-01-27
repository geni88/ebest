
#%%
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


#%%

url = "http://dart.fss.or.kr/report/viewer.do?rcpNo=20190722000450&dcmNo=6815487&eleId=0&offset=0&length=0&dtd=dart3.xsd"

res = requests.get(url)

res_soup = bs(res.text)
res_soup


#%%
data = pd.read_html(res.text)    ## pandas 로 html 을 불러들일 경우 BeautifulSoup 으로 파싱하면 안됨.
len(data)


#%%
data[0]


#%%
data[1]


#%%
data[4]


#%%
data[26]


#%%
summary_profit = data[26].iloc[2,3]
summary_profit


#%%
summary_profit2 = data[26].iloc[:,[2,3]]
summary_profit2.columns = ["type", "value"]
summary_profit2


#%%
summary_profit2 = data[26].iloc[1:4,[2,3]]
summary_profit2.columns = ["type", "value"]
summary_profit2


#%%

url = "https://finance.naver.com/item/main.nhn?code=900250"
res_crystal = requests.get(url)
res_crystal.text
soup_crystal = bs(res_crystal.text)
soup_crystal


#%%
dd = soup_crystal.findAll('dd')
dd
#%%
dd[0]

#%%
dd[4]

#%%
dd[4].text.split(" ")[1].replace(", ","")

#%%
dd[4].text.split()

#%%
def get_item(item):
    for i in soup_crystal.findAll('dd') :
        if item in i.text :
            return i.text.split(" ")[1]

#%%
get_item("종목명")
#%%
get_item("거래량")
#%%


#%%


#%%


#%%


#%%
