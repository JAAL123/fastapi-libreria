from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import book_crud
from app.schema import book_schema
from app.dependecies import get_db

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.post("/", response_model=book_schema.BookResponse)
def create_book(book: book_schema.BookCreate, db: Session = Depends(get_db)):
    return book_crud.create_book(db=db, book=book)


@router.get("/", response_model=list[book_schema.BookResponse])
def get_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return book_crud.get_books(db=db, skip=skip, limit=limit)
