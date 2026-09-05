import aiosqlite
from fastapi import APIRouter, Depends

from ..database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])


async def summary(
    db: aiosqlite.Connection,
    from_account: str,
    date_from: str | None = None,
    date_to: str | None = None,
) -> dict:
    conditions = []
    params: list[str] = []

    account_pattern = f"%{from_account}%"
    conditions.append("(to_account LIKE ? OR from_account LIKE ?)")
    params.extend([account_pattern] * 10)

    if date_from:
        conditions.append("date >= ?")
        params.append(date_from)
    if date_to:
        conditions.append("date <= ?")
        params.append(date_to)

    where = " AND ".join(conditions)
    where = f"WHERE {where}" if where else where

    query = f"""
        SELECT
            SUM(CASE WHEN to_account LIKE ? THEN amount ELSE 0 END) as sum_income,
            AVG(CASE WHEN to_account LIKE ? THEN amount ELSE 0 END) as avg_income,
            MIN(CASE WHEN to_account LIKE ? THEN amount ELSE 0 END) as min_income,
            MAX(CASE WHEN to_account LIKE ? THEN amount ELSE 0 END) as max_income,
            SUM(CASE WHEN from_account LIKE ? THEN amount ELSE 0 END) as sum_expense,
            AVG(CASE WHEN from_account LIKE ? THEN amount END) as avg_expense,
            MIN(CASE WHEN from_account LIKE ? THEN amount END) as min_expense,
            MAX(CASE WHEN from_account LIKE ? THEN amount END) as max_expense,
            MIN(date) as date_from, 
            MAX(date) as date_to
        FROM transactions
        {where}
    """
    async with db.execute(query, params) as cur:
        rows = await cur.fetchall()
        row_dict = dict(rows[0])
        sum_income = row_dict["sum_income"] or 0
        sum_expense = row_dict["sum_expense"] or 0
        row_dict["balance"] = sum_income - sum_expense
        return row_dict


@router.get("/summary")
async def get_summary(
    from_account: str,
    date_from: str | None = None,
    date_to: str | None = None,
    db: aiosqlite.Connection = Depends(get_db),
):
    """Retrieves the current balance, sum income, and sum, average, min, and max expense of a given account"""
    result = await summary(
        db,
        from_account=from_account,
        date_from=date_from,
        date_to=date_to,
    )
    return {
        "balance": result["balance"] or 0,
        "sum_income": result["sum_income"] or 0,
        "avg_income": result["avg_income"] or 0,
        "min_income": result["min_income"] or 0,
        "max_income": result["max_income"] or 0,
        "sum_expense": result["sum_expense"] or 0,
        "avg_expense": result["avg_expense"] or 0,
        "min_expense": result["min_expense"] or 0,
        "max_expense": result["max_expense"] or 0,
        "date_from": result["date_from"] or "",
        "date_to": result["date_to"] or "",
    }
