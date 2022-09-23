import csv
import datetime
import os.path
from pathlib import Path

from src.parser.models import item, category
from .BaseSaver import BaseSaver


class CSVBaseSaver(BaseSaver):
    def save_headers(self, param: list[category.Category]) -> list[category.Category]:
        try:
            with open(self.file_path, "w", encoding="UTF-8") as csv_file:
                csv.writer(csv_file).writerows(param)
                return param
        except Exception as e:
            print(e)
            return param

    def last_check(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(os.path.getmtime(self.file_path))

    file_path: str = "data.csv"
    categories_path: str = "categories.csv"

    def __init__(self, **kwargs):
        self.file_path = kwargs['file_path']
        self.file_path = kwargs['categories_path']
        super().__init__()

    def save(self, data: list[item.Item]) -> bool:
        try:
            with open(self.file_path, "a+", encoding="UTF-8") as csv_file:
                csv.writer(csv_file).writerows(data.__dict__)
                return True
        except Exception as e:
            print(e)
            return False
