# from twilio.rest import Client
#
# account_sid = 'AC8389590356ee5d239b8bb4cc1d2b713d' # Found on Twilio Console Dashboard
# auth_token = '4ac02135edc2808c8032a5efae32e70c' # Found on Twilio Console Dashboard
#
# myPhone = '+918109055354' # Phone number you used to verify your Twilio account
# TwilioNumber = '+12019890272' # Phone number given to you by Twilio
#
# client = Client(account_sid, auth_token)
#
# client.messages.create(
#   to=myPhone,
#   from_=TwilioNumber,
#   body='Bhavik Gadhe! ' + u'\U0001f680')


import requests

message = "This message from python!"
url = "https://www.fast2sms.com/dev/bulk"
payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers=8109055354"
headers = {
'authorization': "vZelsaJT89xKHWGq7XLwhojOdCpRBQUbzYgi3N4tc12D6mykMIkg71cqvy5Kr8GoUJIwplSzTQV9xhnX",
'Content-Type': "application/x-www-form-urlencoded",
'Cache-Control': "no-cache",
}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
