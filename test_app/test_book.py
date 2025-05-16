from fastapi.testclient import TestClient
from main import app
from schemas.book import BookCreate

client = TestClient(app)


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    data = response.json()
    assert data["message"] == "Book added successfully"
    assert data["data"]["title"] == "Johny bravo"


def test_get_book_by_id():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 200
    assert get_book_data['id'] == book_id


def test_get_book_by_id_not_found():
    book_id = 1
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 404
    assert get_book_data['detail'] == "book not found."


def test_update_book():
  # Create a book
  payload = {
      "title": "Old Title",
      "author": "Author A",
      "year": 2020,
      "pages": 300,
      "language": "English"
  }
  response = client.post("/books", json=payload)
  book_id = response.json()["data"]["id"]

  # Update the book
  update_payload = {
      "title": "New Title",
      "pages": 350
  }
  update_response = client.put(f"/books/{book_id}", json=update_payload)
  assert update_response.status_code == 200
  assert update_response.json()["data"]["title"] == "New Title"
  assert update_response.json()["data"]["pages"] == 350


def test_delete_book():
  # Create a book
  payload = {
      "title": "Delete Me",
      "author": "Author B",
      "year": 2021,
      "pages": 250,
      "language": "French"
  }
  response = client.post("/books", json=payload)
  book_id = response.json()["data"]["id"]

  # Delete the book
  delete_response = client.delete(f"/books/{book_id}")
  assert delete_response.status_code == 200
  assert delete_response.json()["message"] == "Book deleted successfully"

  # Confirm it's deleted
  get_response = client.get(f"/books/{book_id}")
  assert get_response.status_code == 404
