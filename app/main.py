from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlmodel import Session
from sqlalchemy import select

from app.database import get_session
from app.models.question import *
from app.models.answer import *

app = FastAPI()

### QUESTIONS
# GET
@app.get("/questions/", response_model=List[QuestionsTable])
async def get_questions(*, session: Session = Depends(get_session)):
    questions = session.exec(select(QuestionsTable)).scalars().all()
    
    if not questions:
        raise HTTPException(status_code=404, detail="Вопросов не найдено.")
    
    return questions

@app.get("/questions/{id}", response_model=QuestionsTable)
async def get_question_by_id(*, session: Session = Depends(get_session), id: int):
    question = session.get(QuestionsTable, id)

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден.")
    
    return question

# POST
@app.post("/questions/", response_model=QuestionsTable)
async def post_question(*, session: Session = Depends(get_session), question: Question):
    new_question = QuestionsTable.model_validate(question)
    session.add(new_question)
    session.commit()
    session.refresh(new_question)

    return new_question

# DELETE
@app.delete("/questions/{id}")
async def delete_question(*, session: Session = Depends(get_session), id: int):
    question = session.get(QuestionsTable, id)

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден.")
    
    session.delete(question)
    session.commit()

    return {"message": "Удаление успешно"}


### ANSWERS
# GET
@app.get("/answers/{id}")
async def get_answer(*, session: Session = Depends(get_session), id: int):
    answer = session.get(AnswersTable, id)

    if not answer:
        raise HTTPException(status_code=404, detail="Ответ не найден.")
    
    return answer

#POST
@app.post("/questions/{id}/answers/", response_model=AnswersTable)
async def post_answer(*, session: Session = Depends(get_session), id: int, answer: str, user_id: str):
    question_obj = session.get(QuestionsTable, id)

    if not question_obj:
        raise HTTPException(status_code=403, detail="Нельзя добавить ответ к несуществующему вопросу!")
    
    new_answer = AnswersTable.model_validate({"text": answer, "question_id": id, "user_id": user_id})
    session.add(new_answer)
    session.commit()
    session.refresh(new_answer)

    return new_answer

# DELETE
@app.delete("/answers/{id}")
async def delete_answer(*, session: Session = Depends(get_session), id: int):
    answer = session.get(AnswersTable, id)

    if not answer:
        raise HTTPException(status_code=404, detail="Ответ не найден.")
    
    session.delete(answer)
    session.commit()

    return {"message": "Удаление успешно"}

# Методы API:
# Вопросы (Questions):
# GET /questions/ — список всех вопросов
# POST /questions/ — создать новый вопрос
# GET /questions/{id} — получить вопрос и все ответы на него
# DELETE /questions/{id} — удалить вопрос (вместе с ответами)


# Ответы (Answers):
# POST /questions/{id}/answers/ — добавить ответ к вопросу
# GET /answers/{id} — получить конкретный ответ
# DELETE /answers/{id} — удалить ответ
