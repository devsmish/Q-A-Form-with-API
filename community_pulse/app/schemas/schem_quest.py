from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=12)
    category_id: int # Теперь это поле обязательно


class QuestionResponse(BaseModel):
    id: int
    text: str
    # ВАЖНО: имя поля должно совпадать с relationship в модели
    # Если в модели 'categories', то и тут 'categories'
    category: Optional[CategoryBase] = Field(None, alias="categories")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class MessageResponse(BaseModel):
    message: str
