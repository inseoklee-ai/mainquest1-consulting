# 배포 가이드 (Render)

이 프로젝트는 `render.yaml`(Blueprint)로 Render에 배포합니다.

## 준비물
- GitHub 저장소 (이미 있음): https://github.com/inseoklee-ai/mainquest1-consulting
- Render 계정 (무료) — https://render.com 에서 GitHub으로 가입

## 배포 순서
1. Render 로그인 → **New +** → **Blueprint**
2. 이 GitHub 저장소(`mainquest1-consulting`) 선택 → Render가 `render.yaml`을 자동 인식
3. **Apply** 클릭 → 빌드/배포 시작 (몇 분 소요)
4. 완료되면 `https://mainquest1-consulting.onrender.com` 형태의 URL 발급
5. 그 URL을 브라우저에서 열어 신청/조회 동작 확인

## 동작 원리 (설정 요약)
- 빌드: `pip install -r requirements.txt`
- 실행: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Python: 3.12.7 (Render 호환용. 로컬 개발은 3.14)

## ⚠️ SQLite 주의 (무료 플랜)
Render 무료 플랜은 디스크가 **임시**라서, 재배포·재시작 시 `consulting.db`가 초기화될 수 있습니다.
- 과제 **시연**에는 충분합니다.
- **영구 저장**이 필요하면 8단계에서 붙일 **Supabase(PostgreSQL)** 로 데이터베이스를 옮기면 됩니다.

## 무료 플랜 특성
- 일정 시간 요청이 없으면 서버가 잠자기(sleep) 상태가 되어, 첫 접속이 느릴 수 있습니다(수십 초). 정상입니다.

## 로그인(Supabase) 사용 시 — 환경변수 등록
로그인 기능을 배포본에서도 켜려면, Render 대시보드에서 환경변수를 등록해야 합니다.
1. Render → 웹 서비스(mainquest1-consulting) → 왼쪽 **Environment**
2. 아래 3개를 **Add Environment Variable** 로 추가 (값은 로컬 `.env`와 동일):
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SESSION_SECRET`
3. 저장하면 자동 재배포됩니다.
> 환경변수를 등록하지 않으면 배포본은 `AUTH_ENABLED=false`가 되어, 로그인 없이 신청/조회만 동작합니다(기존 흐름은 그대로 유지).
> Supabase 대시보드에서 이메일 확인(Confirm email)을 OFF로 두어야 데모 로그인이 매끄럽습니다.
