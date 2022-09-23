import datetime

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session, sessionmaker

from src.parser.models import category
from src.parser.models.item import Item
from src.parser.savers.BaseSaver import BaseSaver


class SQLBaseSaver(BaseSaver):
    connection: Connection

    def __init__(self, **kwargs):
        engine = create_engine(
            f"postgresql://{kwargs['user']}:{kwargs['password']}@{kwargs['host']}:{kwargs['port']}/{kwargs['database']}",
            echo=True,
            pool_pre_ping=True
        )
        session_factory = sessionmaker(bind=engine)
        self.session = session_factory()
        print("Connected successfully...", " ", sep='\n')
        super().__init__()

    def save_headers(self, headers: list[category.Category]) -> list[category.Category]:
        if self.session.query(category.Category).count() == 0 or len(headers) == 0:
            self.session.add_all(headers)
            self.session.commit()
        return headers

    def save(self, data: list[Item]) -> bool:
        if self.session.query(Item).count() == 0 or len(data) == 0:
            self.session.add_all(data)
            self.session.commit()
        return True

    def last_check(self) -> datetime.datetime:
        return self.session.query(Item).order_by(Item.created_at.desc()).first().created_at
