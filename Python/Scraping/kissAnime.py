#!/usr/bin/python3
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
import re

_URL = 'https://kissanime.ru/'

# functional
html = requests.get(_URL, headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"})
bsObj = soup(html.text, "lxml")
print(bsObj)
# urls = bsObj.findAll("a", {"href": re.compile(".https://kissanime.ru/Anime/.")})
# for url in urls:
#     print(url.text)
    # resObj = requests.get(url['href'], stream = True)
    # with open('BankFiles/'+url.text+'.xlsx','wb') as file:
    #     file.write(resObj.content)
