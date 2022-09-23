import json

from .BaseSaver import BaseSaver
from ..models import item


class JsonBaseSaver(BaseSaver):
    file_path: str = "data.json"

    def __init__(self, **kwargs):
        self.file_path = kwargs['file_path']
        super().__init__()

    def save(self, data: list[item.Item]) -> bool:
        try:
            with open(self.file_path, "a+", encoding="UTF-8") as json_file:
                json.dump(data, json_file, indent=2, separators=(', ', ': '), ensure_ascii=False)
                return True
        except Exception as e:
            print(e)
            return False