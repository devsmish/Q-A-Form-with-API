from flask import Flask
from pydantic import ValidationError

from community_pulse.app.routers.questions import questions_bp
from community_pulse.app.routers.responses import responses_bp
from community_pulse.app.routers.categories import categories_bp
from community_pulse.config import DevelopmentConfig
from community_pulse.app.extensions import db, migrate
from community_pulse.app.utils.response import PydanticResponse


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.response_class = PydanticResponse

    app.register_blueprint(questions_bp, url_prefix='/questions')
    app.register_blueprint(responses_bp, url_prefix='/responses')
    app.register_blueprint(categories_bp, url_prefix='/categories')

    db.init_app(app)

    import community_pulse.app.models

    migrate.init_app(app, db)

    # Глобальный обработчик ошибок валидации DTO
    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(e: ValidationError):
        return {
            "error": "Validation Error",
            "details": e.errors(include_url=False, include_context=False)
        }, 400

    return app
