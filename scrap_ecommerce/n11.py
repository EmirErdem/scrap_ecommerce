from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

list=[]
page=1
while page<=10:
  header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"}
  url="https://www.n11.com/bilgisayar/cevre-birimleri/kulaklik-ve-mikrofon?pg="+str(page)+""

  get=requests.get(url,headers=header)
  content=get.content
  soup=BeautifulSoup(content,"lxml")

  p = soup.find_all("li", attrs={"class": "column"})

  for link in p:
    links=link.a.get("href")
    product_name = link.find("h3", attrs={"class": "productName"}).text.strip()
    old_price = str(link.find("span", attrs={"class": "oldPrice cPoint priceEventClick"}))
    old_price=re.sub("<.*?>", "", old_price).strip()
    price = link.find("span", attrs={"class": "newPrice cPoint priceEventClick"}).text.strip()
    free_shipping = link.find("span", attrs={"class": "cargoBadgeText"}).text.strip().replace("ÜCRETSİZ KARGO","var").replace("None","yok")
    review_count = link.find("span", attrs={"class": "ratingText"}).text.strip("()")
    number_of_products = str(link.find('div', {'class': 'badgeItem'}))
    number_of_products = str(re.findall("src=\".*?\"", number_of_products)).replace("[]","").replace("['src=\"","").replace("\"']","").\
      replace("https://n11scdn.akamaized.net/a1/org/22/02/24/62/53/73/94/24/80/86/14/07/9785087381537011610.png","").\
      replace("https://n11scdn.akamaized.net/a1/org/22/05/30/89/74/72/83/53/92/92/53/57/34570407203254977414.png","").\
      replace("https://n11scdn.akamaized.net/a1/org/22/05/30/84/94/93/75/20/96/77/67/96/63104252748620086859.png","son kalan 1 ürün").\
      replace("https://n11scdn.akamaized.net/a1/org/22/05/30/74/97/24/73/93/38/93/96/39/42560667209980724364.png","son kalan 3 ürün").\
      replace("https://n11scdn.akamaized.net/a1/org/22/05/30/48/70/62/93/77/58/60/63/32/81730332650147723759.png","son kalan 2 ürün")


    list.append([product_name,links,number_of_products,old_price,price,free_shipping,review_count])

  page = page + 1


df = pd.DataFrame(list)
df.columns = ["Product_name","links","number_of_products","old_price","price","free_shipping","review_count"]
df.to_csv("data\n11.csv")
