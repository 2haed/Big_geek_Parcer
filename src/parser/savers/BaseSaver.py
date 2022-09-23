from abc import ABC, abstractmethod


from src.parser.models import item, category


class BaseSaver(ABC):
    @abstractmethod
    def save(self, data: list[item.Item]) -> bool:
        pass

    @abstractmethod
    def save_headers(self, param) -> list[category.Category]:
        pass

    @abstractmethod
    def last_check(self):
        pass

