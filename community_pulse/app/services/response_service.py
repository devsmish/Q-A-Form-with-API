from typing import Optional

from community_pulse.app.extensions import db
from community_pulse.app.models.question import Question
from community_pulse.app.models.response import Response
from community_pulse.app.schemas.response_schema import ResponseCreate

class ResponseService:
    @staticmethod
    def add_response(schema_data: ResponseCreate) -> Optional[Response]:
        """Добавить новый ответ на вопрос. Возвращает None, если вопрос не найден."""
        question = db.session.get(Question, schema_data.question_id)
        if not question:
            return None

        new_response = Response(
            question_id=schema_data.question_id,
            is_agree=schema_data.is_agree
        )
        db.session.add(new_response)
        db.session.commit()
        return new_response
