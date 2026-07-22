"""인증 로직 (Supabase Auth) — spec: user-auth.

- 회원가입 / 로그인 래퍼 (Supabase Auth 이메일+비밀번호)
- 세션(서버측 쿠키)에 '검증된 이메일'만 저장 (design D2/D3)
- 토큰은 클라이언트에 노출하지 않는다.
"""
from functools import lru_cache

from .config import AUTH_ENABLED, SUPABASE_ANON_KEY, SUPABASE_URL
from .services import normalize_email

# Supabase 인증 에러 타입 (패키지 위치가 버전마다 달라 방어적으로 import)
try:
    from supabase_auth.errors import AuthApiError
except Exception:  # pragma: no cover
    class AuthApiError(Exception):
        pass

SESSION_KEY = "user_email"


@lru_cache(maxsize=1)
def get_client():
    """Supabase 클라이언트 (한 번 생성 후 재사용)."""
    from supabase import create_client
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


# ---------- 회원가입 ----------
def sign_up(email: str, password: str) -> dict:
    """결과: {status, message}. status ∈ {ok, exists, invalid, error}"""
    email_n = normalize_email(email)
    if not email_n or not password:
        return {"status": "invalid", "message": "이메일과 비밀번호를 모두 입력해주세요."}
    try:
        res = get_client().auth.sign_up({"email": email_n, "password": password})
    except AuthApiError as e:
        msg = str(e).lower()
        if "registered" in msg or "already" in msg or "exists" in msg:
            return {"status": "exists", "message": "이미 가입된 이메일입니다. 로그인해주세요."}
        return {"status": "invalid", "message": f"회원가입에 실패했습니다: {e}"}
    except Exception as e:  # 네트워크/설정 오류 등
        return {"status": "error", "message": f"회원가입 처리 중 오류가 발생했습니다: {e}"}

    # 이메일 확인(Confirm email)이 켜져 있으면 session이 없을 수 있다.
    if getattr(res, "session", None):
        return {"status": "ok", "message": "가입이 완료되어 로그인되었습니다.", "email": email_n}
    return {"status": "ok", "message": "가입되었습니다. 이메일 확인이 필요할 수 있어요. 확인 후 로그인해주세요.", "email": None}


# ---------- 로그인 ----------
def sign_in(email: str, password: str) -> dict:
    """결과: {status, message, email?}. status ∈ {ok, invalid, error}"""
    email_n = normalize_email(email)
    if not email_n or not password:
        return {"status": "invalid", "message": "이메일과 비밀번호를 모두 입력해주세요."}
    try:
        res = get_client().auth.sign_in_with_password({"email": email_n, "password": password})
    except AuthApiError:
        return {"status": "invalid", "message": "이메일 또는 비밀번호가 올바르지 않습니다."}
    except Exception as e:
        return {"status": "error", "message": f"로그인 처리 중 오류가 발생했습니다: {e}"}

    if getattr(res, "user", None):
        # Supabase가 검증한 이메일을 신뢰한다.
        verified = normalize_email(getattr(res.user, "email", email_n) or email_n)
        return {"status": "ok", "message": "로그인되었습니다.", "email": verified}
    return {"status": "invalid", "message": "이메일 또는 비밀번호가 올바르지 않습니다."}


# ---------- 세션 헬퍼 ----------
def login_session(request, email: str) -> None:
    request.session[SESSION_KEY] = normalize_email(email)


def logout_session(request) -> None:
    request.session.pop(SESSION_KEY, None)


def current_user(request):
    """로그인한 사용자의 이메일 (없으면 None)."""
    return request.session.get(SESSION_KEY)
