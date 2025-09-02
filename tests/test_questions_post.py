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

def test_post_question(session: Session, client: TestClient):
    question = client.post("/questions/", json={"text": "test"})

    res = question.json()

    assert question.status_code == 200

    assert res["text"] == "test"
    assert res["id"] == 1


### TESTS INCORRECT

def test_post_question_empty(client: TestClient):
    try:
        client.post("/questions/", json={})
    except ValueError:
        pass

def test_post_question_invalid(client: TestClient):
    try:
        client.post("/questions/", json={"text": 1453.333})
    except ValueError: 
        pass