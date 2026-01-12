from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    year = Column(Integer)
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)
    cover_url = Column(String, nullable=True)

    # relaciones
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    loans = relationship("Loan", back_populates="book")

    author = relationship("Author", back_populates="books")
