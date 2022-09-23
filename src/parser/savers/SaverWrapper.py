from src.parser.savers.CSVSaver import CSVBaseSaver
from src.parser.savers.JSONSaver import JsonBaseSaver
from src.parser.savers.SQLSaver import SQLBaseSaver
from typing import Optional
from src.parser.models import item, category
from src.parser.savers.BaseSaver import BaseSaver


class SaverWrapper:
    saver: BaseSaver = None

    def __init__(self, saver: dict):
        self.set_saver(**saver)

    def set_saver(self, **saver):
        match saver['name']:
            case "csv":
                self.saver = CSVBaseSaver(file_path=saver['file_path'])
            case "json":
                self.saver = JsonBaseSaver(file_path=saver['file_path'])
            case "sql":
                self.saver = SQLBaseSaver(**saver['args'])
            case _:
                raise ValueError("Unknown saver")

    def save(self, data: list[item.Item]) -> bool:
        return self.saver.save(data)

    def last_check(self):
        return self.saver.last_check()

    def save_headers(self, param) -> Optional[list[category.Category]]:
        return self.saver.save_headers(param)
