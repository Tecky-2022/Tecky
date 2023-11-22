from bs4 import BeautifulSoup
from googlesearch import search
import requests

query = input()
flag=0
for j in search(query, tld="co.in", num=10, stop=10, pause=2):
    if "geeksforgeeks" in j or "w3schools" in j or "wikipedia" in j:
        url=j
        print(url)
        print("\n\n")
        htm=requests.get(url)
        soup=BeautifulSoup(htm.text,'lxml')
        dat=soup.find('p').get_text()
        if len(dat)>10:
            print(dat)
            flag=1
            break

if flag==0:
    print("Sorry! No relevant results found")
