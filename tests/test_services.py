"""스펙 시나리오 = 테스트 (spec/consulting-application).

각 스펙 시나리오를 자동 테스트로 검증한다.
테스트마다 임시 DB 파일을 사용해 실제 데이터와 분리한다.
"""
import threading
from datetime import datetime, timezone

import pytest

from app import db, services


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """각 테스트마다 격리된 임시 SQLite 파일을 쓰도록 DB_PATH를 교체."""
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init_db()
    yield


# ---------- 신청 접수 / 형식 검증 ----------
def test_정상_신청_접수():
    r = services.create_application("Owner@SME.co.kr", "010-1234-5678")
    assert r["status"] == "ok"


def test_이메일_형식_오류():
    r = services.create_application("not-an-email", "010-1234-5678")
    assert r["status"] == "invalid"


def test_휴대폰_형식_오류():
    r = services.create_application("a@b.com", "12")
    assert r["status"] == "invalid"


# ---------- 중복 차단 ----------
def test_동일인_재신청_거부():
    services.create_application("dup@a.com", "010-0000-0001")
    r = services.create_application("dup@a.com", "010-0000-0001")
    assert r["status"] == "duplicate"


def test_이메일_대소문자_공백_정규화_후_동일인():
    services.create_application("a@a.com", "010-0000-0002")
    r = services.create_application("  A@A.COM ", "01000000002")
    assert r["status"] == "duplicate"


def test_다른_사람은_정상_신청():
    services.create_application("p1@a.com", "010-0000-0011")
    r = services.create_application("p2@a.com", "010-0000-0012")
    assert r["status"] == "ok"


# ---------- 주 정원 4명 ----------
def test_정원_4명까지_접수_5번째_거부():
    results = [
        services.create_application(f"cap{i}@a.com", f"0100000{i:04d}")
        for i in range(4)
    ]
    assert all(r["status"] == "ok" for r in results)
    fifth = services.create_application("cap5@a.com", "0100009999")
    assert fifth["status"] == "full"


# ---------- 동시성: 정원 초과 절대 불가 (design D3) ----------
def test_동시_신청이_정원을_넘지_않음():
    """빈 주에 10명이 동시에 신청해도 정확히 4명만 접수되어야 한다."""
    N = 10
    results = [None] * N
    barrier = threading.Barrier(N)

    def worker(i):
        barrier.wait()  # 최대한 동시에 출발
        results[i] = services.create_application(f"c{i}@a.com", f"0101110{i:04d}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    ok = sum(1 for r in results if r["status"] == "ok")
    full = sum(1 for r in results if r["status"] == "full")
    assert ok == services.WEEKLY_CAPACITY
    assert ok + full == N

    # DB에도 정확히 4건만 저장됨
    conn = db.get_connection()
    try:
        count = conn.execute("SELECT COUNT(*) AS c FROM applications;").fetchone()["c"]
    finally:
        conn.close()
    assert count == services.WEEKLY_CAPACITY


# ---------- 주(week) 판정 / 다음 주 초기화 (design D1) ----------
def test_같은_주는_같은_week_key():
    # 2026-07-20(월) ~ 2026-07-26(일) 은 모두 같은 주
    mon = datetime(2026, 7, 20, 0, 0, tzinfo=services.KST)
    sun = datetime(2026, 7, 26, 23, 59, tzinfo=services.KST)
    assert services.week_key_for(mon) == services.week_key_for(sun) == "2026-07-20"


def test_다음_주는_다른_week_key():
    sun = datetime(2026, 7, 26, 23, 59, tzinfo=services.KST)
    next_mon = datetime(2026, 7, 27, 0, 0, tzinfo=services.KST)
    assert services.week_key_for(sun) != services.week_key_for(next_mon)
    assert services.week_key_for(next_mon) == "2026-07-27"


def test_UTC_입력도_KST로_판정():
    # 2026-07-19 15:30 UTC = 2026-07-20 00:30 KST → 월요일 주
    utc_dt = datetime(2026, 7, 19, 15, 30, tzinfo=timezone.utc)
    assert services.week_key_for(utc_dt) == "2026-07-20"


# ---------- 내 신청 내역 조회 ----------
def test_본인_내역_조회():
    services.create_application("me@a.com", "010-2222-3333")
    rows = services.find_applications("me@a.com", "010-2222-3333")
    assert len(rows) == 1


def test_내역_없음():
    rows = services.find_applications("none@a.com", "010-9999-9999")
    assert rows == []


def test_타인_내역_비노출_부분일치():
    """이메일만 같고 휴대폰이 다르면 노출되면 안 된다."""
    services.create_application("shared@a.com", "010-5555-0001")
    rows = services.find_applications("shared@a.com", "010-5555-9999")
    assert rows == []


# ---------- 로그인 사용자 조회 (이메일 기준, add-supabase-auth) ----------
def test_이메일_기준_조회는_해당_이메일만():
    services.create_application("login@a.com", "010-6666-0001")
    services.create_application("other@a.com", "010-6666-0002")
    rows = services.find_applications_by_email("login@a.com")
    assert len(rows) == 1
    assert rows[0]["email"] == "login@a.com"


def test_이메일_기준_조회_정규화_적용():
    services.create_application("Case@A.com", "010-6666-0003")
    rows = services.find_applications_by_email("  CASE@a.COM ")
    assert len(rows) == 1


def test_이메일_기준_조회_없으면_빈리스트():
    assert services.find_applications_by_email("nobody@a.com") == []
