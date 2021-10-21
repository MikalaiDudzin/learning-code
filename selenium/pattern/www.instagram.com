from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
from fake_useragent import UserAgent
from instagram import username, password
import pickle

url = 'https://www.instagram.com/'

useragent = UserAgent()

# options
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={useragent.opera}')
# headless mode
# options.add_argument("--headless")
# options.headless = True

driver = webdriver.Chrome(executable_path='D:\проекты\pythonProject\chromedriver.exe', options=options)

try:
    driver.get(url=url)
    sleep(2)
#
#     username_imput = driver.find_element_by_name('username')
#     username_imput.clear()
#     username_imput.send_keys(username)
#     sleep(2)
#
#     password_imput = driver.find_element_by_name('password')
#     password_imput.clear()
#     password_imput.send_keys(password)
#     sleep(2)
#
#     password_imput.send_keys(Keys.ENTER)
#
#     sleep(5)
#
#     # клик по кнопке
#     # login_button = driver.find_element_by_class_name('dfgt').click()
#
# #     cookies
#     pickle.dump(driver.get_cookies(), open(f'{username}_cookies', 'wb'))
#     sleep(10)

    for cookie in pickle.load(open(f'{username}_cookies', 'rb')):
        driver.add_cookie(cookie)

    driver.refresh()
    sleep(5)
    login_button = driver.find_element_by_class_name('HoLwm').click()


except Exception  as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
