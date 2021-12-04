import pandas as pd
import os
import glob
from datetime import datetime
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import requests

_URL = 'https://www.myntra.com/shorts/arise/arise-men-black-solid-regular-fit-shorts/5345804/buy'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
}

# html = uReq(_URL)
# bsObj = soup(html, "html.parser")

page = requests.get(_URL, headers=headers)
html = soup(page.content, "html.parser")

print(html)
