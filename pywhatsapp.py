# By NAI
# 2022/06
# Send Message via Whatsapp
# To run this project you need install selenium , and mysql.connector

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import mysql.connector
from datetime import date
import sys
import os



# To display text arabic
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

#Save session user
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=/User_data')

# today = date.today()
#datanow = today.strftime("%Y-%m-%d")

phones = []
# msgs = []
success = 0
error = 0


connect = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="amani_sms"
)
mycursor = connect.cursor()


def send_message():
  mycursor.execute("SELECT phone, `msg` FROM phone_whats WHERE send_status = 0 AND deleted = 0")
  result = mycursor.fetchall()
  # for x in result:
  #   phones.append(x[0])
  #   msgs.append(str(x[1]))

  for value in result:
    phone = value[0]
    browser = webdriver.Chrome(executable_path='C:/chromedriver/chromedriver.exe',chrome_options=options)
    browser.get(f'https://web.whatsapp.com/send?phone=+964{phone}&text={value[1]}')
    sleep(5)
    try:
      # wait to loading all element page
      browser.implicitly_wait(35)
      button = browser.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')
      button.click()
      sleep(5)
      updaterow(phone)
      browser.close()
    except Exception as e:
      browser.close()


def updaterow(phone):
  sql =  """Update phone_whats set send_status = %s where phone = %s"""
  val = (1, phone)
  mycursor.execute(sql,val)
  connect.commit()

if __name__== "__main__":
  send_message()

  # print("المجموع الكلي للرسائل: ",len(phones))
  # print("\nتم الارسال: ",success)
  # print("\nلم يتم الارسال : ",error)



