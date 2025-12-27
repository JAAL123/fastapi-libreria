from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import book_crud
from app.schema import book_schema
from app.dependecies import get_db
from typing import Optional

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.post("/", response_model=book_schema.BookResponse)
def create_book(book: book_schema.BookCreate, db: Session = Depends(get_db)):
    return book_crud.create_book(db=db, book=book)


@router.get("/", response_model=list[book_schema.BookResponse])
def get_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    year: Optional[int] = None,
):
    return book_crud.get_books(db=db, skip=skip, limit=limit, year=year)


@router.patch("/{book_id}/borrow", response_model=book_schema.BookResponse)
def borrow_book(book_id: int, user_id: int, db: Session = Depends(get_db)):
    db_book = book_crud.borrow_book(db=db, book_id=book_id, user_id=user_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return db_book


@router.patch("/{book_id}/return", response_model=book_schema.BookResponse)
def return_book(book_id: int, db: Session = Depends(get_db)):
    db_book = book_crud.return_book(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return db_book
