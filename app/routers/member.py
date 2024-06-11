from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Book as SQLAlchemyBook
from app.schemas import Book as PydanticBook
from app.database import get_db

router = APIRouter()


@router.post("/borrow")
async def borrow_book(book: PydanticBook, db: Session = Depends(get_db)):
    db_book = (
        db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book.book_id).first()
    )
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if not db_book.is_available:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    db_book.is_available = False
    db.commit()
    db.refresh(db_book)
    return {"message": f"The book '{db_book.title}' has been borrowed."}


@router.post("/return")
async def return_book(book: PydanticBook, db: Session = Depends(get_db)):
    db_book = (
        db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book.book_id).first()
    )
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db_book.is_available = True
    db.commit()
    db.refresh(db_book)
    return {"message": f"The book '{db_book.title}' has been returned."}
