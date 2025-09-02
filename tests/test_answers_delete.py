from fastapi.testclient import TestClient
from app import main
from app.database import get_session
from app.models.question import QuestionsTable
from app.models.answer import AnswersTable
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import NullPool
from sqlalchemy.exc import IntegrityError

import pytest

### FIXTURES

@pytest.fixture(name="session")
def test_session():
    DATABASE_URL = "postgresql://postgres:1@localhost:5432/test"

    engine = create_engine(DATABASE_URL, poolclass=NullPool)
    SQLModel.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            yield session
    finally:
        SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    main.app.dependency_overrides[get_session] = get_session_override
    client = TestClient(main.app)
    yield client
    main.app.dependency_overrides.clear()

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

def test_delete_anwer_404(session: Session, client: TestClient):
    try:
        question = QuestionsTable(id=1000, text="test")
        answer = AnswersTable(question_id=1, text="test answer", user_id="test")
        session.add(question)
        session.add(answer)
        session.commit()
    except IntegrityError:
        pass