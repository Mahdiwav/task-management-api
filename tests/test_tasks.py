


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["is_completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_task_invalid_title(client):
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_list_tasks(client):
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_list_tasks_with_pagination(client):
    for i in range(25):
        client.post("/tasks", json={"title": f"Task {i}"})

    response = client.get("/tasks?skip=5&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10


def test_list_tasks_with_filter(client):
    client.post("/tasks", json={"title": "Complete Task", "is_completed": True})
    client.post("/tasks", json={"title": "Incomplete Task", "is_completed": False})

    response = client.get("/tasks?is_completed=true")
    assert response.status_code == 200
    data = response.json()
    assert all(t["is_completed"] for t in data)


def test_get_task(client):
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_get_nonexistent_task(client):
    response = client.get("/tasks/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(client):
    create_response = client.post("/tasks", json={"title": "Old Title"})
    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "New Title", "is_completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["is_completed"] is True


def test_delete_task(client):
    create_response = client.post("/tasks", json={"title": "To Delete"})
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}