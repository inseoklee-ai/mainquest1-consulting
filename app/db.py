"""SQLite 데이터 계층 (design.md D4).

- applications 테이블
- UNIQUE(email, phone): 중복 신청 차단 (design D2)
- week_key 인덱스: 주 정원 카운트 (design D1/D3)
"""
import sqlite3
from pathlib import Path

# 프로젝트 루트의 consulting.db (.gitignore 로 커밋 제외)
DB_PATH = Path(__file__).resolve().parent.parent / "consulting.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS applications (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    email      TEXT NOT NULL,
    phone      TEXT NOT NULL,
    week_key   TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(email, phone)
);
CREATE INDEX IF NOT EXISTS idx_applications_week_key
    ON applications(week_key);
"""


def get_connection() -> sqlite3.Connection:
    """새 DB 커넥션. 정원 동시성 제어(BEGIN IMMEDIATE)를 위해
    자동 트랜잭션을 끄고(isolation_level=None) 수동으로 제어한다.
    """
    conn = sqlite3.connect(DB_PATH, isolation_level=None, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_db() -> None:
    """앱 시작 시 테이블/인덱스 생성 (없으면)."""
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
    finally:
        conn.close()
