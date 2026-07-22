# 실행 방법 (로컬 개발)

## 1. 최초 1회 — 가상환경 + 의존성 설치
```powershell
cd C:\Users\lis29\MainQuest1
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. 서버 실행
```powershell
cd C:\Users\lis29\MainQuest1
.\.venv\Scripts\uvicorn.exe app.main:app --reload --port 8020
```

## 3. 브라우저에서 확인
- 홈: http://localhost:8020
- 상태확인: http://localhost:8020/health
- 자동 API 문서: http://localhost:8020/docs

## 테스트 실행
```powershell
cd C:\Users\lis29\MainQuest1
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -v
```
스펙 시나리오(형식 검증·중복 차단·주 4명 정원·동시성·내역 조회)를 자동 검증합니다.

## 종료
터미널에서 `Ctrl + C`
