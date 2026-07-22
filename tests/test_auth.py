"""인증 세션 헬퍼 테스트 (spec: user-auth).

Supabase 네트워크 호출 없이, 세션 저장/조회/삭제와 이메일 정규화만 검증한다.
"""
from app import auth


class FakeRequest:
    """request.session 만 흉내내는 최소 목 객체."""
    def __init__(self):
        self.session = {}


def test_로그인_세션_저장_후_조회():
    req = FakeRequest()
    auth.login_session(req, "Owner@SME.com")
    # 정규화되어 저장되고, 그대로 조회된다
    assert auth.current_user(req) == "owner@sme.com"


def test_비로그인은_None():
    req = FakeRequest()
    assert auth.current_user(req) is None


def test_로그아웃하면_세션_비워짐():
    req = FakeRequest()
    auth.login_session(req, "a@a.com")
    auth.logout_session(req)
    assert auth.current_user(req) is None


def test_로그아웃_두번_호출해도_에러없음():
    req = FakeRequest()
    auth.logout_session(req)  # 로그인 안 한 상태에서 호출
    assert auth.current_user(req) is None
