from fastapi.testclient import TestClient
from sqlmodel import Session

### TESTS CORRECT

def test_post_question(client: TestClient):
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