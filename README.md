# Инструкция

Данный проект является тестовым заданием. 

Использованные инструменты: Fastapi, Sqlalchemy, Alembic, Pytest, SQLModel, Postgresql, Docker

## Модели:
### Question – вопрос:
id: int

text: str (текст вопроса)

created_at: datetime


### Answer – ответ на вопрос:
id: int

question_id: int (ссылка на Question)

user_id: str (идентификатор пользователя, например uuid)

text: str (текст ответа)

created_at: datetime


### Методы API:

#### Вопросы (Questions):
GET /questions/ — список всех вопросов

POST /questions/ — создать новый вопрос

GET /questions/{id} — получить вопрос и все ответы на него

DELETE /questions/{id} — удалить вопрос (вместе с ответами)


#### Ответы (Answers):
POST /questions/{id}/answers/ — добавить ответ к вопросу

GET /answers/{id} — получить конкретный ответ

DELETE /answers/{id} — удалить ответ


## Логика:
- Нельзя создать ответ к несуществующему вопросу.
- Один и тот же пользователь может оставлять несколько ответов на один вопрос.
- При удалении вопроса должны удаляться все его ответы (каскадно).


## Поднятие окружения и запуск приложения

1. Из корневой папки проекта выполнить:
> python -m virtualenv venv

ИЛИ
> python -m venv venv

2. Активировать виртуальное окружение

> .venv/Scripts/activate

3.  Установить зависимости

> pip install -r requirements.txt

4. Поднять контейнер с базой

> docker pull postgres

> cd app

> docker compose up -d

5. накатить миграции

> alembic upgrade head

6. Запустить приложение

> fastapi dev main.py

По адресу http://127.0.0.1:8000/docs#/ можно проверить работу

## Запуск тестов

Из корневой павки проекта запустить

> python -m pytest tests/
