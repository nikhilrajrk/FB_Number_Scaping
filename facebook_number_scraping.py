import requests
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from getpass import getpass

user_name = input('Enter Your Phone_Number [or] Email : ')
wordlist = getpass('Enter Your Password : ')

notify_disable = webdriver.FirefoxProfile()
notify_disable.set_preference("dom.webnotifications.enabled", False)

browser = webdriver.Firefox(firefox_profile=notify_disable,executable_path = 'C:\\geckodriver.exe')

#url = 'https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110'
url = 'https://www.facebook.com/'

browser.get(url)

email = browser.find_element_by_id('email')
email.send_keys(user_name)

#Password_Field
password = browser.find_element_by_id('pass')
password.send_keys(wordlist)

#Login Facebook
login = browser.find_element_by_id('loginbutton')
login.submit()

time.sleep(3)

curr_url = browser.current_url

if 'login_attempt' in str(curr_url):
    browser.close()
    print('Please Check Your UserName [or] Password!')
    exit()

time.sleep(2)

browser.get('https://www.facebook.com/profile.php?id=100033127044384&lst=100033127044384%3A100033127044384%3A1559287970&sk=friends&source_ref=pb_friends_tl')

time.sleep(3)

html = browser.execute_script("return document.documentElement.outerHTML")

soup = BeautifulSoup(html, 'lxml')
#'id':'pagelet_timeline_app_collection_100033127044384:2356318349:2'
div1 = soup.find_all('div',{'class':'fsl fwb fcb'})

#friends_url = []

for i in div1:
    a_tag = i.find('a').get('href')
    browser.get(a_tag)

    html = browser.execute_script("return document.documentElement.outerHTML")

    soup = BeautifulSoup(html, 'lxml')

    about_url = soup.find('a',{"data-tab-key":"about"}).get('href').replace('&amp;','')
    #print(about_url)
    friend_name = soup.find('a',{"class":"_2nlw _2nlv"})

    browser.get(about_url)

    html = browser.execute_script("return document.documentElement.outerHTML")
    
    soup = BeautifulSoup(html, 'lxml')

    phone_number = soup.find('span',{'dir':'ltr'})
    
    if phone_number != None:
        print(f'>>> {friend_name.text} : {phone_number.text}')

    else:
        print(f'>>> {friend_name.text} : phone number not there')
        continue

browser.close()
