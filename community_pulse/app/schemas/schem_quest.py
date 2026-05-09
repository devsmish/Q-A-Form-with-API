from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2)


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=12)
    category_id: int


class QuestionResponse(BaseModel):
    id: int
    name: str
    category: Optional[CategoryBase] = None
    # class Config:
    #     # Указываем Pydantic использовать эти параметры чтобы можно было переносить данные прямо с объекта
    #     orm_mode = True
    #     from_attributes = True

    model_config = ConfigDict(
        from_attributes=True
    )


class MessageResponse(BaseModel):
    message: str
