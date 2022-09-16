import psycopg2
import requests
from bs4 import BeautifulSoup
import csv
import json

import sqlcommands
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
    '1': UrlPath("catalog", "Каталог"),
    '2': UrlPath("sale", "Акция Осенняя"),
}

URL_LOWER_PATHS = {
    '1': UrlPath("apple-iphone", "Apple Iphone"),
    '2': UrlPath("planshety-apple-ipad", "Apple Ipad"),
    '3': UrlPath("apple-airpods", "Apple Airpods"),
    '4': UrlPath("aksessuary", "Аксессуары"),
    '5': UrlPath("dlya-doma", "Для Дома"),
    '6': UrlPath("apple", "Apple"),
    '7': UrlPath("xiaomi", "Xiaomi"),
    '8': UrlPath("samsung", "Samsung"),
    '9': UrlPath("gadgeti", "Гаджеты"),
    '10': UrlPath("smartfony", "Смартфоны"),
    '12': UrlPath("akusticheskie-sistemi", "Акустические Системы"),
    '13': UrlPath("dlya-avto", "Для Авто"),
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
            query_create_table = 'create table IF NOT EXISTS public.Goods (good_id serial primary key, title varchar(255) unique, price int, old_price int null, link_product varchar(255), img_link varchar(255))'
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


def parser(path: UrlPath, saver):
    print(f"Parsed data from: {URL + path.path}")
    current_url = URL + path.path
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


def main_():
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
        if choice in URL_LOWER_PATHS:
            for i in SAVER.values():
                print(i[1])
            saver: str = input("Where to parse?: ")
            print(URLPATH['1'] + "/" + URL_LOWER_PATHS[choice])
            parser(URLPATH['1'] + "/" + URL_LOWER_PATHS[choice], saver)
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


def main():
    with psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
    ) as connection:
        cursor = connection.cursor()
        args_str = f"(\'{URLPATH['1'].path}\', \'{URLPATH['1'].desc}\', NULL), (\'{URLPATH['2'].path}\', \'{URLPATH['2'].desc}\', NULL)"
        cursor.execute(sqlcommands.insert_categories + args_str)
        args_str = ",".join([f'(\'{category.path}\', \'{category.desc}\', 1)' for category in URL_LOWER_PATHS.values()])
        print(args_str)
        cursor.execute(sqlcommands.insert_categories + args_str)



if __name__ == '__main__':
    main_()
