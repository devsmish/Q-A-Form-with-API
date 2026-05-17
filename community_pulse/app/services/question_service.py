from typing import List, Optional, Dict, Any
from sqlalchemy import func
from community_pulse.app.extensions import db
from community_pulse.app.models.question import Question, Category
from community_pulse.app.models.response import Response
from community_pulse.app.schemas.question_schema import QuestionCreate

class QuestionService:
    @staticmethod
    def get_all_questions() -> List[Question]:
        """Получить все вопросы."""
        return db.session.query(Question).all()

    @staticmethod
    def get_question_by_id(question_id: int) -> Optional[Question]:
        """Найти вопрос по ID."""
        return db.session.get(Question, question_id)

    @staticmethod
    def create_question(schema_data: QuestionCreate) -> Optional[Question]:
        """Создать вопрос. Возвращает None, если указанной категории нет."""
        category = db.session.get(Category, schema_data.category_id)
        if not category:
            return None

        question = Question(
            text=schema_data.text,
            category_id=schema_data.category_id
        )
        db.session.add(question)
        db.session.commit()
        return question

    @staticmethod
    def update_question(question_id: int, json_data: dict) -> Optional[Question]:
        """Обновить текст вопроса или его категорию с проверкой существования категории."""
        question = db.session.get(Question, question_id)
        if not question:
            return None

        if 'text' in json_data:
            question.text = json_data['text']

        if 'category_id' in json_data:
            if not db.session.get(Category, json_data['category_id']):
                return None  # Сигнал роуту, что категория не существует (передадим 400)
            question.category_id = json_data['category_id']

        db.session.commit()
        return question

    @staticmethod
    def delete_question(question_id: int) -> bool:
        """Удалить вопрос по ID."""
        question = db.session.get(Question, question_id)
        if not question:
            return False
        db.session.delete(question)
        db.session.commit()
        return True

    @staticmethod
    def get_question_statistics(question_id: int) -> Optional[Dict[str, Any]]:
        """Динамически считает статистику ответов 'на лету' без таблицы системной статистики."""
        question = db.session.get(Question, question_id)
        if not question:
            return None

        stats = (
            db.session.query(Response.is_agree, func.count(Response.id))
            .filter(Response.question_id == question_id)
            .group_by(Response.is_agree)
            .all()
        )

        stats_dict = dict(stats)
        agree_count = stats_dict.get(True, 0)
        disagree_count = stats_dict.get(False, 0)

        return {
            "question_id": question_id,
            "agree_count": agree_count,
            "disagree_count": disagree_count
        }
