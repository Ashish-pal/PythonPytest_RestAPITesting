import requests
import uuid

baseURL_API = "https://todo.pixegami.io"


def test_call_baseURL_API():
    response = requests.get(baseURL_API)
    assert response.status_code == 200


def test_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()

    task_id = data["task"]["task_id"]
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]


def test_can_update_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "my updated content",
        "is_done": True,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]


def test_task_papa_payload():
    pass


def test_can_list_users():
    n = 3
    payload = new_task_payload()
    for _ in range(3):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    user_id = payload["user_id"]
    list_task_response = list_task(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()

    tasks = data["tasks"]
    assert len(tasks) == n


def test_can_delete_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def create_task(payload):
    return requests.put(baseURL_API + "/create-task", json=payload)


def update_task(payload):
    return requests.put(baseURL_API + "/update-task", json=payload)


def get_task(task_id):
    return requests.get(baseURL_API + f"/get-task/{task_id}")


def list_task(user_id):
    return requests.get(baseURL_API + f"/list-tasks/{user_id}")


def delete_task(task_id):
    return requests.delete(baseURL_API + f"/delete-task/{task_id}")


def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False,
    }
