from app.models import book_model, author_model


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
