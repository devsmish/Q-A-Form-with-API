from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from community_pulse.app.services.category_service import CategoryService
from community_pulse.app.schemas.question_schema import CategoryBase, CategoryCreate

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['POST'])
def create_category():
    try:
        data = CategoryCreate.model_validate(request.get_json())
        new_cat = CategoryService.create_category(data)
        return jsonify(CategoryBase.model_validate(new_cat).model_dump()), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400

@categories_bp.route('/', methods=['GET'])
def get_categories():
    categories = CategoryService.get_all_categories()
    return jsonify([CategoryBase.model_validate(c).model_dump() for c in categories]), 200

@categories_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = CategoryService.get_category_by_id(id)
    if not category:
        return jsonify({'message': "Категория с таким ID не найдена"}), 404
    return jsonify(CategoryBase.model_validate(category).model_dump()), 200

@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    category = CategoryService.update_category(id, request.get_json())
    if not category:
        return jsonify({"message": "Категория не найдена"}), 404
    return jsonify(CategoryBase.model_validate(category).model_dump()), 200

@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    if not CategoryService.delete_category(id):
        return jsonify({"message": "Категория не найдена"}), 404
    return jsonify({"message": "Категория удалена"}), 204
