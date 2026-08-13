from datetime import UTC, datetime

import aiosqlite
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ..database import get_db
from .get_transaction import get_by_id

router = APIRouter(prefix="/transactions", tags=["transactions"])


class TransactionUpdate(BaseModel):
    date: str | None = None
    from_account: str | None = None
    to_account: str | None = None
    amount: float | None = Field(default=None, ge=0)
    description: str | None = None


async def update(
    db: aiosqlite.Connection, id: int, scheme: TransactionUpdate
) -> dict | None:
    exists = await get_by_id(db, id)
    if not exists:
        return None
    updates = scheme.model_dump(exclude_unset=True, exclude_none=True)
    if not updates:
        return exists
    updates["modified_at"] = datetime.now(UTC).replace(tzinfo=None)
    set_clause = ", ".join(f"{key} = ?" for key in updates)
    values = list(updates.values()) + [id]
    query = f"UPDATE transactions SET {set_clause} WHERE id = ?"
    await db.execute(query, values)
    await db.commit()
    return await get_by_id(db, id)


@router.patch("/{id}")
async def update_transaction(
    id: int, data: TransactionUpdate, db: aiosqlite.Connection = Depends(get_db)
):
    """Updates a transaction by its ID"""
    result = await update(db, id, data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction ID {id} could not be found nor updated.",
        )
    return result
