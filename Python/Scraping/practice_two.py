from urllib.request import urlopen
from bs4 import BeautifulSoup
# import BeautifulSoupimport
import re

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "lxml")
for child in bsObj.find("table", {"id": "giftList"}).children:
    print(child)


html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "lxml")
for sibling in bsObj.find("table", {"id": "giftList"}).tr.next_siblings:
    print(sibling)


html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "lxml")
print(bsObj.find("img", {"src": "../img/gifts/img1.jpg"
                         }).parent.previous_sibling.get_text())


html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "lxml")
images = bsObj.findAll("img", {"src": re.compile("\.\.\/img\/gifts/img.*\.jpg")})
for image in images:
    print(image["src"])
