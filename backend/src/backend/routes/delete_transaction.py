import aiosqlite
from fastapi import APIRouter, Depends, HTTPException, status

from ..database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])


async def delete(db: aiosqlite.Connection, id: int) -> bool:
    query = "DELETE FROM transactions WHERE id = ?"
    cur = await db.execute(query, (id,))
    await db.commit()
    return cur.rowcount > 0


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(id: int, db: aiosqlite.Connection = Depends(get_db)):
    """Deletes a transaction by its ID"""
    deleted = await delete(db, id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction ID {id} could not be found nor deleted",
        )
