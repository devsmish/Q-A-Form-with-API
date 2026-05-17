from flask import Response, jsonify
from pydantic import BaseModel


class PydanticResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        """Этот метод автоматически срабатывает во Flask, если роут
        возвращает тип данных, который Flask изначально не поддерживает."""
        # 1. Если роут вернул одну Pydantic модель
        if isinstance(response, BaseModel):
            return jsonify(response.model_dump())

        # 2. Если роут вернул список Pydantic моделей
        if isinstance(response, list) and all(isinstance(item, BaseModel) for item in response):
            return jsonify([item.model_dump() for item in response])

        # Во всех остальных случаях (строки, обычные словари) отдаем стандартному Flask
        return super().get_response(response, environ)