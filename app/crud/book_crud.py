from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Optional
from datetime import datetime
from app.models.book_model import Book
from app.models.loan_model import Loan
from app.schema import book_schema
from app.core.config import settings


async def create_book(db: AsyncSession, book: book_schema.BookCreate):

    db_book = Book(**book.model_dump())

    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    query = select(Book).options(selectinload(Book.author)).where(Book.id == db_book.id)
    result = await db.execute(query)
    return result.scalar_one()


async def get_books(
    db: AsyncSession, skip: int = 0, limit: int = 100, year: Optional[int] = None
):
    query = select(Book).options(selectinload(Book.author))

    if year:
        query = query.where(Book.year == year)

    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


async def get_book(db: AsyncSession, book_id: int):
    query = select(Book).options(selectinload(Book.author)).where(Book.id == book_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def borrow_book(db: AsyncSession, book_id: int, user_id: int):

    query_book = select(Book).where(Book.id == book_id)
    result_book = await db.execute(query_book)
    db_book = result_book.scalar_one_or_none()

    if not db_book:
        return "BOOK_NOT_FOUND"

    if db_book.available_copies < 1:
        return "NO_STOCK"

    query_loan = select(Loan).where(
        Loan.user_id == user_id, Loan.book_id == book_id, Loan.return_date.is_(None)
    )
    result_loan = await db.execute(query_loan)
    existing_loan = result_loan.scalar_one_or_none()

    if existing_loan:
        return "BOOK_ALREADY_BORROWED"

    query_count = (
        select(func.count())
        .select_from(Loan)
        .where(Loan.user_id == user_id, Loan.return_date.is_(None))
    )
    result_count = await db.execute(query_count)
    active_loans_count = result_count.scalar() or 0

    if active_loans_count >= settings.MAX_LOANS_PER_USER_ALLOWED:
        return "MAX_LOANS_REACHED"

    db_book.available_copies -= 1
    db_loan = Loan(book_id=book_id, user_id=user_id, loan_date=datetime.now())

    db.add(db_loan)
    db.add(db_book)

    await db.commit()
    await db.refresh(db_loan)
    return db_loan


async def return_book(db: AsyncSession, book_id: int, user_id: int):

    query_loan = select(Loan).where(
        Loan.book_id == book_id, Loan.user_id == user_id, Loan.return_date.is_(None)
    )
    result_loan = await db.execute(query_loan)
    loan = result_loan.scalar_one_or_none()

    query_book = select(Book).where(Book.id == book_id)
    result_book = await db.execute(query_book)
    db_book = result_book.scalar_one_or_none()

    if not db_book:
        return "BOOK_NOT_FOUND"

    if not loan:
        return "LOAN_NOT_FOUND"

    loan.return_date = datetime.now()
    db_book.available_copies += 1

    db.add(loan)
    db.add(db_book)

    await db.commit()
    await db.refresh(loan)
    return loan


async def add_book_stock(db: AsyncSession, book_id: int, quantity: int):
    db_book = await get_book(db, book_id)

    if not db_book:
        return None

    db_book.available_copies += quantity
    db_book.total_copies += quantity

    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book
