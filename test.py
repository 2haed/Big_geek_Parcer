import requests
from bs4 import BeautifulSoup
import json


URL = 'https://biggeek.ru/catalog/apple'
HOST = 'https://biggeek.ru/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/102.0.5005.167 YaBrowser/22.7.4.957 Yowser/2.5 Safari/537.36 '
}
html = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(html.content, 'html.parser')
items = soup.find_all('div', class_='catalog-card')
cards = []
for item in items:
    cards.append(
        {
            'title': item.find('a', class_='catalog-card__title cart-modal-title').get_text(strip=True),
            'price': item.find('b', class_='cart-modal-count').get_text(strip=True).replace("₽", ""),
            'old-price': item.find('span', class_='old-price').get_text(strip=True),
            'link-product': HOST + item.find('a', class_='catalog-card__title cart-modal-title').get('href'),
            'card_image': HOST + item.find('a', class_='catalog-card__img').find('img').get('src')
            }
        )

category_dropdown_link = soup.find_all('a', class_='category-dropdown-header__sub-link')
for i in range(len(category_dropdown_link)):
    if category_dropdown_link[i].text == 'Apple iPad':
        print(i+1, ". ", category_dropdown_link[i].text, sep='')