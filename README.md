# Q-A-Form-with-API
Mini Flask-project "Community Pulse" (API Form Question - Answer)

● Создание миграции
flask --app community_pulse.app db init # Инициализирует миграции
flask --app community_pulse.app db migrate -m "Initial migration" # Создает файлы миграции
flask --app community_pulse.app db migrate -m "add Category"
● Применение миграции
flask --app community_pulse.app db upgrade # Применяет миграции к базе данных
● Откат миграции
flask db downgrade # Откатывает последнюю миграцию