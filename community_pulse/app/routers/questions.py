from flask import Blueprint, request
from community_pulse.app.services.question_service import QuestionService
from community_pulse.app.schemas.question_schema import QuestionCreate, QuestionResponse

questions_bp = Blueprint('questions', __name__)


@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = QuestionService.get_all_questions()
    # Flask понимает, что это список Pydantic-моделей, и превращает его в JSON-массив
    return [QuestionResponse.model_validate(q) for q in questions], 200


@questions_bp.route('/', methods=['POST'])
def create_question():
    question_dto = QuestionCreate.model_validate(request.get_json())

    question = QuestionService.create_question(question_dto)
    if not question:
        return {"message": "Указанная категория не существует"}, 400

    # Чистый Pydantic-объект
    return QuestionResponse.model_validate(question), 201


@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    question = QuestionService.get_question_by_id(id)
    if not question:
        return {'message': "Вопрос с таким ID не найден"}, 404

    return QuestionResponse.model_validate(question), 200


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    question = QuestionService.update_question(id, request.get_json())
    if not question:
        return {'message': "Вопрос не найден или указанная категория не существует"}, 400

    return QuestionResponse.model_validate(question), 200


@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    if not QuestionService.delete_question(id):
        return {'message': "Вопрос с таким ID не найден"}, 404

    return "", 204
