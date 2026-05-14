from flask import Blueprint, jsonify, request
from community_pulse.app.models import db
from community_pulse.app.models.mod_quest import Category
from community_pulse.app.schemas.schem_quest import CategoryBase, CategoryCreate
from pydantic import ValidationError


categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['POST'])
def create_category():
    """Создание новой категории."""

    try:
        data = CategoryCreate.model_validate(request.get_json())
        new_cat = Category(name=data.name)
        db.session.add(new_cat)
        db.session.commit()
        return jsonify(CategoryBase.model_validate(new_cat).model_dump()), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400

@categories_bp.route('/', methods=['GET'])
def get_categories():
    """Получение списка всех категорий."""

    categories = db.session.query(Category).all()
    return jsonify([CategoryBase.model_validate(c).model_dump() for c in categories]), 200


@categories_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    """Получение информации о категории по её ID."""

    category = db.session.get(Category, id)

    if category is None:
        return jsonify({'message': "Категория с таким ID не найдена"}), 404

    return jsonify(CategoryBase.model_validate(category).model_dump()), 200


@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    """Обновление категории по её ID."""

    category = db.session.get(Category, id)
    if not category:
        return jsonify({"message": "Категория не найдена"}), 404

    data = request.get_json()
    category.name = data.get('name', category.name)
    db.session.commit()
    return jsonify(CategoryBase.model_validate(category).model_dump()), 200


@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    """Удаление категории по её ID."""

    category = db.session.get(Category, id)
    if not category:
        return jsonify({"message": "Категория не найдена"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Категория удалена"}), 200
