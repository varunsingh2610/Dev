#!/usr/bin/python3
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import requests
import shutil
import os
import threading
from multiprocessing.pool import ThreadPool as Pool
#
_URL = 'https://www.rbi.org.in/Scripts/bs_viewcontent.aspx?Id=2009'
pool_size = 5
pool = Pool(pool_size)
def downloadfiles(text, resObj):
    print(text)
    with open('bankFiles/'+text+'.xlsx','wb') as file:
        file.write(resObj.content)


# functional
shutil.rmtree('/home/varun.singh/Dev/Python/Scraping/bankFiles',
              ignore_errors=True, onerror=None)
os.makedirs(
    '/home/varun.singh/Dev/Python/Scraping/bankFiles')

# functional
count = 0
name = []
html = uReq(_URL)
bsObj = soup(html, "html.parser")
urls = bsObj.findAll(
    "a", {"href": re.compile(".rbidocs.rbi.org.in/rdocs/.")})
total = len(urls)-1
for url in urls:
    # if(count == 5):
    #     break
    if url.text not in name:
        if url['href'][:5] != 'https':
            url['href'] = 'https'+url['href'][4:]
        resObj = requests.get(url['href'], stream = True)
        pool.apply_async(downloadfiles, (url.text, resObj))

        count += 1
        print(count)



pool.close()
pool.join()
