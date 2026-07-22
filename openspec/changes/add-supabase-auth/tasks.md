## 1. Supabase 준비 (사용자 작업 포함)

- [ ] 1.1 Supabase 계정 생성 + 프로젝트 1개 생성 (사용자)
- [ ] 1.2 프로젝트 설정에서 `Project URL`, `anon key` 복사 (사용자)
- [ ] 1.3 이메일 확인(Confirm email) 정책 확인/설정 (개발 편의상 off 또는 안내)
- [ ] 1.4 `.env`에 SUPABASE_URL / SUPABASE_ANON_KEY / SESSION_SECRET 저장 (사용자, 커밋 금지)
- [ ] 1.5 `.env.example` 작성 후 커밋 (값은 비움)

## 2. 의존성 / 설정

- [ ] 2.1 의존성 추가: `supabase`, `python-dotenv`, (세션) `itsdangerous`
- [ ] 2.2 앱 시작 시 .env 로드 + 설정 검증(키 없으면 명확한 에러)
- [ ] 2.3 SessionMiddleware 추가 (SESSION_SECRET 사용, HttpOnly)

## 3. 인증 서비스 계층

- [ ] 3.1 Supabase 클라이언트 초기화 모듈 (app/auth.py)
- [ ] 3.2 sign_up(email, password) 래퍼 + 에러 매핑(중복/형식)
- [ ] 3.3 sign_in(email, password) 래퍼 + 에러 매핑(자격 실패)
- [ ] 3.4 세션에 검증된 이메일 저장/삭제 헬퍼, current_user(request) 헬퍼

## 4. 화면 / 라우트

- [ ] 4.1 GET/POST /signup (회원가입 폼 + 처리)
- [ ] 4.2 GET/POST /login (로그인 폼 + 처리)
- [ ] 4.3 POST /logout (세션 종료)
- [ ] 4.4 헤더(base.html) 로그인 상태 분기 (로그인/회원가입 ↔ 이메일/로그아웃)
- [ ] 4.5 /my: 로그인 시 이메일 기준 자동 조회, 비로그인 시 기존 폼 유지

## 5. 신청 조회 로직 확장

- [ ] 5.1 services에 find_applications_by_email(email) 추가 (정규화 적용)
- [ ] 5.2 /my 라우트에서 로그인/비로그인 분기 연결 (스키마 변경 없음)

## 6. 테스트

- [ ] 6.1 로그인 이메일 기준 조회가 해당 이메일 신청만 반환하는지 (타 이메일 비노출)
- [ ] 6.2 비로그인 조회는 기존대로 이메일+휴대폰 둘 다 필요 (회귀 테스트 통과 유지)
- [ ] 6.3 (가능하면) 인증 래퍼는 Supabase 호출을 목(mock)으로 단위 테스트

## 7. 배포 / 문서

- [ ] 7.1 docs/DEPLOY.md에 Render 환경변수(SUPABASE_*, SESSION_SECRET) 등록 절차 추가
- [ ] 7.2 README 기능/진행 상태 갱신
- [ ] 7.3 로컬에서 회원가입→로그인→내 신청 자동조회→로그아웃 수동 확인
