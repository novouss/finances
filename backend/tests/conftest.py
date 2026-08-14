from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import database


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """Creates an isolated test database file"""
    return tmp_path / "test.db"


@pytest.fixture
def client(db_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Wires TestClient to isolated test database"""
    monkeypatch.setattr(database, "DB_PATH", db_path)
    from backend.main import app

    with TestClient(app) as c:
        yield c
