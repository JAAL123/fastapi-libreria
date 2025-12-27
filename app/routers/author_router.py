from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import author_crud
from app.schema import author_schema
from app.dependecies import get_db

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


@router.post("/", response_model=author_schema.AuthorResponse)
def create_author(author: author_schema.AuthorCreate, db: Session = Depends(get_db)):
    return author_crud.create_author(db=db, author=author)


@router.get("/", response_model=list[author_schema.AuthorResponse])
def get_authors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return author_crud.get_authors(db=db, skip=skip, limit=limit)
