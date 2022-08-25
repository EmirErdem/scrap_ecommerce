from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


list=[]
page=1
while page<=10:
  header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"}
  url="https://www.ciceksepeti.com/bluetooth-kulaklik?page="+str(page)+""

  get=requests.get(url,headers=header)
  content=get.content
  soup=BeautifulSoup(content,"lxml")

  p = soup.find_all("div", attrs={"class": "products__item js-category-item-hover js-product-item-for-countdown js-product-item"})

  for link in p:
    domain = "https://www.ciceksepeti.com"
    links =domain+link.a.get("href")
    product_name = link.find("p", attrs={"class": "products__item-title"}).text.strip()
    payment_option = link.find("p", attrs={"class": "products__installment"}).text.strip()
    price= link.find("div", attrs={"class": "price price--now"}).text.strip()
    old_price = str(link.find("div", attrs={"class": "price price--old"}))
    old_price=re.sub("<.*?>", "", old_price).strip()
    discount = str(link.find("span", attrs={"class": "discount-percentage__text"}))
    discount = re.sub("<.*?>", "", discount).strip()
    shipping = link.find("span", attrs={"class": "products__item-badge-text"}).text.strip()
    review_count = str(link.find("span", attrs={"class": "products-stars__review-count"}))
    review_count= re.sub("<.*?>", "", review_count).strip("()").replace("None","0")


    list.append(
      [product_name,links,old_price,discount,price,payment_option,shipping,review_count])
  page = page + 1


df = pd.DataFrame(list)
df.columns = ["product_name","links","old_price","discount","price","payment_option","shipping","review_count"]
df.to_csv("data\ciceksepeti.csv")
