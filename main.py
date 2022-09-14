import psycopg2
import requests
from bs4 import BeautifulSoup
import csv
import json
import pymysql
from config import host, user, password, db_name
from collections import namedtuple

UrlPath = namedtuple("URLPATH", ["path", "desc"])
SaverPath = namedtuple("SAVER", ["func", "desc"])
HOST = 'https://biggeek.ru/'
URL = 'https://biggeek.ru/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/102.0.5005.167 YaBrowser/22.7.4.957 Yowser/2.5 Safari/537.36 '
}
URLPATH = {
    '2': UrlPath("sale", "Акция Осенняя"),
    '3': UrlPath("catalog/apple-iphone", "Apple Iphone"),
    '4': UrlPath("catalog/planshety-apple-ipad", "Apple Ipad"),
    '5': UrlPath("catalog/apple-airpods", "Apple Airpods"),
    '6': UrlPath("catalog/aksessuary", "Аксессуары"),
    '7': UrlPath("catalog/dlya-doma", "Для Дома"),
}

URL_LOWER_PATHS = {
    '1': UrlPath("catalog/apple", "Apple"),
    '2': UrlPath("catalog/xiaomi", "Xiaomi"),
    '3': UrlPath("catalog/samsung", "Samsung"),
    '4': UrlPath("catalog/gadgeti", "Гаджеты"),
    '5': UrlPath("catalog/smartfony", "Смартфоны"),
    '6': UrlPath("catalog/aksessuary", "Аксессуары"),
    '7': UrlPath("catalog/akusticheskie-sistemi", "Акустические Системы"),
    '8': UrlPath("catalog/dlya-avto", "Для Авто"),
    '9': UrlPath("catalog/dlya-doma", "Для Дома"),
}

SAVER = {
    '1': SaverPath("save_sql", "SQL"),
    '2': SaverPath("save_json", "JSON"),
    '3': SaverPath("save_csv", "CSV")
}


def get_html(url, page=-1):
    if page != -1:
        url += "?page=" + str(page)
    r = requests.get(url, headers=HEADERS)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='catalog-card')
    cards = []
    for item in items:
        cards.append(
            {
                'title': item.find('a', class_='catalog-card__title cart-modal-title').get_text(strip=True),
                'price': item.find('b', class_='cart-modal-count').get_text(strip=True),
                'old-price': item.find('span', class_='old-price').get_text(strip=True),
                'link-product': HOST + item.find('a', class_='catalog-card__title cart-modal-title').get('href'),
                'card_image': HOST + item.find('a', class_='catalog-card__img').find('img').get('src')
            }
        )
    return cards

def save_csv(items, filepath):
    with open(filepath, 'a+', newline='', encoding="UTF-8") as file:
        writer = csv.writer(file, delimiter=';')
        for item in items:
            writer.writerow([item['title'], item['price'].replace('₽', ''), item['old-price'], item['link-product'],
                             item['card_image']])

def save_sql(items: list[dict[str, any]]):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        print("Connected successfully...", " ", sep='\n')
        with connection.cursor() as cursor:
            query_create_table = 'create table IF NOT EXISTS public.Goods (id serial primary key, title varchar(255) unique, price int, old_price int null, link_product varchar(255), img_link varchar(255))'
            cursor.execute(query_create_table)
        with connection.cursor() as cursor:
            insert_query = 'INSERT INTO public.Goods (title, price, old_price, link_product, img_link) VALUES '
            for item in items:
                insert_query += f'(\'{item["title"]}\', {item["price"].replace("₽", "").replace(" ", "")}, {item["old-price"].replace(" ", "") if item["old-price"] != "" else 0},  \'{item["link-product"]}\', \'{item["card_image"]}\'),\n'
            insert_query = insert_query[0: -2]
            cursor.execute(insert_query)
            connection.commit()
    except Exception as ex:
        if ex.args[0] == 1062:
            print("Goods are already in the database")
        else:
            print('Connection error...')
            print(ex)
    finally:
        connection.close()

def save_json(items, filepath):
    with open(filepath, 'a+', encoding="UTF-8") as json_file:
        json.dump(items, json_file, indent=2, separators=(', ', ': '), ensure_ascii=False)

def parser(path: str, saver):
    print(f"Parsed data from: {URL + path}")
    current_url = URL + path
    response = requests.get(current_url, HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    pages = soup.find_all('a', class_='prod-pagination__item')
    if (len(pages) > 0):
        max_page = pages[-1].text
        print(f'Всего страниц: {max_page}')
    else:
        print('Всего страниц: 1')
    page_amount = input('Укажите количество страниц для парсинга: ')
    if saver.upper() == "JSON":
        print('Введите путь файла с названием в конце')
        filepath = input() + '.json'
    elif saver.upper() == "CSV":
        print('Введите путь файла с названием в конце')
        filepath = input() + '.csv'
    page_amount = int(page_amount.strip())
    html = get_html(current_url)
    if html.status_code == 200:
        cards = []
        for page in range(0, page_amount):
            print(f'Парсим страницу: {page + 1}')
            html = get_html(current_url, page + 1)
            cards.extend(get_content(html.text))
            if saver.upper() == "SQL":
                save_sql(cards)
            elif saver.upper() == "JSON":
                save_json(cards, filepath)
            elif saver.upper() == "CSV":
                save_csv(cards, filepath)
            cards.clear()
    else:
        print('Error')

    print(' ', 'Парсер закончил работу', ' ', sep='\n')


while True:
    print("Categories:")
    response = requests.get(URL, HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    first = soup.find('button', class_='dropdown-header__button')
    others = soup.find_all('a', class_='nav-fixed-header__link')
    print(f"1. {(first.text.rstrip())}")
    for i in range(0, len(others)):
        print(i + 2, ". ", others[i].text, sep='')
    print("Введите значение или -1 для выхода:", " ", sep="\n")
    choice: str = input("What to parse?: ")
    if choice == "-1":
        print("Bye!")
        break
    if choice in URLPATH:
        for i in SAVER.values():
            print(i[1])
        saver: str = input("Where to parse?: ")
        parser(URLPATH[choice].path, saver)
    elif choice == "1":
        dropdown_header_link = soup.find_all('a', class_='category-dropdown-header__link')
        for i in range(len(dropdown_header_link) - 9):
            print(i + 1, ". ", dropdown_header_link[i].text, sep='')
        choice: str = input("What to parse?: ")
        for i in SAVER.values():
            print(i[1])
        saver: str = input("Where to parse?: ")
        parser(URL_LOWER_PATHS[choice].path, saver)
        continue
    else:
        print("Wrong choice")