from flask import Flask, jsonify
from pydantic import ValidationError

from community_pulse.app.routers.questions import questions_bp
from community_pulse.app.routers.responses import responses_bp
from community_pulse.app.routers.categories import categories_bp
from community_pulse.config import DevelopmentConfig
from community_pulse.app.extensions import db, migrate
import community_pulse.app.models


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.register_blueprint(questions_bp, url_prefix='/questions')
    app.register_blueprint(responses_bp, url_prefix='/responses')
    app.register_blueprint(categories_bp, url_prefix='/categories')

    db.init_app(app)
    migrate.init_app(app, db)

    # Глобальный обработчик ошибок валидации DTO
    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(e: ValidationError):
        return jsonify({
            "error": "Validation Error",
            "details": e.errors()  # Передает клиенту массив с точным описанием, где ошибка
        }), 400

    return app
