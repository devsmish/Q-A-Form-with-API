from flask import Blueprint, request
from community_pulse.app.services.category_service import CategoryService
from community_pulse.app.schemas.question_schema import CategoryBase, CategoryCreate

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/', methods=['POST'])
def create_category():
    # Валидация входного DTO. Если JSON невалиден, Flask сразу вернет 400
    data = CategoryCreate.model_validate(request.get_json())

    new_cat = CategoryService.create_category(data)

    # Возвращаем Pydantic объект и статус-код. Flask сам создаст JSON!
    return CategoryBase.model_validate(new_cat), 201


@categories_bp.route('/', methods=['GET'])
def get_categories():
    categories = CategoryService.get_all_categories()

    # Чистый список Pydantic-объектов!
    return [CategoryBase.model_validate(c) for c in categories], 200


@categories_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = CategoryService.get_category_by_id(id)
    if not category:
        return {"message": "Категория с таким ID не найдена"}, 404

    return CategoryBase.model_validate(category), 200


@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    # Валидация входящих данных через DTO
    data = CategoryCreate.model_validate(request.get_json())

    category = CategoryService.update_category(id, data.model_dump())
    if not category:
        return {"message": "Категория не найдена"}, 404

    return CategoryBase.model_validate(category), 200


@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    if not CategoryService.delete_category(id):
        return {"message": "Категория не найдена"}, 404

    # Возвращаем обычный dict и статус 204 No Content
    return "", 204
