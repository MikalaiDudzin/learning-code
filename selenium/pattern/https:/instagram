from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from fake_useragent import UserAgent

url = 'https://www.instagram.com/'

useragent = UserAgent()

# options
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={useragent.opera}')


driver = webdriver.Chrome(executable_path='D:\проекты\pythonProject\chromedriver.exe', options=options)

try:
    driver.get(url=url)
    time.sleep(2)

    username_imput = driver.find_element_by_name('username')
    username_imput.clear()
    username_imput.send_keys('username')
    time.sleep(2)

    password_imput = driver.find_element_by_name('password')
    password_imput.clear()
    password_imput.send_keys('password')
    time.sleep(2)

    password_imput.send_keys(Keys.ENTER)

    time.sleep(5)

    # клик по кнопке
    # login_button = driver.find_element_by_class_name('dfgt').click()

except Exception  as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
