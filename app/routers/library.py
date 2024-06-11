from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas, database

router = APIRouter()


# Create a new library
@router.post("/library/", response_model=schemas.Library)
def create_library(
    library: schemas.LibraryCreate, db: Session = Depends(database.get_db)
):
    return crud.create_library(db=db, library=library)


# Read libraries with pagination
@router.get("/library/", response_model=List[schemas.Library])
def read_libraries(
    skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)
):
    return crud.get_libraries(db, skip=skip, limit=limit)


# Read a specific library by ID
@router.get("/library_id/{library_id}", response_model=schemas.Library)
def read_library(library_id: int, db: Session = Depends(database.get_db)):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return db_library


# Add a new book to the library
@router.post("/book/{library_id}/books/", response_model=schemas.Book)
def add_book(
    library_id: int, book: schemas.BookCreate, db: Session = Depends(database.get_db)
):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return crud.create_book(db=db, book=book, library_id=library_id)


# Remove a book from the library
@router.delete("/book/{library_id}/books/{book_id}")
def remove_book(library_id: int, book_id: int, db: Session = Depends(database.get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None or db_book.library_id != library_id:
        raise HTTPException(
            status_code=404, detail="Book not found in the specified library"
        )
    crud.delete_book(db=db, book_id=book_id)
    return {"message": "Book removed"}


# Register a new member
@router.post("/member/{library_id}/members/", response_model=schemas.Member)
def register_member(
    library_id: int,
    member: schemas.MemberCreate,
    db: Session = Depends(database.get_db),
):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return crud.create_member(db=db, member=member, library_id=library_id)


# Issue a book to a member
@router.post("/issue/{library_id}/issue/", response_model=schemas.Transaction)
def issue_book(
    library_id: int,
    book_id: int,
    member_id: int,
    db: Session = Depends(database.get_db),
):
    db_book = crud.get_book(db, book_id=book_id)
    db_member = crud.get_member(db, member_id=member_id)
    if db_book is None or db_member is None or db_book.library_id != library_id:
        raise HTTPException(
            status_code=404, detail="Book or member not found in the specified library"
        )
    return crud.issue_book(db=db, book_id=book_id, member_id=member_id)


# Return a book from a member
@router.post("/return/{library_id}/return/", response_model=schemas.Transaction)
def return_book(
    library_id: int,
    book_id: int,
    member_id: int,
    db: Session = Depends(database.get_db),
):
    db_book = crud.get_book(db, book_id=book_id)
    db_member = crud.get_member(db, member_id=member_id)
    if db_book is None or db_member is None or db_book.library_id != library_id:
        raise HTTPException(
            status_code=404, detail="Book or member not found in the specified library"
        )
    return crud.return_book(db=db, book_id=book_id, member_id=member_id)
