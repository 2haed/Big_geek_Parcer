from sqlalchemy import Column, String, Text, ForeignKey

from .base import BaseModel


class Category(BaseModel):
    __tablename__ = 'categories'

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    parent = Column(String(255), ForeignKey('categories.name', ondelete='CASCADE'), nullable=True, default=None)

    def __repr__(self):
        return f"Category(name={self.name}, description={self.description}, parent={self.parent})"
