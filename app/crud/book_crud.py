from sqlalchemy.orm import Session
from app.models.book_model import Book
from app.schema import book_schema


def create_book(db: Session, book: book_schema.BookCreate):
    db_book = Book(title=book.title, author_id=book.author_id, year=book.year)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()


def borrow_book(db: Session, book_id: int, user_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        return None

    db_book.owner_id = user_id

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def return_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        return None

    db_book.owner_id = None

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
