#!/usr/bin/python3
import requests
import schedule
import time
from bs4 import BeautifulSoup as soup
def telegramBot(message):

    bot_token = '869841352:AAHKqw7LDWSuGmIUdeuPWBP2aXY1G484-wU'
    bot_chatID = '-305083559'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + \
        bot_chatID + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)
    return response.json()

def price():
    """
    For OnePlus 7
    """
    onplus_7 = 'https://www.amazon.in/Test-Exclusive-608/dp/B07HGBMJT6/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
    }
    page = requests.get(onplus_7, headers=headers)
    html = soup(page.content, "html.parse")
    # print(html)
    title = html.find('span', id ='productTitle').text.strip()
    price = html.find('span', id ='priceblock_dealprice').text
    if price == None:
        price = html.find('span', id ='priceblock_ourprice').text
    print(title)
    print(price)
    if float(price.strip('₹ ').replace(',','')) < 32999:
        telegramBot("Price drop!")
        telegramBot(title+" "+price+" "+onplus_7)
    else:
        telegramBot(title+" "+price)



    """
    For Asus Zenphone 6
    """
    asus6 = 'https://www.flipkart.com/asus-6z-black-64-gb/p/itmfg5hgqf3hwaj4?pid=MOBFG5HF4AG4DWYT&srno=s_1_1&otracker=AS_Query_OrganicAutoSuggest_7_8&otracker1=AS_Query_OrganicAutoSuggest_7_8&lid=LSTMOBFG5HF4AG4DWYTMJUBLX&fm=SEARCH&iid=d22e71ff-2daf-417d-99f6-209829750f1b.MOBFG5HF4AG4DWYT.SEARCH&ppt=sp&ppn=sp&ssid=ji8549p4v40000001562563081907&qH=08ccb31be1c0c13f'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
    }
    page = requests.get(asus6, headers=headers)
    html = soup(page.content, "html.parse")

    title = html.find('span', {'class': '_35KyD6'}).text
    price = html.find('div', class_='_1vC4OE _3qQ9m1').text
    if float(price.strip('₹').replace(',','')) < 31999:
        telegramBot("Price drop!")
        telegramBot(title+" "+price+" "+asus6)
    else:
        telegramBot(title+" "+price)
        pass

# schedule.every().day.at("11:04").do(price)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
price()

"""
for myntra pdp-name, pdp-price, pdp-mrp, pdp-discount
"""
