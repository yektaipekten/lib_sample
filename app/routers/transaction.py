from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Transaction as SQLAlchemyTransaction
from app.schemas import Transaction as PydanticTransaction
from app.database import get_db

router = APIRouter()


@router.get("/transaction/{transaction_id}", response_model=PydanticTransaction)
async def get_transaction_details(transaction_id: int, db: Session = Depends(get_db)):
    transaction = (
        db.query(SQLAlchemyTransaction)
        .filter(SQLAlchemyTransaction.transaction_id == transaction_id)
        .first()
    )

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction
