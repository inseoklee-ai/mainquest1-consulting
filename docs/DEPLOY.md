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
