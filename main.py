from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from notifications import makeNotification
import configure
import time
from misc import makeAssignment
import makefiles

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

browser.quit()

makefiles.makeData(newAssignments)