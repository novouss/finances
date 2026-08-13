import aiosqlite
from fastapi import APIRouter, Depends, HTTPException, status

from ..database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])


async def get_by_id(db: aiosqlite.Connection, id: int) -> dict | None:
    query = "SELECT * FROM transactions WHERE id = ?"
    async with db.execute(query, (id,)) as cur:
        row = await cur.fetchone()
        return dict(row) if row else None


@router.get("/{id}")
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
