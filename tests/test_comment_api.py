import pytest
from flask import Flask
from src.apps.backend.server import app  # import your Flask app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_comment(client):
    response = client.post(
        "/api/tasks/1/comments",
        data=json.dumps({"content": "Test comment", "author": "Tester"}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["content"] == "Test comment"

def test_list_comments(client):
    # Add one first
    client.post(
        "/api/tasks/1/comments",
        data=json.dumps({"content": "Another comment"}),
        content_type='application/json'
    )
    response = client.get("/api/tasks/1/comments")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0

def test_update_comment(client):
    # Add comment
    res = client.post(
        "/api/tasks/1/comments",
        data=json.dumps({"content": "Old"}),
        content_type='application/json'
    )
    comment_id = res.get_json()["id"]

    # Update it
    response = client.patch(
        f"/api/comments/{comment_id}",
        data=json.dumps({"content": "Updated"}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["content"] == "Updated"

def test_delete_comment(client):
    res = client.post(
        "/api/tasks/1/comments",
        data=json.dumps({"content": "To delete"}),
        content_type='application/json'
    )
    comment_id = res.get_json()["id"]

    response = client.delete(f"/api/comments/{comment_id}")
    assert response.status_code == 204
