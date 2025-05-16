from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_users():
  response = client.get("/users")
  assert response.status_code == 200
  assert isinstance(response.json(), dict)


def test_add_user():
  payload = {
      "username": "queenlatifah",
      "email": "latifah@example.com",
      "full_name": "Queen Latifah"
  }
  response = client.post("/users", json=payload)
  data = response.json()
  assert response.status_code == 200
  assert data["message"] == "User added successfully"
  assert data["data"]["username"] == "queenlatifah"


def test_get_user_by_id():
  payload = {
      "username": "beyonce",
      "email": "beyonce@example.com",
      "full_name": "Beyoncé Knowles"
  }
  response = client.post("/users", json=payload)
  user_id = response.json()["data"]["id"]

  get_response = client.get(f"/users/{user_id}")
  assert get_response.status_code == 200
  assert get_response.json()["id"] == user_id


def test_get_user_by_id_not_found():
  response = client.get("/users/non-existent-id")
  assert response.status_code == 404
  assert response.json()["detail"] == "user not found."


def test_update_user():
  payload = {
      "username": "testuser",
      "email": "test@example.com",
      "full_name": "Test User"
  }
  response = client.post("/users", json=payload)
  user_id = response.json()["data"]["id"]

  update_payload = {
      "full_name": "Updated User"
  }
  update_response = client.put(f"/users/{user_id}", json=update_payload)
  assert update_response.status_code == 200
  assert update_response.json()["data"]["full_name"] == "Updated User"


def test_delete_user():
  payload = {
      "username": "deleteuser",
      "email": "delete@example.com",
      "full_name": "Delete Me"
  }
  response = client.post("/users", json=payload)
  user_id = response.json()["data"]["id"]

  delete_response = client.delete(f"/users/{user_id}")
  assert delete_response.status_code == 200
  assert delete_response.json()["message"] == "User deleted successfully"

  # Confirm deletion
  get_response = client.get(f"/users/{user_id}")
  assert get_response.status_code == 404

