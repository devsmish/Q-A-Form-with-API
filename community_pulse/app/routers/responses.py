from flask import Blueprint, jsonify, request
from community_pulse.app.services.response_service import ResponseService
from community_pulse.app.services.question_service import QuestionService
from community_pulse.app.schemas.response_schema import ResponseCreate

responses_bp = Blueprint('response', __name__)


@responses_bp.route('/', methods=['GET'])
def get_responses():
    """Получение динамической статистики по всем вопросам."""
    questions = QuestionService.get_all_questions()
    results = []

    for q in questions:
        stats = QuestionService.get_question_statistics(q.id)
        if stats:
            results.append(stats)

    return jsonify(results), 200


@responses_bp.route('/', methods=['POST'])
def add_response():
    # Валидация входного DTO ответа
    schema_data = ResponseCreate.model_validate(request.get_json())

    response = ResponseService.add_response(schema_data)
    if not response:
        return jsonify({'message': "Вопрос не найден"}), 404

    return jsonify({'message': f"Ответ на вопрос {schema_data.question_id} добавлен"}), 201
