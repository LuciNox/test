from fastapi.testclient import TestClient
from app.models.question import QuestionsTable
from sqlmodel import Session

### TESTS CORRECT

def test_delete_question(session: Session, client: TestClient):
    question = QuestionsTable(id=1, text="test")
    session.add(question)
    session.commit()

    res = client.delete(f"/questions/{question.id}")

    assert res.status_code == 200

    question_db = client.get(f"/questions/{question.id}")

    assert question_db.status_code == 404