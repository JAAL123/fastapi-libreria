from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import book_crud
from app.schema import book_schema
from app.dependecies import get_db, get_current_user
from typing import Optional
from fastapi import Path

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.get("/", response_model=list[book_schema.BookResponse])
def get_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    year: Optional[int] = None,
):
    return book_crud.get_books(db=db, skip=skip, limit=limit, year=year)


@router.get("/{book_id}", response_model=book_schema.BookResponse)
def get_book(db: Session = Depends(get_db), book_id: int = Path(..., ge=1)):
    db_book = book_crud.get_book(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return db_book


@router.post("/", response_model=book_schema.BookResponse)
def create_book(
    book: book_schema.BookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return book_crud.create_book(db=db, book=book)


@router.patch(
    "/{book_id}/borrow",
    response_model=book_schema.BookResponse,
)
def borrow_book(
    book_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_book = book_crud.get_book(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    if db_book.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book already borrowed"
        )

    db_book.owner_id = user_id

    return book_crud.borrow_book(db=db, book_id=book_id, user_id=user_id)


@router.patch("/{book_id}/return", response_model=book_schema.BookResponse)
def return_book(
    book_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    db_book = book_crud.return_book(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    if db_book.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book not borrowed by you"
        )

    db_book.owner_id = None

    return book_crud.return_book(db=db, book_id=book_id)
