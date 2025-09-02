from fastapi.testclient import TestClient
from app import main
from app.database import get_session
from app.models.question import QuestionsTable
from app.models.answer import AnswersTable
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import NullPool

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

def test_get_answer(session: Session, client: TestClient):
    question = QuestionsTable(id=888, text="test1")
    answer_1 = AnswersTable(question_id=question.id, text="test answer", user_id="test")
    answer_2 = AnswersTable(question_id=question.id, text="test answer 1", user_id="test")
    session.add(question)
    session.add(answer_1)
    session.add(answer_2)
    session.commit()
    
    answer = client.get(f"/answers/{answer_1.id}")
    
    result = answer.json()

    assert answer.status_code == 200

    assert result["text"] == answer_1.text
    assert result["id"] == answer_1.id
    assert result["user_id"] == answer_1.user_id
    assert result["question_id"] == question.id


### TESTS INCORRECT

def test_get_answer_404(client: TestClient):
    questions = client.get(f"/answers/{1}")

    assert questions.status_code == 404

def test_get_answer_incorrect(session: Session, client: TestClient):
    question = QuestionsTable(id=888, text="test1")
    answer_1 = AnswersTable(question_id=question.id, text="test answer", user_id="test")
    answer_2 = AnswersTable(question_id=question.id, text="test answer 1", user_id="test")
    session.add(question)
    session.add(answer_1)
    session.add(answer_2)
    session.commit()
    
    answer = client.get("/answers/{answer.id}")  # несуществующий объект

    assert answer.status_code == 422