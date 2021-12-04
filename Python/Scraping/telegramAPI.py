#!/usr/bin/python3
import requests


def telegramBot(message):

    bot_token = '869841352:AAHKqw7LDWSuGmIUdeuPWBP2aXY1G484-wU'
    bot_chatID = '-305083559'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + \
        bot_chatID + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)

    return response.json()


result = telegramBot("I will send price of products every day in a day or two!!")
# print(result)
