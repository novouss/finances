import aiosqlite
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..database import get_db

router = APIRouter(prefix="/transactions/id", tags=["transactions"])


class TransactionResponse(BaseModel):
    id: int
    date: str
    created_at: str
    modified_at: str
    from_account: str | None
    to_account: str | None
    amount: float
    description: str | None

    model_config = {"from_attributes": True}


async def get_by_id(db: aiosqlite.Connection, id: int) -> dict | None:
    query = "SELECT * FROM transactions WHERE id = ?"
    async with db.execute(query, (id,)) as cur:
        row = await cur.fetchone()
        return dict(row) if row else None


@router.get("/{id}", response_model=TransactionResponse)
async def get_transaction(
    id: int,
    db: aiosqlite.Connection = Depends(get_db),
) -> dict:
    """Retrieves a transaction by its ID"""
    result = await get_by_id(db, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction ID {id}, could not be found",
        )
    return result
