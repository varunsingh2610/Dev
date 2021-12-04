#!/usr/bin/python3

# packages to install
# zope.interface, constantly, incremental, attrs, Automat, hyperlink, PyHamcrest, Twisted, queuelib, pyasn1, pyasn1-modules, asn1crypto, cryptography, service-identity, pyOpenSSL, PyDispatcher, w3lib, cssselect, parsel, scrapy, scrapy-useragents
#
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, build_opener
import re


opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')]
response = opener.open('https://kissanime.ru/Anime/Kimetsu-no-Yaiba')
html_contents = response.read()


# req = Request('https://kissanime.ru/Anime/Kimetsu-no-Yaiba', headers={'User-Agent': 'Mozilla/5.0'})
# page = urlopen(req).read()
#
# soup = BeautifulSoup(page, 'html.parser')



# url = 'https://kissanime.ru/Anime/Kimetsu-no-Yaiba'
# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
# request = Request(url,headers={'User-Agent': user_agent})
# response = urlopen(request)
# html = response.read()
