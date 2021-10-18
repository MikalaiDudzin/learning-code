from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import lxml
import csv
import datetime
import time

cur_data = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
start_time = datetime.datetime.now()




with open(f'av_{cur_data}.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(
        (
            "Модель",
            "Год",
            "Характеристики",
            "Город",
            "Пробег",
            "Цена в руб.",
            "Цена в USD",
            "Ссылка",
        )
    )

cars_datas = []

page = 1
while True:
    user = UserAgent().random
    headers = {'user-agent': user}

    url = f'https://cars.av.by/filter?page={page}&sort=4'
    # print(url)
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    cars = soup.find('div', class_='listing__items').find_all('div', class_='listing-item')
    # print(cars[1])

    for car in cars:
        car_date = car.find(class_='listing-item__date').text

        if car_date == 'вчера':

            break


        else:
            try:
                car_model = car.find('span', class_='link-text').text.replace(",", " ")
            except:
                car_model = '-------'

            try:
                car_year = car.find(class_='listing-item__params').find_next().text[0:4]
            except:
                car_year = '-------'

            try:
                car_data = car.find(class_='listing-item__params').find_next().find_next().text
            except:

                car_data = '-------'
            try:
                car_сity = car.find(class_='listing-item__location').text
            except:
                car_сity = '-------'

            try:
                car_milage = car.find(class_='listing-item__params').find_next().find_next().find_next().text
            except:
                car_milage = '-------'

            try:
                car_price = car.find(class_='listing-item__price').text
            except:
                car_price = '-------'

            try:
                car_price_usd = car.find(class_='listing-item__priceusd').text
            except:
                car_price_usd = '-------'

            try:
                car_url = 'https://cars.av.by' + (car.find(class_='listing-item__link').get('href'))
            except:
                car_url = '-------'

            car_date = car.find(class_='listing-item__date').text
            # print(car_data)
            cars_datas.append(
                {
                    'car_model': car_model,
                    'car_year': car_year,
                    'car_data' : car_data,
                    'car_сity': car_сity,
                    'car_milage': car_milage,
                    'car_price': car_price,
                    'car_price_usd': car_price_usd,
                    'car_url': car_url,
                }
            )

            with open(f'av_{cur_data}.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        car_model,
                        car_year,
                        car_data,
                        car_сity,
                        car_milage,
                        car_price,
                        car_price_usd,
                        car_url
                    )
                )

            # time.sleep(10)
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    print(f'обработано  {page} страниц')
    #         print(car_data)
    # print(page)
    page += 1
print(f'Сбор данных завершен потрачено времени {cur_time} ')




