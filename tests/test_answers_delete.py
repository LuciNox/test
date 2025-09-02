from fastapi.testclient import TestClient
from app.models.question import QuestionsTable
from app.models.answer import AnswersTable
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

### TESTS CORRECT

def test_delete_answer_cascade(session: Session, client: TestClient):
    question = QuestionsTable(id=1000, text="test")
    answer = AnswersTable(question_id=question.id, text="test answer", user_id="test")
    session.add(question)
    session.add(answer)
    session.commit()

    res = client.delete(f"/questions/{question.id}")

    assert res.status_code == 200

    answer_db = client.get(f"/answers/{answer.id}")

    assert answer_db.status_code == 404

def test_delete_answer(session: Session, client: TestClient):
    question = QuestionsTable(id=1000, text="test")
    answer = AnswersTable(question_id=question.id, text="test answer", user_id="test")
    session.add(question)
    session.add(answer)
    session.commit()

    res = client.delete(f"/answers/{answer.id}")

    assert res.status_code == 200

    question_db = client.get(f"/questions/{question.id}")
    answer_db = client.get(f"/answers/{answer.id}")

    assert question_db.status_code == 200
    assert answer_db.status_code == 404


### TESTS INCORRECT

def test_delete_anwer_404(client: TestClient):
    res = client.delete(f"/answers/{1}")

    assert res.status_code == 404

def test_delete_anwer_404(session: Session):
    try:
        question = QuestionsTable(id=1000, text="test")
        answer = AnswersTable(question_id=1, text="test answer", user_id="test")
        session.add(question)
        session.add(answer)
        session.commit()
    except IntegrityError:
        pass