from typing import List
from community_pulse.app.extensions import db
from community_pulse.app.models.question import Category
from community_pulse.app.schemas.question_schema import CategoryCreate


class CategoryService:
    @staticmethod
    def get_all_categories() -> List[Category]:
        """Получить все категории из базы."""
        return db.session.query(Category).all()

    @staticmethod
    def get_category_by_id(category_id: int) -> Category:
        """Получить категорию по ID или вернуть None."""
        return db.session.get(Category, category_id)

    @staticmethod
    def create_category(schema_data: CategoryCreate) -> Category:
        """Создать категорию, используя валидированные Pydantic данные."""
        new_cat = Category(**schema_data.model_dump())
        db.session.add(new_cat)
        db.session.commit()
        return new_cat

    @staticmethod
    def update_category(category_id: int, json_data: dict) -> Category:
        """Обновить имя категории, если она существует."""
        category = db.session.get(Category, category_id)
        if not category:
            return None

        category.name = json_data.get('name', category.name)
        db.session.commit()
        return category

    @staticmethod
    def delete_category(category_id: int) -> bool:
        """Удалить категорию. Возвращает True в случае успеха."""
        category = db.session.get(Category, category_id)
        if not category:
            return False

        db.session.delete(category)
        db.session.commit()
        return True
