from sqlalchemy import Column, String, ForeignKey, DECIMAL, Integer

from src.parser.models.base import BaseModel


class Item(BaseModel):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    price = Column(DECIMAL, nullable=False)
    old_price = Column(DECIMAL, nullable=True, default=None)
    category_name = Column(String(255), ForeignKey('categories.name', ondelete='CASCADE'), nullable=False)
    link_product = Column(String(255), nullable=False)
    card_image = Column(String(255), nullable=False)

    def __repr__(self):
        return f"Item(title={self.title}, price={self.price}, old_price={self.old_price}, category_name={self.category_name}, link_product={self.link_product}, card_image={self.card_image})"
