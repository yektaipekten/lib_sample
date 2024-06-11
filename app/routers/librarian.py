from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Book as SQLAlchemyBook, Member as SQLAlchemyMember
from app.schemas import Book as PydanticBook, Member as PydanticMember
from app.database import get_db

router = APIRouter()


@router.post("/books")  # Add book to lib
async def add_book(book: PydanticBook, db: Session = Depends(get_db)):
    db_book = SQLAlchemyBook(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {"message": f"The book '{db_book.title}' has been added."}


@router.post("/books")  # Remove book to lib
async def remove_book(book: PydanticBook, db: Session = Depends(get_db)):
    db_book = (
        db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book.book_id).first()
    )
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return {"message": f"The book '{db_book.title}' has been removed."}


@router.post("/issue")  # issue book
async def issue_book(
    book: PydanticBook, member: PydanticMember, db: Session = Depends(get_db)
):
    db_book = (
        db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book.book_id).first()
    )
    db_member = (
        db.query(SQLAlchemyMember)
        .filter(SQLAlchemyMember.member_id == member.member_id)
        .first()
    )

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    if not db_book.is_available:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    db_book.is_available = False

    db.commit()
    db.refresh(db_book)
    return {
        "message": f"The book '{db_book.title}' has been issued to {db_member.name}."
    }


@router.post("/return")
async def return_book(
    book: PydanticBook, member: PydanticMember, db: Session = Depends(get_db)
):
    db_book = (
        db.query(SQLAlchemyBook).filter(SQLAlchemyBook.book_id == book.book_id).first()
    )
    db_member = (
        db.query(SQLAlchemyMember)
        .filter(SQLAlchemyMember.member_id == member.member_id)
        .first()
    )

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    db_book.is_available = True

    db.commit()
    db.refresh(db_book)
    return {
        "message": f"The book '{db_book.title}' has been returned by {db_member.name}."
    }
