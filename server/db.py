"""
phone-cluster: server.db

SQLite storage layer for server state (v0.x).
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_db_path() -> Path:
    # XDG-ish default without extra deps
    data_dir = Path.home() / ".local" / "share" / "phone-cluster"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "server.db"


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or default_db_path()
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            client_id    TEXT PRIMARY KEY,
            name         TEXT NOT NULL,
            created_at   TEXT NOT NULL,
            last_seen    TEXT NOT NULL,
            capabilities TEXT NOT NULL DEFAULT '{}'
        )
        """
    )
    conn.commit()
