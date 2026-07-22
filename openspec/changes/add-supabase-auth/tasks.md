## 1. Supabase 준비 (사용자 작업 포함)

- [x] 1.1 Supabase 계정 생성 + 프로젝트 생성 (mainquest1-consulting)
- [x] 1.2 Project URL, anon(legacy) key 복사
- [x] 1.3 이메일 확인(Confirm email) OFF 설정
- [x] 1.4 `.env`에 SUPABASE_URL / SUPABASE_ANON_KEY / SESSION_SECRET 저장 (커밋 안 됨)
- [x] 1.5 `.env.example` 작성 후 커밋 (값 비움)

## 2. 의존성 / 설정

- [x] 2.1 의존성 추가: supabase, python-dotenv, itsdangerous
- [x] 2.2 app/config.py: .env 로드 + AUTH_ENABLED 판정
- [x] 2.3 SessionMiddleware 추가 (SESSION_SECRET)

## 3. 인증 서비스 계층

- [x] 3.1 Supabase 클라이언트 초기화 (app/auth.py)
- [x] 3.2 sign_up 래퍼 + 에러 매핑(중복/형식)
- [x] 3.3 sign_in 래퍼 + 에러 매핑(자격 실패)
- [x] 3.4 세션 저장/삭제 + current_user 헬퍼

## 4. 화면 / 라우트

- [x] 4.1 GET/POST /signup
- [x] 4.2 GET/POST /login
- [x] 4.3 POST /logout
- [x] 4.4 헤더 로그인 상태 분기
- [x] 4.5 /my: 로그인 시 이메일 기준 자동 조회, 비로그인 시 기존 폼

## 5. 신청 조회 로직 확장

- [x] 5.1 services.find_applications_by_email(email) (정규화 적용)
- [x] 5.2 /my 로그인/비로그인 분기 (스키마 변경 없음)

## 6. 테스트

- [x] 6.1 로그인 이메일 기준 조회가 해당 이메일 신청만 반환 (타 이메일 비노출)
- [x] 6.2 비로그인 조회는 기존대로 이메일+휴대폰 (회귀 통과 유지)
- [x] 6.3 세션 헬퍼(login/logout/current_user) 단위 테스트

## 7. 배포 / 문서

- [x] 7.1 docs/DEPLOY.md에 Render 환경변수(SUPABASE_*, SESSION_SECRET) 등록 절차 추가
- [x] 7.2 README 기능/진행 상태 갱신
- [x] 7.3 로컬에서 회원가입→자동로그인→내 신청 자동조회→로그아웃 수동 확인
