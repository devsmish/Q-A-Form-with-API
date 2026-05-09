import os

# Поднимаемся на один уровень выше (в корень Community_Pulse)
# .parent для корректного выхода из папки community_pulse
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Config:
    DEBUG = False
    TESTING = False
    # Теперь путь будет точно указывать на внешнюю папку instance
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'example.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
