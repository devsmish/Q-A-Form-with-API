from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from community_pulse.app.extensions import db
from community_pulse.app.models import Response
from community_pulse.app.models.base import Model


class Category(Model):
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)

    questions: Mapped[List["Question"]] = relationship("Question", back_populates="category", lazy=True)

    def __repr__(self):
        return f'Category: {self.name}'


class Question(Model):
    text: Mapped[str] = mapped_column(db.String(255), nullable=False)

    responses: Mapped[List["Response"]] = relationship("Response", back_populates="question", lazy=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="questions")

    def __repr__(self):
        return f'Question: {self.text}'
