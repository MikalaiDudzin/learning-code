from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import lxml
import random
import requests

user = UserAgent().random
header = {'user-agent': user}

fests_urls_list = []

for i in range(0, 96, 24):


    url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=September'
    req = requests.get(url=url, headers=header)
    json_data = json.loads(req.text)
    html_respnse = json_data['html']

    with open(f'data/index_{i}.html', 'w') as file:
        file.write(html_respnse)

    with open(f'data/index_{i}.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    cards = soup.find_all('a', class_='card-details-link')

    for item in cards:
        fests_url = 'https://www.skiddle.com' + item.get('href')
        fests_urls_list.append(fests_url)

count = 0
fest_list_result = []
for url in fests_urls_list:
    count += 1
    print(count)
    print(url)

    req = requests.get(url=url , headers=header)

    try:
        soup = BeautifulSoup(req.text, 'lxml')
        fest_info_blosk = soup.find('div', class_='top-info-cont')

        fest_name = fest_info_blosk.find('h1').text.strip()
        fest_data = fest_info_blosk.find('h3').text.strip()
        fest_location_url = 'https://www.skiddle.com' + fest_info_blosk.find('a', class_='tc-white').get('href')

        req = requests.get(url=fest_location_url, headers=header)
        soup = BeautifulSoup(req.text, 'lxml')

        contact_detailes = soup.find('h2', string='Venue contact details and info').find_next()
        item  = [item.text for item in contact_detailes.find_all('p')]

        contact_details_dict = {}
        for contact_detail in item:
            contact_detail_list = contact_detail.split(":")

            if len(contact_detail_list) == 3:
                contact_details_dict[contact_detail_list[0].strip()] = contact_detail_list[1].strip() + ":" \
                                                                       + contact_detail_list[2].strip()
            else:
                contact_details_dict[contact_detail_list[0].strip()] = contact_detail_list[1].strip()
        fest_list_result.append(
            {
                'Fest name': fest_name,
                'Fest data': fest_data,
                'Contacts data': contact_details_dict
            }
        )


    except Exception as ex:
        print(ex)
        print('damn ... there was some error ...')

with open('fest_list_result.json', 'a', encoding='utf-8') as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)

