from calendar import monthrange
from datetime import datetime

import aiosqlite
from fastapi import APIRouter, Depends

from ..database import get_db
from .get_summary import get_summary

router = APIRouter(prefix="/transactions", tags=["transactions"])


async def rating(
    db: aiosqlite.Connection,
    from_account: str,
    date_from: str | None = None,
    date_to: str | None = None,
) -> int:
    current = await get_summary(
        db=db, from_account=from_account, date_from=date_from, date_to=date_to
    )

    date_now = datetime.strptime(current["date_to"], "%Y-%m-%d")
    _, month_range = monthrange(date_now.year, date_now.month)
    days_left = month_range - date_now.day + 1

    # Cannot divide by zero
    if not current["avg_expense"]:
        return 3

    print(days_left)
    ratio = current["balance"] / days_left / current["avg_expense"]
    # > +15% above average
    if ratio > 1.15:
        return 5
    # > +10% above average
    if ratio > 1.10:
        return 4
    # < -15% below average
    if ratio < 0.85:
        return 1
    # < -10% below average
    if ratio < 0.90:
        return 2
    # Between -5% and +5% (and the gaps)
    return 3


@router.get("/rating")
async def get_rating(
    from_account: str,
    date_from: str | None = None,
    date_to: str | None = None,
    db: aiosqlite.Connection = Depends(get_db),
):
    """Returns a performance score (1-5) based on available balance per day and its deviation from the average expense until the end of the month"""
    result = await rating(
        db, from_account=from_account, date_from=date_from, date_to=date_to
    )
    return {"rating": result}
