from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

list=[]
page=1
while page<=10:
  header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"}
  url="https://www.trendyol.com/kulaklik-x-c92?pi="+str(page)+""

  get=requests.get(url,headers=header)
  content=get.content
  soup=BeautifulSoup(content,"lxml")

  p = soup.find_all("div", attrs={"class": "p-card-wrppr add-to-bs-card"})

  for link in p:
    domain = "https://www.trendyol.com"
    links = domain + link.a.get("href")
    product_name = link.find("div", attrs={"class": "prdct-desc-cntnr"}).text.strip()
    price = link.find("div", attrs={"class": "pr-bx-nm with-org-prc"}).text.strip()
    free_shipping = str(link.find("div", attrs={"class": "stmp fc"}))
    free_shipping=re.sub("<.*?>","",free_shipping).replace("KARGO BEDAVA","var").replace("None","yok")
    fast_delivery=str(link.find("div", attrs={"class": "stmp rd"}))
    fast_delivery = re.sub("<.*?>", "", fast_delivery).replace("HIZLI TESLİMAT","var").replace("None","yok")
    review_count = str(link.find("span", attrs={"class": "ratingCount"}))
    review_count=re.sub("<.*?>", "", review_count).strip("()")



    list.append([product_name,links,price,free_shipping,fast_delivery,review_count])
  page = page + 1

df = pd.DataFrame(list)
df.columns = ["product_name","links","price","free_shipping","fast_delivery","review_count"]
df.to_csv("data\trendyol.csv")