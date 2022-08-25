from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

list=[]
page=1
while page<=10:
  header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"}
  url="https://www.hepsiburada.com/ara?q=kulakl%C4%B1k&filtreler=MainCategory.Id:16218&sayfa="+str(page)+""

  get=requests.get(url,headers=header)
  content=get.content
  soup=BeautifulSoup(content,"lxml")
  p=soup.find_all("li",attrs={"class":"productListContent-item"})


  for link in p:
    domain = "https://www.hepsiburada.com"
    links = domain + link.a.get("href")
    product_name = link.find("h3", attrs={"data-test-id":"product-card-name"}).text.strip()
    product_image = link.img.get("src")
    price = link.find("div", attrs={"data-test-id":"price-current-price"}).text.strip().replace("\n", "").replace("\r", "").replace("(Adet )", "").replace("TL", " TL")
    old_price = str(link.find("div", attrs={"data-test-id": "price-prev-price"}))
    old_price= re.sub("<.*?>","",old_price).strip().replace("88A28B56-64F8-4938-A404-582848FCD2DB","")
    old_price=re.sub("\%.*","",old_price)
    discount=str(link.find("div", attrs={"data-test-id":"price-prev-price-discount"}))
    discount = re.sub("<.*?>", "", discount).strip()
    review_count = link.find("div", attrs={"data-test-id":"review"}).text.strip()

    list.append([product_name,product_image,links,old_price,discount,price,review_count])
  page = page + 1


df = pd.DataFrame(list)
df.columns = ["Product_name","product_image","links","old_price","discount","price","review_count"]
df.to_csv("data\hepsiburada.csv")