from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.crud import user_crud
from app.schema import user_schema
from app.dependecies import get_db
from app.services import email as email_service


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=user_schema.UserResponse)
def create_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks,
):
    db_user = user_crud.create_user(db=db, user=user)
    background_tasks.add_task(
        email_service.send_welcome_email,
        email_to=user.email,
        username=user.username,
    )

    return db_user
