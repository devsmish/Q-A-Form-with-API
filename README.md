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

Testing Postman
1. Используйте Postman, чтобы отправить GET запрос на:
http://localhost:5000/questions
Ожидаемый результат: статус 200.

2. Используйте Postman со следующими данными:
● Метод: POST
● URL: http://localhost:5000/questions
● Body: raw: JSON
● Body: {"text": "Ваш новый вопрос"}
Ожидаемый результат: сообщение о создании вопроса с его ID.

3. 