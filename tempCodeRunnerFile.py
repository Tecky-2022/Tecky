for j in search(query, tld="co.in", num=1, stop=1, pause=2):
    url=j
    print(url)
    print("\n\n")
    
htm=requests.get(url)
soup=BeautifulSoup(htm.text,'lxml')
dat=soup.find('p').get_text()
print(dat)