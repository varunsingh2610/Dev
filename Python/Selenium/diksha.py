#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import schedule
import time
import pandas as pd

df = pd.read_excel('diksha_sample.xlsx', sheet_name='Sheet1')
df['PASSWORD'] = 'Nan'
df['EMAIL'] = 'Nan'
for i in range(df.shape[0]):
    df['PASSWORD'][i]= df['FIRST NAME'][i].title()+df['LAST NAME'][i].lower()+'@1234'
    df['EMAIL'][i]= df['FIRST NAME'][0].lower()+df['LAST NAME'][0].lower()+'@yopmail.com'


# Create Email
yopmail = webdriver.Firefox()
yopmail.get("http://www.yopmail.com/en/")
time.sleep(5)
yopEmail = yopmail.find_element_by_xpath('//*[@id="login"]')
yopEmail.send_keys(df['FIRST NAME'][0].lower()+df['LAST NAME'][0].lower())
# yopEmail.send_keys('pintubhanware')

time.sleep(5)
yopmail.find_element_by_xpath('/html/body/center/div/div/div[3]/table[3]/tbody/tr/td[1]/table/tbody/tr[3]/td/div[1]/form/table/tbody/tr[1]/td[3]/input').click()
time.sleep(2)
try:
    yopmail.find_element_by_xpath('/html/body/div[3]/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr[1]/td[3]/a/span/span').click()
except:
    yopmail.find_element_by_xpath('/html/body/center/div/div/div[3]/table[3]/tbody/tr/td[1]/table/tbody/tr[3]/td/div[1]/form/table/tbody/tr[1]/td[3]/input').click()
time.sleep(1)


# Register

browser = webdriver.Firefox()
browser.get("https://diksha.gov.in/signup?client_id=portal&state=2a5653a0-f87b-4564-8118-2ef586bf8d9d&redirect_uri=https:%2F%2Fdiksha.gov.in%2Flearn%3Fauth_callback%3D1&scope=openid&response_type=code&version=4&error_callback=https:%2F%2Fdiksha.gov.in%2Fauth%2Frealms%2Fsunbird%2Fprotocol%2Fopenid-connect%2Fauth")
time.sleep(10)
browser.refresh()


browser.find_element_by_xpath('//*[@id="districts"]').click()
time.sleep(2)
# Sagar
# browser.find_element_by_xpath('/html/body/sui-modal[2]/sui-dimmer/div/div/div/div[2]/form/div[2]/div/sui-select/div[3]/sui-select-option[39]/span[2]').click()

# Mandla
browser.find_element_by_xpath('/html/body/sui-modal[2]/sui-dimmer/div/div/div/div[2]/form/div[2]/div/sui-select/div[3]/sui-select-option[28]/span[2]').click()
time.sleep(2)
browser.find_element_by_xpath('/html/body/sui-modal[2]/sui-dimmer/div/div/div/div[3]/button').click()

time.sleep(2)

browser.find_element_by_xpath('//*[@id="email"]').click()

name = browser.find_element_by_xpath("/html/body/sui-modal/sui-dimmer/div/div/div/div/div/div[2]/div/form/div[1]/input")
email = browser.find_element_by_xpath("/html/body/sui-modal/sui-dimmer/div/div/div/div/div/div[2]/div/form/div[4]/input")
password = browser.find_element_by_xpath("/html/body/sui-modal/sui-dimmer/div/div/div/div/div/div[2]/div/form/div[5]/div/input")
repassword = browser.find_element_by_xpath("/html/body/sui-modal/sui-dimmer/div/div/div/div/div/div[2]/div/form/div[6]/input")

name.send_keys(df['FIRST NAME'][0].title()+ ' ' +df['LAST NAME'][0].title())
email.send_keys(df['EMAIL'][0])
password.send_keys(df['PASSWORD'][0])
repassword.send_keys(df['PASSWORD'][0])

browser.find_element_by_xpath('//*[@id="tncAccepted"]').click()
time.sleep(2)
browser.find_element_by_xpath('/html/body/sui-modal/sui-dimmer/div/div/div/div/div/div[2]/div/button').click()
time.sleep(5)


# Get OTP

yopmail.find_element_by_xpath('/html/body/div[3]/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr[1]/td[3]/a/span/span').click()
time.sleep(3)
iframe = yopmail.find_element_by_xpath("//iframe[@name='ifmail']")
yopmail.switch_to.frame(iframe)

content = yopmail.find_element_by_xpath('//*[@id="mailmillieu"]/div[2]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/p').text
OTP = content[41:47]


time.sleep(5)
browser.find_element_by_xpath('//*[@id="board"]/div[1]').click()

//*[@id="board"]/div[3]/sui-select-option[2]/span[2]

//*[@id="medium"]
//*[@id="medium"]/div[2]/sui-select-option[2]/span[2]

//*[@id="gradeLevel"]
//*[@id="gradeLevel"]/div[2]/sui-select-option[3]/span[2]

//*[@id="subject"]/div[1]
//*[@id="subject"]/div[2]/sui-select-option[4]/span[2]

//*[@id="districts"]
//*[@id="districts"]/div[2]/sui-select-option[28]/span[2]

/html/body/sui-modal/sui-dimmer/div/div/div/div[3]/button


search = browser.find_element_by_xpath('//*[@id="keyword"]')
name.send_keys("NYK")
/html/body/app-root/div/app-header/div/div[2]/div/app-search/button



/html/body/app-root/div/ng-component/div[2]/div/div[2]/div/div[1]/app-card/div/div[1]/div[1]/div[2]

//*[@id="batchcardList"]/div/div/div/div/button
//*[@id="enrollToCourse"]
wait 20 seconds
//*[@id="mcq-question-container"]/div[2]/div[3]/div/div/div[1]/div[2]
/html/body/div[10]/div/div/custom-next-navigation/div/a/img


firstname = browser.find_element_by_xpath('//*[@id="ans-field1"]')
firstname.send_keys("Varun Singh")

firstname = browser.find_element_by_xpath('//*[@id="ans-field2"]')
firstname.send_keys("Varun Singh")

firstname = browser.find_element_by_xpath('//*[@id="ans-field3"]')
firstname.send_keys("Varun Singh")

firstname = browser.find_element_by_xpath('//*[@id="ans-field4"]')
firstname.send_keys("Varun Singh")

firstname = browser.find_element_by_xpath('//*[@id="ans-field5"]')
firstname.send_keys("Varun Singh")

/html/body/div[10]/div/div/custom-next-navigation/div/a/img

//*[@id="mcq-question-container"]/div[2]/div[3]/div/div/div[2]/div[2]/span/p
/html/body/div[10]/div/div/custom-next-navigation/div/a/img


age = browser.find_element_by_xpath('//*[@id="ans-field1"]')
age.send_keys("Varun Singh")
city = browser.find_element_by_xpath('//*[@id="ans-field2"]')
city.send_keys("Mandla")
state = browser.find_element_by_xpath('//*[@id="ans-field3"]')
state.send_keys("Madhya Pradesh")
/html/body/div[10]/div/div/custom-next-navigation/div/a/img

//*[@id="assess-summary"]/div/div/div[3]/button[2]
/html/body/sui-modal/sui-dimmer/div/div/div/div[2]/div/sui-rating/i[5]
/html/body/sui-modal/sui-dimmer/div/div/div/div[3]/button


# time.sleep(10)
# browser.quit()
