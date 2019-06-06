from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from notifications import makeNotification
import configure
import time
from misc import makeAssignment
import makefiles
import os
import sys
import calendars

key = input("Please input Encryption Key - ")
try:
    config = configure.loadconfiguration(key.encode())
except:
    print("Wrong Key. Quitting in 3 Seconds.")
    time.sleep(3)
    quit()

makeNotification("Auto SMS", "Starting Automated SMS Procedure", icon="icon.ico")

browser = webdriver.Chrome()

browser.get("https://sms.eursc.eu/login.php")

usr_sms = config["SMS"]["usr"]
pwd_sms = config["SMS"]["pwd"]

browser.find_element_by_xpath('//*[@id="user_email"]').send_keys(usr_sms, Keys.TAB)
time.sleep(0.5)
browser.find_element_by_xpath('//*[@id="userNameInput"]').send_keys(usr_sms)
browser.find_element_by_xpath('//*[@id="passwordInput"]').send_keys(pwd_sms, Keys.ENTER)
browser.get('https://sms.eursc.eu/content/common/dashboard.php')

time.sleep(1)
i = 2
newAssignments = []
while True:
    try:
        time.sleep(0.1)
        browser.find_element_by_xpath('/html/body/div[2]/div/div/li[1]/div[2]/table/tbody[2]/tr[' + str(i) + ']/td[3]/a').click()
        time.sleep(0.2)
        a_subject = browser.find_element_by_xpath('//*[@id="assignment_container"]/table/tbody/tr[1]/td[2]').text
        a_desc_short = browser.find_element_by_xpath('//*[@id="assignment_container"]/table/tbody/tr[2]/td[2]').text
        a_type = browser.find_element_by_xpath('//*[@id="assignment_container"]/table/tbody/tr[3]/td[2]').text
        a_date = browser.find_element_by_xpath('//*[@id="assignment_container"]/table/tbody/tr[4]/td[2]').text
        a_desc_full = browser.find_element_by_xpath('//*[@id="assignment_container"]/table/tbody/tr[5]/td[2]').text
        browser.find_element_by_xpath('/html/body/div[4]/div[1]/a').click()
        newAssignments.append(makeAssignment(a_subject, a_desc_short, a_type, a_date, a_desc_full))
        i += 1
    except:
        break

if not os.path.exists("credentials.json") and config["GOOGLE"]["usr"] != "-":
    browser.get('https://developers.google.com/calendar/quickstart/python')
    browser.find_element_by_xpath('//*[@id="top_of_page"]/div[2]/div[2]/a[2]').click()
    browser.find_element_by_xpath('//*[@id="gc-wrapper"]/div[2]/article/article/div[2]/p[4]/a').click()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="identifierId"]').send_keys(config["GOOGLE"]["usr"], Keys.ENTER)
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(config["GOOGLE"]["pwd"], Keys.ENTER)
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="gc-wrapper"]/div[2]/article/article/div[2]/p[4]/a').click()
    browser.implicitly_wait(10)
    browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="devsite-dialog-onload-henhouse-0_widget_container"]/iframe'))
    browser.find_element_by_xpath('/html/body/hen-flow/hen-success-page/div[2]/div[2]/ng-container/div/a').click()

    time.sleep(1)
    os.system("move %userprofile%\\Downloads\\credentials.json " + os.getcwd())

browser.quit()

calendars.addToCalendars(config, newAssignments)

makefiles.makeData(newAssignments)