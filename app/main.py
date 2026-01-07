from fastapi import FastAPI
from app.core.database import engine, Base
from app.routers import (
    author_router,
    book_router,
    user_router,
    auth_router,
    loan_router,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Libreria",
    description="API para gestionar una libreria",
    version="0.0.1",
)


app.include_router(author_router.router)
app.include_router(book_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(loan_router.router)


@app.get("/")
def read_root():
    return {"message": "API arriba"}
