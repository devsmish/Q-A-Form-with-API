from flask import Blueprint, jsonify, request
from community_pulse.app.models import db, Question
from sqlalchemy import select

questions_bp = Blueprint('questions', __name__)


@questions_bp.route('/', methods=['GET'])
def get_questions():
    """Получение списка всех вопросов."""
    print(request.args)
    print(request.form)
    print(request.data)
    # print(request.get_json())
    # print(request.json)
    print(request.files)
    print(request.method)
    print(request.headers)

    # questions = Question.query.all()

    questions = db.session.query(Question).all()

    # questions = db.session.execute(select(Question)).scalars().all()

    questions_data = [{'id': q.id, 'text': q.text} for q in questions]

    return jsonify(questions_data)


@questions_bp.route('/', methods=['POST'])
def create_question():
    """Создание нового вопроса."""
    data = request.get_json()

    if not data or not data.get('text'):
        return jsonify({'error': 'No question text provided'}), 400

    question = Question(text=data['text'])
    db.session.add(question)
    db.session.commit()
    return jsonify({'message': 'Вопрос создан', 'id': question.id}), 201


@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """Получение деталей конкретного вопроса по его ID."""

    question = db.session.query(Question).filter(Question.id == id).one_or_none()
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404

    return jsonify({'message': f"Вопрос: {question.text}"}), 200


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """Обновление конкретного вопроса по его ID."""

    question = db.session.query(Question).filter(Question.id == id).one_or_none()
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404

    data = request.get_json()

    if data and data.get('text'):
        question.text = data['text']
        db.session.commit()
        return jsonify({'message': f"Вопрос обновлен: {question.text}"}), 200

    return jsonify({'message': "Текст вопроса не предоставлен"}), 400


@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """Удаление конкретного вопроса по его ID."""
    question = db.session.query(Question).filter(Question.id == id).one_or_none()
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f"Вопрос с ID {id} удален"}), 200
