from selenium import webdriver
import time
import pickle
from movielist import script_list
import requests

# print(script_list)
driver = webdriver.Chrome()

for i in range(len(script_list)):
    path = "https://imsdb.com/scripts/{}.html".format(script_list[i])
    req = requests.get(path)
    if req.status_code == requests.codes['ok']:
        print(script_list[i])
        driver.get(path)
        path1 = "/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr/td/pre"
        dos = open("scripts.txt", "a")
        time.sleep(1)
        try:
            dos.write(driver.find_element_by_xpath(path1).text)
            print(script_list[i], "completed")
        except UnicodeEncodeError:
            pass
