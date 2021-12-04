from pyvirtualdisplay import Display
from selenium import webdriver
import time
import datetime
import requests
import schedule

with Display():
    # we can now start Firefox and it will run inside the virtual display
    # browser = webdriver.Firefox()

    # put the rest of our selenium code in a try/finally
    # to make sure we always clean up at the end
    try:
        data = {"varun": {"username": "IA0892", "password": "Pass@1234"},
                "shweta": {"username": "IA0597", "password": "ynp@eia%"}}


        URL = "http://sms6.rmlconnect.net/bulksms/bulksms?"
        destination = "8109055354"
        destination2 = "9892727524"

        PARAMS = {'username': "avenues", "password": "zerb5rv", "type": "0",
                  "dlr": "1", "source": "CCAVEN"}


        def punch():

            day = datetime.datetime.today().weekday()
            date = datetime.datetime.now().day

            if (day == 5) and ((7 < date < 15) or (21 < date < 29)):
                pass
                print("Pass")

            else:
                print("Punching")
                for i in data:

                    browser = webdriver.Firefox()
                    browser.get(
                        "http://hralign.avenues.info/HRAlign_Avenue_LIVE/login.spr")

                    time.sleep(10)

                    username = browser.find_element_by_id("username")
                    password = browser.find_element_by_id("password")

                    username.send_keys(data[i]["username"])
                    password.send_keys(data[i]["password"])

                    browser.find_element_by_xpath(
                        '//*[@id="contact"]/div/div/div[4]/button').click()

                    time.sleep(5)

                    try:
                        browser.find_element_by_xpath(
                            '//*[@id="moodIe"]/div/div/ul/li[1]/img').click()
                    except:
                        print("Unable to locate element: Sad Smiley")
                    try:
                        time.sleep(5)
                        browser.find_element_by_xpath(
                            '//*[@id="header"]/header/ul/li[1]').click()

                        time.sleep(5)
                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[6]/div/div[4]/div[1]/button').click()
                        except:
                            browser.find_element_by_xpath(
                                '/html/body/div[3]/div/div[4]/div[1]/button').click()
                        time.sleep(10)
                        try:
                            PARAMS["message"] = i + " is Done!"
                            PARAMS["destination"] = destination
                            response = requests.get(url=URL, params=PARAMS)
                            if i == "shweta":
                                PARAMS["message"] = "Your punching Done!"
                                PARAMS["destination"] = destination2
                                response = requests.get(url=URL, params=PARAMS)
                        except:
                            print("SMS service might not be working!!")
                        browser.quit()
                        time.sleep(60)
                    except:
                        print("Unable to locate element: Log Button")


        schedule.every().monday.at("09:30").do(punch)
        schedule.every().monday.at("19:00").do(punch)

        schedule.every().tuesday.at("09:30").do(punch)
        schedule.every().tuesday.at("19:00").do(punch)

        schedule.every().wednesday.at("09:30").do(punch)
        schedule.every().wednesday.at("19:00").do(punch)

        schedule.every().thursday.at("09:30").do(punch)
        schedule.every().thursday.at("19:00").do(punch)

        schedule.every().friday.at("09:30").do(punch)
        schedule.every().friday.at("19:00").do(punch)

        schedule.every().saturday.at("09:30").do(punch)
        schedule.every().saturday.at("14:00").do(punch)


        while True:
            schedule.run_pending()
            time.sleep(1)

    finally:
        browser.quit()
