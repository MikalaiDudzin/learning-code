from bs4 import BeautifulSoup
import lxml
import random
import csv
import requests
from fake_useragent import UserAgent
import datetime

user = UserAgent().random
headers = {'user-agent': user}

def get_data():

    cur_data = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f'labirint_{cur_data}.csv', 'w') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название книги",
                "Автор",
                "Издательство",
                "Цена со скидкой",
                "Цена без скидки",
                "Процент скидки",
                "Наличие кешбека",
                "Наличие на складе"
            )
        )

    url = 'https://www.labirint.ru/novelty/?display=table&period=14'
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')


    pages_count = int(soup.find('div', class_='pagination-number').find_all('a')[-1].text)

    books_data = []

    for page in range(1, pages_count + 1):

        url = f'https://www.labirint.ru/novelty/?display=table&period=14&page={page}'

        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')

        books_items = soup.find('tbody', class_='products-table__body').find_all('tr')

        for book in books_items:
            book_data = book.find_all('td')

            try:
                book_title = book_data[0].find('a').text.strip()
            except:
                book_title = 'Нет названия'

            try:
                book_author = book_data[1].text.strip()
            except:
                book_author = 'Нет автора'

            try:
                book_publishing = book_data[2].find_all('a')
                book_publishing = ':'.join(book.text for book in book_publishing)
            except:
                book_publishing = 'Нет издательства'

            try:
                book_new_price = int(book_data[3].find('div', 'price').find('span').find('span').text.strip().replace(" ", ""))
            except:
                book_new_price = 'Нет новой цены'

            try:
                book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
            except:
                book_old_price = 'Нет старого прайса'

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
            except:
                book_sale = 'Нет скидки'

            try:
                book_cashback = book_data[3].find('span', class_='product-cashback').find('a').get_text()
            except:
                book_cashback = 'Нет кешбека'

            try:
                book_status = book_data[-1].text.strip()
            except:
                book_status = "Нет статуса"

            # print(book_status )

            books_data.append(
                {
                    'book_title': book_title,
                    'book_author': book_author,
                    'book_publishing':book_publishing,
                    'book_new_price':book_new_price,
                    'book_old_price':book_old_price,
                    'book_sale': book_sale,
                    'book_cashback': book_cashback,
                    'book_status': book_status
                }
            )

            with open(f'labirint_{cur_data}.csv', 'a') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_title,
                        book_author,
                        book_publishing,
                        book_new_price,
                        book_old_price,
                        book_sale,
                        book_cashback,
                        book_status
                    )
                )

        print(f'обработанна {page} из {pages_count} страниц')

def main():
    get_data()

if __name__ == '__main__':
    main()