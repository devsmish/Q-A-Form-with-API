from flask import Flask
from pydantic import ValidationError

from community_pulse.app.routers.questions import questions_bp
from community_pulse.app.routers.responses import responses_bp
from community_pulse.app.routers.categories import categories_bp
from community_pulse.config import DevelopmentConfig
from community_pulse.app.extensions import db, migrate
# Импортируем провайдер и класс ответа
from community_pulse.app.utils.response import PydanticJSONProvider, pydantic_to_dict


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Настройка JSON-провайдера для стандартных вызовов
    app.json = PydanticJSONProvider(app)

    # Централизованный перехватчик: подготавливает любые Pydantic-данные для Flask
    base_make_response = app.make_response

    def smart_make_response(rv):
        if isinstance(rv, tuple) and len(rv) > 0:
            rv_list = list(rv)
            rv_list[0] = pydantic_to_dict(rv_list[0])
            rv = tuple(rv_list)
        else:
            rv = pydantic_to_dict(rv)
        return base_make_response(rv)

    app.make_response = smart_make_response

    # Регистрация блупринтов
    app.register_blueprint(questions_bp, url_prefix='/questions')
    app.register_blueprint(responses_bp, url_prefix='/responses')
    app.register_blueprint(categories_bp, url_prefix='/categories')

    db.init_app(app)

    import community_pulse.app.models
    migrate.init_app(app, db)

    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(e: ValidationError):
        return {
            "error": "Validation Error",
            "details": e.errors(include_url=False, include_context=False)
        }, 400

    return app
