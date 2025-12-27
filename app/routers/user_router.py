from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import user_crud
from app.schema import user_schema
from app.dependecies import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, user=user)
