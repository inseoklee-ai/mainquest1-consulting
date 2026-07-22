"""신청 관련 비즈니스 로직 (spec: consulting-application).

핵심 규칙
- 이메일/휴대폰 형식 검증
- 정규화: 이메일 소문자, 휴대폰 숫자만 (design D2)
- 중복 차단: 동일 (email, phone) 전체 1회
- 주 정원 4명: 신청 시각(KST) 기준 그 주(월~일), 동시성에도 초과 없음 (design D1/D3)
"""
import re
import sqlite3
from datetime import datetime, timedelta, timezone

from .db import get_connection

WEEKLY_CAPACITY = 4
KST = timezone(timedelta(hours=9))

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ---------- 정규화 ----------
def normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def normalize_phone(phone: str) -> str:
    """숫자만 남긴다. 예: '010-1234-5678' -> '01012345678'"""
    return re.sub(r"\D", "", phone or "")


# ---------- 검증 ----------
def validate_email(email: str) -> bool:
    return bool(_EMAIL_RE.match(email))


def validate_phone(phone_digits: str) -> bool:
    """한국 휴대폰: 0으로 시작하는 10~11자리 숫자."""
    return bool(re.fullmatch(r"0\d{9,10}", phone_digits))


# ---------- 주(week) 판정 (design D1) ----------
def week_key_for(dt: datetime) -> str:
    """주어진 시각(KST 변환)이 속한 주의 '월요일 날짜'(YYYY-MM-DD)를 반환."""
    kst_dt = dt.astimezone(KST)
    monday = kst_dt.date() - timedelta(days=kst_dt.weekday())
    return monday.isoformat()


def current_week_key() -> str:
    return week_key_for(datetime.now(timezone.utc))


# ---------- 신청 생성 (핵심) ----------
def create_application(email: str, phone: str) -> dict:
    """신청을 저장한다. 결과: {status, message}.

    status ∈ {"invalid", "duplicate", "full", "ok"}
    정원 확인 + 저장을 BEGIN IMMEDIATE 트랜잭션으로 원자적 처리 (design D3).
    """
    email_n = normalize_email(email)
    phone_n = normalize_phone(phone)

    if not validate_email(email_n):
        return {"status": "invalid", "message": "이메일 형식이 올바르지 않습니다."}
    if not validate_phone(phone_n):
        return {"status": "invalid", "message": "휴대폰번호 형식이 올바르지 않습니다. (예: 010-1234-5678)"}

    week_key = current_week_key()
    created_at = datetime.now(timezone.utc).isoformat()

    conn = get_connection()
    try:
        # 쓰기 락을 즉시 잡아 동시 신청을 직렬화한다.
        conn.execute("BEGIN IMMEDIATE;")

        # 1) 중복 차단 (전체 1회)
        dup = conn.execute(
            "SELECT 1 FROM applications WHERE email = ? AND phone = ? LIMIT 1;",
            (email_n, phone_n),
        ).fetchone()
        if dup:
            conn.execute("ROLLBACK;")
            return {"status": "duplicate", "message": "이미 신청 내역이 있습니다. '내 신청 내역'에서 확인해주세요."}

        # 2) 주 정원 확인
        count = conn.execute(
            "SELECT COUNT(*) AS c FROM applications WHERE week_key = ?;",
            (week_key,),
        ).fetchone()["c"]
        if count >= WEEKLY_CAPACITY:
            conn.execute("ROLLBACK;")
            return {"status": "full", "message": "이번 주 정원(4명)이 마감되었습니다. 다음 주에 다시 신청해주세요."}

        # 3) 저장
        conn.execute(
            "INSERT INTO applications (email, phone, week_key, created_at) VALUES (?, ?, ?, ?);",
            (email_n, phone_n, week_key, created_at),
        )
        conn.execute("COMMIT;")
        return {"status": "ok", "message": "신청이 정상 접수되었습니다. 순서대로 연락드리겠습니다."}
    except sqlite3.IntegrityError:
        # UNIQUE 위반 = 동시 중복 신청. 최종 방어선 (design D2).
        try:
            conn.execute("ROLLBACK;")
        except sqlite3.Error:
            pass
        return {"status": "duplicate", "message": "이미 신청 내역이 있습니다. '내 신청 내역'에서 확인해주세요."}
    finally:
        conn.close()


# ---------- 내 신청 내역 조회 (email + phone 둘 다 일치) ----------
def find_applications(email: str, phone: str) -> list[dict]:
    email_n = normalize_email(email)
    phone_n = normalize_phone(phone)
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT email, phone, week_key, created_at FROM applications "
            "WHERE email = ? AND phone = ? ORDER BY created_at DESC;",
            (email_n, phone_n),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def find_applications_by_email(email: str) -> list[dict]:
    """로그인 사용자용: 검증된 이메일 기준 조회 (휴대폰 불필요, design D3)."""
    email_n = normalize_email(email)
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT email, phone, week_key, created_at FROM applications "
            "WHERE email = ? ORDER BY created_at DESC;",
            (email_n,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
