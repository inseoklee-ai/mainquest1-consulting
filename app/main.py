"""중소기업 AI 도입 컨설팅 신청 - FastAPI 진입점.

4단계: 화면(신청/조회) 뼈대까지.
- 실제 저장·중복 차단·주 정원 로직은 6단계에서 붙인다.
- 지금은 폼이 정상적으로 보이고, 전송(POST)이 동작하는지까지 확인한다.
"""
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 주당 정원 (design.md D0/D3, spec 참조) — 한 곳에 모아둔다.
WEEKLY_CAPACITY = 4

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="중소기업 AI 도입 컨설팅 신청")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """홈 화면."""
    return templates.TemplateResponse(request, "home.html")


@app.get("/health")
def health() -> dict:
    """서비스 상태 확인용 엔드포인트."""
    return {"status": "ok", "weekly_capacity": WEEKLY_CAPACITY}


@app.get("/apply", response_class=HTMLResponse)
def apply_form(request: Request):
    """신청 화면(폼) 보여주기."""
    return templates.TemplateResponse(request, "apply.html")


@app.post("/apply", response_class=HTMLResponse)
def apply_submit(request: Request, email: str = Form(...), phone: str = Form(...)):
    """신청 폼 전송 처리 (4단계: 화면 동작 확인용 임시 응답).

    TODO(6단계): 형식 검증 → 중복 차단 → 주 정원 확인 후 저장.
    """
    return templates.TemplateResponse(
        request,
        "apply.html",
        {
            "email": email,
            "phone": phone,
            "message": f"입력을 받았습니다 (이메일: {email}, 휴대폰: {phone}). "
                       "실제 저장·정원 처리는 다음 단계에서 붙입니다.",
            "message_type": "info",
        },
    )


@app.get("/my", response_class=HTMLResponse)
def my_form(request: Request):
    """내 신청 내역 조회 화면(폼) 보여주기."""
    return templates.TemplateResponse(request, "my.html")


@app.post("/my", response_class=HTMLResponse)
def my_lookup(request: Request, email: str = Form(...), phone: str = Form(...)):
    """조회 폼 전송 처리 (4단계: 화면 동작 확인용 임시 응답).

    TODO(6단계): 이메일+휴대폰 둘 다 일치하는 신청 내역 조회.
    """
    return templates.TemplateResponse(
        request,
        "my.html",
        {
            "email": email,
            "phone": phone,
            "searched": True,
            "message": "조회 화면이 동작합니다. 실제 신청 내역 조회는 다음 단계에서 붙입니다.",
            "message_type": "info",
        },
    )
