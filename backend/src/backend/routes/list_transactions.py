import aiosqlite
from fastapi import APIRouter, Depends

from ..database import get_db
from .get_transaction import TransactionResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])

ALLOWED_SORT = ("date", "created_at", "modified_at")
ALLOWED_ORDER = ("ASC", "DESC")


async def get_list(
    db: aiosqlite.Connection,
    from_account: str | None = None,
    to_account: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    sort_by: str = "date",
    sort_order: str = "DESC",
    offset: int = 0,
    limit: int = 10,
) -> list[dict]:
    conditions = []
    params: list[str] = []

    if date_from:
        conditions.append("date >= ?")
        params.append(date_from)
    if date_to:
        conditions.append("date <= ?")
        params.append(date_to)
    if from_account:
        conditions.append("from_account LIKE ?")
        params.append(f"%{from_account}%")
    if to_account:
        conditions.append("to_account LIKE ?")
        params.append(f"%{to_account}%")

    where = " AND ".join(conditions)
    where = f"WHERE {where}" if where else where

    if sort_by not in ALLOWED_SORT:
        sort_by = "date"
    if sort_order not in ALLOWED_ORDER:
        sort_order = "DESC"
    query = f"""
        SELECT *
        FROM transactions
        {where}
        ORDER BY {sort_by} {sort_order}
        LIMIT ? OFFSET ?
    """
    final_params = params + [limit, offset]
    async with db.execute(query, final_params) as cur:
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


@router.get("", response_model=list[TransactionResponse])
async def list_transactions(
    from_account: str | None = None,
    to_account: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    sort_by: str = "date",
    sort_order: str = "DESC",
    offset: int = 0,
    limit: int = 10,
    db: aiosqlite.Connection = Depends(get_db),
):
    """Retrieves a list of transactions based on provided parameters"""
    return await get_list(
        db,
        from_account=from_account,
        to_account=to_account,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
    )
