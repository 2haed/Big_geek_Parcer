# encoding: utf-8
from datetime import datetime, timedelta
from typing import Optional

from bs4 import BeautifulSoup
import requests

from src.parser.models.category import Category
from src.parser.models.item import Item

_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/102.0.5005.167 YaBrowser/22.7.4.957 Yowser/2.5 Safari/537.36 '
}


class Parser:
    last_check: datetime = None

    def __init__(self, last_check: datetime):
        self.last_check = last_check

    def parse_headers(self, url: str) -> Optional[list[Category]]:
        if datetime.now() - self.last_check > timedelta(days=1):
            request = requests.get(url, headers=_headers)
            if request.status_code != 200:
                raise Exception("Bad status code")

            soup = BeautifulSoup(request.text, 'html.parser')
            categories = [
                Category('catalog', 'Root category', "NULL"),
            ]
            for header in soup.find('ul', attrs={'class': ['dropdown-header__list', 'category-dropdown-header']}):
                s = BeautifulSoup(str(header), 'html.parser')
                found = s.find('a', {'class': 'category-dropdown-header__link'})
                if found is not None:
                    categories.append(Category(found['href'], found.text, 'catalog'))
            return categories
        else:
            return None

    def parse_category(self, url: str, category: str):
        request = requests.get(url, headers=_headers)
        if request.status_code != 200:
            raise Exception("Bad status code")

        soup = BeautifulSoup(request.text, 'html.parser')
        for card in soup.find_all('div', attrs={'class': 'catalog-card'}):
            s = BeautifulSoup(str(card), 'html.parser')
            title = s.find('a', attrs={'class': ['catalog-card__title', 'cart-modal-title']})
            ref, title = (title['href'], title.text) if title is not None else (None, None)
            price = s.find('span', attrs={'class': 'cart-modal-count'})
            price = price.text if price is not None and len(price) != 0 else "NULL"
            old_price = s.find('span', attrs={'class': 'old-price'})
            old_price = old_price.text if old_price is not None and len(old_price) != 0 else "NULL"
            yield Item(title=title, price=price.replace(" ", ""), old_price=old_price.replace(" ", ""),
                       category_name=category, link_product=ref, card_image=None)
