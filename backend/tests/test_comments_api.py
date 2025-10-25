# tests/test_comments_api.py
import json
import pytest
from backend.main import app, db, Task, Comment

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    # ensure CORS not interfering
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def create_task(client, title="Demo Task"):
    rv = client.post("/tasks", json={"title": title})
    assert rv.status_code == 201
    data = rv.get_json()
    return data["id"]


def test_add_and_list_and_get_comment(client):
    task_id = create_task(client)
    # add comment
    rv = client.post(f"/tasks/{task_id}/comments", json={"author": "Alice", "body": "First comment"})
    assert rv.status_code == 201
    c = rv.get_json()
    assert c["author"] == "Alice"
    assert c["body"] == "First comment"
    comment_id = c["id"]

    # list
    rv = client.get(f"/tasks/{task_id}/comments")
    assert rv.status_code == 200
    comments = rv.get_json()
    assert isinstance(comments, list)
    assert len(comments) == 1
    assert comments[0]["id"] == comment_id

    # get single
    rv = client.get(f"/comments/{comment_id}")
    assert rv.status_code == 200
    single = rv.get_json()
    assert single["author"] == "Alice"


def test_update_comment(client):
    task_id = create_task(client)
    rv = client.post(f"/tasks/{task_id}/comments", json={"author": "Bob", "body": "Hello"})
    cid = rv.get_json()["id"]

    # update body
    rv = client.put(f"/comments/{cid}", json={"body": "Updated"})
    assert rv.status_code == 200
    new = rv.get_json()
    assert new["body"] == "Updated"

    # update author empty -> fail
    rv = client.put(f"/comments/{cid}", json={"author": ""})
    assert rv.status_code == 400


def test_delete_comment(client):
    task_id = create_task(client)
    rv = client.post(f"/tasks/{task_id}/comments", json={"author": "Eve", "body": "To delete"})
    cid = rv.get_json()["id"]

    rv = client.delete(f"/comments/{cid}")
    assert rv.status_code == 200
    # now 404
    rv = client.get(f"/comments/{cid}")
    assert rv.status_code == 404


def test_validation_errors(client):
    task_id = create_task(client)
    # missing author
    rv = client.post(f"/tasks/{task_id}/comments", json={"body": "no author"})
    assert rv.status_code == 400
    # missing body
    rv = client.post(f"/tasks/{task_id}/comments", json={"author": "X"})
    assert rv.status_code == 400

    # non existing task
    rv = client.post("/tasks/9999/comments", json={"author": "A", "body": "b"})
    assert rv.status_code == 404
