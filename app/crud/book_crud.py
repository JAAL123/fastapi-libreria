from sqlalchemy.orm import Session
from app.models.book_model import Book
from app.models.loan_model import Loan
from typing import Optional
from app.schema import book_schema
from datetime import datetime


def create_book(db: Session, book: book_schema.BookCreate):
    db_book = Book(title=book.title, author_id=book.author_id, year=book.year)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100, year: Optional[int] = None):

    query = db.query(Book)

    if year:
        query = query.filter(Book.year == year)

    return query.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def borrow_book(db: Session, book_id: int, user_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        return None

    if db_book.available_copies < 1:
        return "NO_STOCK"

    db_book.available_copies -= 1

    db_loan = Loan(book_id=book_id, user_id=user_id)
    db.add(db_book)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def return_book(db: Session, book_id: int, user_id: int):
    loan = (
        db.query(Loan)
        .filter(
            Loan.book_id == book_id, Loan.user_id == user_id, Loan.return_date == None
        )
        .first()
    )

    if not loan:
        return "LOAN_NOT_FOUND"
    # actualizar la fecha de devolucion para marcarlo como devuelto
    loan.return_date = datetime.utcnow()

    # actualizar el stock del libro
    db_book = db.query(Book).filter(Book.id == book_id).first()
    db_book.available_copies += 1

    db.add(loan)
    db.add(db_book)
    db.commit()
    db.refresh(loan)
    return loan


def add_book_stock(db: Session, book_id: int, quantity: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        return None

    db_book.available_copies += quantity
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
