import json
import os
import uuid
from typing import Optional, List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    status,
    BackgroundTasks,
    Path,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import book_crud
from app.core.config import settings
from app.schema import book_schema, loan_schema
from app.dependecies import get_db, get_current_user, get_current_admin
from app.services import email as email_service
from app.core.redis_client import get_redis_client, delete_cache_pattern
import redis.asyncio as redis
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.get("/", response_model=List[book_schema.BookResponse])
async def get_books(
    db: AsyncSession = Depends(get_db),  # AsyncSession
    skip: int = 0,
    limit: int = 100,
    year: Optional[int] = None,
    cache: redis.Redis = Depends(get_redis_client),
):

    cache_key = f"book_list:{skip}:{limit}:{year}"

    cached_data = await cache.get(cache_key)
    if cached_data:
        print("CACHE HIT: Datos leidos desde redis")
        return json.loads(cached_data)

    print("CACHE MISS: Datos leidos desde la base de datos")

    books = await book_crud.get_books(db=db, skip=skip, limit=limit, year=year)

    books_pydantic = [book_schema.BookResponse.model_validate(book) for book in books]

    books_json = json.dumps(jsonable_encoder(books_pydantic))
    await cache.set(cache_key, books_json, ex=60)

    return books_pydantic


@router.get("/{book_id}", response_model=book_schema.BookResponse)
async def get_book(book_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)):

    db_book = await book_crud.get_book(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return db_book


@router.post("/", response_model=book_schema.BookResponse)
async def create_book(
    book: book_schema.BookCreate,
    db: AsyncSession = Depends(get_db),
    cache: redis.Redis = Depends(get_redis_client),
    current_user=Depends(get_current_admin),
):
    new_book = await book_crud.create_book(db=db, book=book)

    await delete_cache_pattern(cache, "book_list:*")

    return new_book


@router.patch("/{book_id}/borrow", response_model=loan_schema.MyLoanResponse)
async def borrow_book(
    book_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await book_crud.borrow_book(
        db=db, book_id=book_id, user_id=current_user.id
    )

    book = await book_crud.get_book(db=db, book_id=book_id)

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

    if book:
        background_tasks.add_task(
            email_service.send_loan_confirmation_email,
            email_to=current_user.email,
            username=current_user.username,
            book_title=book.title,
        )

    return result


@router.patch("/{book_id}/return", response_model=loan_schema.Loan)
async def return_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    result = await book_crud.return_book(
        db=db, book_id=book_id, user_id=current_user.id
    )

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
async def add_book_stock(
    book_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    updated_book = await book_crud.add_book_stock(
        db=db, book_id=book_id, quantity=quantity
    )

    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return updated_book


@router.post("/{book_id}/cover", response_model=book_schema.BookInfo)
async def upload_book_cover(
    book_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_admin),
):

    book = await book_crud.get_book(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{str(uuid.uuid4())}.{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    public_url = f"static/{unique_filename}"
    book.cover_url = public_url

    db.add(book)
    await db.commit()
    await db.refresh(book)

    return book
