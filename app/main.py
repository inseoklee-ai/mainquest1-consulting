"""중소기업 AI 도입 컨설팅 신청 - FastAPI 진입점.

8단계: 선택적 Supabase 로그인 추가 (spec: user-auth, consulting-application 확장).
- 기존 "로그인 없이 신청/조회"는 그대로 유지
- 로그인 사용자는 검증된 이메일로 "내 신청"을 재입력 없이 조회
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from . import auth
from .config import AUTH_ENABLED, SESSION_SECRET
from .db import init_db
from .services import (
    WEEKLY_CAPACITY,
    create_application,
    find_applications,
    find_applications_by_email,
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="중소기업 AI 도입 컨설팅 신청", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

_STATUS_ALERT = {"ok": "success", "duplicate": "error", "full": "error",
                 "invalid": "error", "exists": "error", "error": "error"}


def render(request: Request, template: str, **context):
    """공통 컨텍스트(로그인 상태 등)를 넣어 템플릿을 렌더링."""
    base = {"user": auth.current_user(request), "auth_enabled": AUTH_ENABLED}
    base.update(context)
    return templates.TemplateResponse(request, template, base)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return render(request, "home.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "weekly_capacity": WEEKLY_CAPACITY, "auth_enabled": AUTH_ENABLED}


# ---------- 신청 ----------
@app.get("/apply", response_class=HTMLResponse)
def apply_form(request: Request):
    return render(request, "apply.html")


@app.post("/apply", response_class=HTMLResponse)
def apply_submit(request: Request, email: str = Form(...), phone: str = Form(...)):
    result = create_application(email, phone)
    keep = result["status"] != "ok"
    return render(
        request, "apply.html",
        email=email if keep else "",
        phone=phone if keep else "",
        message=result["message"],
        message_type=_STATUS_ALERT.get(result["status"], "info"),
    )


# ---------- 내 신청 내역 조회 ----------
@app.get("/my", response_class=HTMLResponse)
def my_form(request: Request):
    user = auth.current_user(request)
    if user:
        # 로그인 시: 검증된 이메일 기준 자동 조회 (휴대폰 불필요)
        return render(request, "my.html", searched=True,
                      applications=find_applications_by_email(user))
    return render(request, "my.html")


@app.post("/my", response_class=HTMLResponse)
def my_lookup(request: Request, email: str = Form(...), phone: str = Form(...)):
    return render(request, "my.html", email=email, phone=phone, searched=True,
                  applications=find_applications(email, phone))


# ---------- 인증 (로그인 기능이 켜졌을 때만) ----------
@app.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return render(request, "signup.html")


@app.post("/signup", response_class=HTMLResponse)
def signup_submit(request: Request, email: str = Form(...), password: str = Form(...)):
    if not AUTH_ENABLED:
        return render(request, "signup.html", message="로그인 기능이 아직 설정되지 않았습니다.", message_type="error")
    result = auth.sign_up(email, password)
    if result["status"] == "ok" and result.get("email"):
        auth.login_session(request, result["email"])
        return RedirectResponse("/my", status_code=303)
    return render(request, "signup.html", email=email,
                  message=result["message"],
                  message_type=_STATUS_ALERT.get(result["status"], "info"))


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return render(request, "login.html")


@app.post("/login", response_class=HTMLResponse)
def login_submit(request: Request, email: str = Form(...), password: str = Form(...)):
    if not AUTH_ENABLED:
        return render(request, "login.html", message="로그인 기능이 아직 설정되지 않았습니다.", message_type="error")
    result = auth.sign_in(email, password)
    if result["status"] == "ok":
        auth.login_session(request, result["email"])
        return RedirectResponse("/my", status_code=303)
    return render(request, "login.html", email=email,
                  message=result["message"],
                  message_type=_STATUS_ALERT.get(result["status"], "info"))


@app.post("/logout")
def logout(request: Request):
    auth.logout_session(request)
    return RedirectResponse("/", status_code=303)
