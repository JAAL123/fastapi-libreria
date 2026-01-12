from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import book_crud
from app.schema import book_schema, loan_schema
from app.dependecies import get_db, get_current_user, get_current_admin
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
):
    return book_crud.create_book(db=db, book=book)


@router.patch(
    "/{book_id}/borrow",
    response_model=loan_schema.Loan,
)
def borrow_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = book_crud.borrow_book(db=db, book_id=book_id, user_id=current_user.id)

    if result == "BOOK_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    if result == "NO_STOCK":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No stock available"
        )

    if result == "BOOK_ALREADY_BORROWED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book already borrowed"
        )

    if result == "MAX_LOANS_REACHED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User has reached max loans"
        )

    return result


@router.patch("/{book_id}/return", response_model=loan_schema.Loan)
def return_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = book_crud.return_book(db=db, book_id=book_id, user_id=current_user.id)

    if result == "BOOK_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    if result == "LOAN_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Loan not found"
        )

    return result


@router.patch("/{book_id}/stock", response_model=book_schema.BookResponse)
def add_book_stock(
    book_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    add_book_stock = book_crud.add_book_stock(db=db, book_id=book_id, quantity=quantity)

    if not add_book_stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return add_book_stock
