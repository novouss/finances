import aiosqlite
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from ..database import get_db
from .get_transaction import get_by_id

router = APIRouter(prefix="/transactions", tags=["transactions"])


class TransactionCreate(BaseModel):
    date: str
    from_account: str | None
    to_account: str | None
    amount: float = Field(..., ge=0)
    description: str | None = None


async def create(db: aiosqlite.Connection, scheme: TransactionCreate) -> dict:
    query = "INSERT INTO transactions (date, from_account, to_account, amount, description) VALUES (?, ?, ?, ?, ?)"
    await db.execute(
        query,
        (
            scheme.date,
            scheme.from_account,
            scheme.to_account,
            scheme.amount,
            scheme.description,
        ),
    )
    await db.commit()
    async with db.execute("SELECT last_insert_rowid()") as cur:
        row = await cur.fetchone()
        return await get_by_id(db, row[0])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    data: TransactionCreate, db: aiosqlite.Connection = Depends(get_db)
) -> dict:
    """Creates a new transaction"""
    return await create(db, data)
