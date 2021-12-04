import requests
import bs4
res = requests.get('https://kissanime.ru')
res.raise_for_status()
noStarchSoup = bs4.BeautifulSoup(res.text, "lxml")
type(noStarchSoup)

exampleFile = open('example.html')
exampleSoup = bs4.BeautifulSoup(exampleFile)
type(exampleSoup)
