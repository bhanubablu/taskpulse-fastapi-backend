import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    user_payload = {
        "full_name": "Task Tester",
        "email": "tasktester@example.com",
        "password": "SecretPassword123"
    }
    client.post("/api/v1/auth/register", json=user_payload)
    login_res = client.post("/api/v1/auth/login", data={"username": user_payload["email"], "password": user_payload["password"]})
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_task_crud_lifecycle(auth_headers):
    # 1. Create Task
    task_payload = {
        "title": "Set up CI/CD with GitHub Actions",
        "description": "Configure automated testing on push",
        "priority": "high",
        "status": "pending"
    }
    res = client.post("/api/v1/tasks/", json=task_payload, headers=auth_headers)
    assert res.status_code == 201
    task = res.json()
    assert task["title"] == task_payload["title"]
    task_id = task["id"]

    # 2. List Tasks
    list_res = client.get("/api/v1/tasks/", headers=auth_headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # 3. Update Task Status
    update_res = client.put(f"/api/v1/tasks/{task_id}", json={"status": "completed"}, headers=auth_headers)
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "completed"

    # 4. Check Analytics
    analytics_res = client.get("/api/v1/tasks/analytics/summary", headers=auth_headers)
    assert analytics_res.status_code == 200
    analytics = analytics_res.json()
    assert analytics["total_tasks"] >= 1
    assert analytics["completed_tasks"] >= 1

    # 5. Delete Task
    del_res = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert del_res.status_code == 204
