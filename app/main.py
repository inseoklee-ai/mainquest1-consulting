"""중소기업 AI 도입 컨설팅 신청 - FastAPI 진입점.

6단계: 저장 + 정원 로직 연결.
- SQLite 저장, 형식 검증, 중복 차단, 주 4명 정원(동시성 안전)
- 내 신청 내역 조회 (이메일+휴대폰 둘 다 일치)
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db import init_db
from .services import WEEKLY_CAPACITY, create_application, find_applications

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작 시 DB 테이블/인덱스 준비."""
    init_db()
    yield


app = FastAPI(title="중소기업 AI 도입 컨설팅 신청", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


# 신청 결과 status -> 화면 알림 종류
_STATUS_ALERT = {"ok": "success", "duplicate": "error", "full": "error", "invalid": "error"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "weekly_capacity": WEEKLY_CAPACITY}


@app.get("/apply", response_class=HTMLResponse)
def apply_form(request: Request):
    return templates.TemplateResponse(request, "apply.html")


@app.post("/apply", response_class=HTMLResponse)
def apply_submit(request: Request, email: str = Form(...), phone: str = Form(...)):
    result = create_application(email, phone)
    # 성공 시엔 입력값을 지워 다시 제출 실수를 줄인다.
    keep = result["status"] != "ok"
    return templates.TemplateResponse(
        request,
        "apply.html",
        {
            "email": email if keep else "",
            "phone": phone if keep else "",
            "message": result["message"],
            "message_type": _STATUS_ALERT.get(result["status"], "info"),
        },
    )


@app.get("/my", response_class=HTMLResponse)
def my_form(request: Request):
    return templates.TemplateResponse(request, "my.html")


@app.post("/my", response_class=HTMLResponse)
def my_lookup(request: Request, email: str = Form(...), phone: str = Form(...)):
    applications = find_applications(email, phone)
    return templates.TemplateResponse(
        request,
        "my.html",
        {
            "email": email,
            "phone": phone,
            "searched": True,
            "applications": applications,
        },
    )
