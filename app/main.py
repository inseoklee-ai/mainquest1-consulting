"""중소기업 AI 도입 컨설팅 신청 - FastAPI 진입점 (3단계: 프로젝트 뼈대).

지금은 서버가 정상적으로 켜지는지 확인하는 최소 버전이다.
신청/조회 기능은 이후 단계(4~6단계)에서 붙인다.
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# 주당 정원 (design.md D0/D3, spec 참조) — 한 곳에 모아둔다.
WEEKLY_CAPACITY = 4

app = FastAPI(title="중소기업 AI 도입 컨설팅 신청")


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    """서버가 살아있음을 눈으로 확인하는 임시 홈 화면."""
    return """
    <!doctype html>
    <html lang="ko">
    <head><meta charset="utf-8"><title>중소기업 AI 도입 컨설팅 신청</title></head>
    <body style="font-family: sans-serif; max-width: 640px; margin: 60px auto; line-height: 1.6;">
      <h1>중소기업 AI 도입 컨설팅 신청</h1>
      <p>서버가 정상적으로 동작 중입니다. (3단계: 프로젝트 뼈대 완료)</p>
      <p>다음 단계에서 신청 화면과 내 신청 내역 조회를 붙입니다.</p>
      <p><a href="/docs">API 문서(/docs)</a> · <a href="/health">상태확인(/health)</a></p>
    </body>
    </html>
    """


@app.get("/health")
def health() -> dict:
    """서비스 상태 확인용 엔드포인트."""
    return {"status": "ok", "weekly_capacity": WEEKLY_CAPACITY}
