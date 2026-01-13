from app.models import book_model, author_model
from app.models.user_model import User
from app.dependecies import get_current_admin
from app.main import app


def test_read_books_empty(client):
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_read_book(client, session):
    author = author_model.Author(name="Gabriel Garcia Marquez", biografy="Nobel")
    session.add(author)
    session.commit()

    book = book_model.Book(
        title="Cien años de soledad",
        year=1967,
        author_id=author.id,
        total_copies=10,
        available_copies=10,
    )
    session.add(book)
    session.commit()

    response = client.get("/books/")

    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Cien años de soledad"
    assert data[0]["year"] == 1967
    assert data[0]["author"]["name"] == "Gabriel Garcia Marquez"
    assert data[0]["total_copies"] == 10
    assert data[0]["available_copies"] == 10


def test_create_book_as_admin(client, session):
    author = author_model.Author(name="Antoine de Saint-Exupery", biografy="Aviador")
    session.add(author)
    session.commit()

    mock_admin = User(id=1, username="admin_test", role="admin")

    app.dependency_overrides[get_current_admin] = lambda: mock_admin

    payload = {
        "title": "El principito",
        "year": 1943,
        "author_id": author.id,
        "total_copies": 5,
        "available_copies": 5,
    }

    response = client.post("/books/", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "El principito"
    assert data["id"] is not None
