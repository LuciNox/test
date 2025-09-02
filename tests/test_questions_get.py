from fastapi.testclient import TestClient
from app import main
from app.database import get_session
from app.models.question import QuestionsTable
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

def test_get_questions(session: Session, client: TestClient):
    question_1 = QuestionsTable(id=888, text="test1")
    question_2 = QuestionsTable(id=999, text="test2")
    session.add(question_1)
    session.add(question_2)
    session.commit()
    
    questions = client.get("/questions/")
    
    result = questions.json()

    assert questions.status_code == 200

    assert len(result) == 2
    assert result[0]["text"] == question_1.text
    assert result[0]["id"] == question_1.id
    assert result[1]["text"] == question_2.text
    assert result[1]["id"] == question_2.id


def test_get_questions_by_id(session: Session, client: TestClient):
    question_1 = QuestionsTable(id=4221, text="test4221")
    session.add(question_1)
    session.commit()
    
    question = client.get(f"/questions/{question_1.id}")
    result = question.json()

    print(question)

    assert question.status_code == 200

    assert result["text"] == question_1.text
    assert result["id"] == question_1.id


### TESTS INCORRECT

def test_get_questions_empty(session: Session, client: TestClient):
    questions = client.get("/questions/")


    assert questions.status_code == 404

def test_get_questions_by_id_empty(session: Session, client: TestClient):
    question_1 = QuestionsTable(id=4221, text="test4221")
    session.add(question_1)
    session.commit()
    
    question = client.get("/questions/1")

    assert question.status_code == 404

def test_get_questions_by_id_incorrect(session: Session, client: TestClient):
    question_1 = QuestionsTable(id=4221, text="test4221")
    session.add(question_1)
    session.commit()
    
    question = client.get("/questions/{question.id}")  # несуществующий объект

    assert question.status_code == 422