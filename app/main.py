from fastapi import FastAPI
from sqlalchemy.orm import Session

from .database import engine, Base

from .routers import library, book, member, librarian, transaction

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(library.router)
app.include_router(book.router)
app.include_router(member.router)
app.include_router(librarian.router)
app.include_router(transaction.router)
