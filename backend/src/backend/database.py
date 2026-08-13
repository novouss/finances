import os
import aiosqlite

DB_PATH = "database/finance.db"


async def _ensure_db_dir() -> None:
    """Ensures that the db directory exists"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


async def get_db() -> aiosqlite.Connection:
    """Retrieves the aiosqlite connection with row factory enabled"""
    await _ensure_db_dir()
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    return db


async def init_db() -> None:
    await _ensure_db_dir()
    query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATETIME NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            modified_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            from_account TEXT,
            to_account TEXT,
            amount REAL NOT NULL,
            description TEXT
        )
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(query)
        await db.commit()
