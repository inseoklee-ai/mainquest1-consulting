## Context

기존 서비스(add-consulting-application)는 FastAPI + SQLite로, 로그인 없이 이메일+휴대폰으로 신청/조회한다. 여기에 **선택적 로그인**을 Supabase Auth로 얹는다. 신청 데이터는 SQLite에 그대로 두고(인증만 Supabase), 로그인 사용자는 검증된 이메일로 자기 신청을 본다. 사용자는 초보 학습자이므로 구조를 단순하게 유지한다.

## Goals / Non-Goals

**Goals:**
- 선택적 회원가입/로그인/로그아웃 (Supabase Auth, 이메일+비밀번호)
- 로그인 사용자가 재입력 없이 "내 신청" 조회
- 기존 비로그인 흐름·SQLite 스키마 **무변경 유지**
- 비밀값 안전 관리(.env, 커밋 금지)

**Non-Goals:**
- 소셜 로그인(구글 등), 비밀번호 재설정 메일 커스터마이즈 — 이번 범위 아님
- 신청 데이터의 Supabase 이전 — 이번 범위 아님(SQLite 유지)
- 역할/권한(admin 등) — 이번 범위 아님

## Decisions

### D1. 인증 = Supabase Auth (이메일+비밀번호)
- 서버(FastAPI)에서 Supabase에 로그인/가입 요청 → 성공 시 사용자 정보/토큰 획득.
- **대안**: 직접 비밀번호 해시·세션 구현 → 보안 리스크·구현량 큼. 학습 목적상 Supabase 채택.

### D2. 세션 처리 = 서버측 세션 쿠키 (권장)
- 로그인 성공 후, 검증된 **사용자 이메일**(및 최소 정보)을 서버 세션에 저장하고 **HttpOnly 쿠키**로 세션 식별.
- Supabase access/refresh 토큰을 브라우저 JS에 노출하지 않는다(HttpOnly).
- 구현: `starlette.middleware.sessions.SessionMiddleware` (secret은 .env의 `SESSION_SECRET`).
- **대안**: 프런트에서 Supabase JS SDK로 토큰 보관 → 서버 렌더링 구조와 안 맞고 토큰 노출 위험. 서버 세션이 단순·안전.

### D3. "내 신청" 매칭 = 세션의 검증된 이메일
- 로그인 시: `find_applications_by_email(session_email)` (휴대폰 불필요).
- 비로그인 시: 기존 `find_applications(email, phone)` (둘 다 필요) 그대로.
- 신청 저장 로직/스키마는 **변경 없음**. 매칭은 기존 `email` 컬럼(정규화 동일 적용)으로 수행.

### D4. 비밀값/환경변수
| 변수 | 용도 |
|------|------|
| `SUPABASE_URL` | Supabase 프로젝트 URL |
| `SUPABASE_ANON_KEY` | 공개(anon) 키 |
| `SESSION_SECRET` | 세션 쿠키 서명용 랜덤 문자열 |
- `.env`에 저장, `.gitignore`에 포함(이미 있음). 예시는 `.env.example`로 커밋.
- Render 배포 시 대시보드 환경변수로 등록.

### D5. 라우트/화면(초안)
- `GET/POST /signup` — 회원가입
- `GET/POST /login` — 로그인
- `POST /logout` — 로그아웃
- `/my` — 로그인 상태면 이메일 기준 자동 조회, 비로그인이면 기존 폼
- 헤더: 로그인 상태에 따라 링크 분기(로그인/회원가입 ↔ 이메일/로그아웃)

### D6. 이메일 정규화 일관성
- 세션 이메일도 저장 시와 동일하게 소문자/trim 정규화 후 매칭한다(services.normalize_email 재사용).

## Risks / Trade-offs

- **[이메일 확인 흐름]** Supabase가 가입 시 확인 메일을 요구하도록 설정돼 있으면 즉시 로그인 안 될 수 있음 → 프로젝트 설정에서 확인 정책을 명시하고 문서화. Mitigation: 개발 중엔 확인 off 또는 확인 안내 화면 제공.
- **[토큰 노출]** access token이 클라이언트에 노출되면 위험 → HttpOnly 서버 세션만 사용(D2).
- **[매칭 불일치]** 로그인 이메일과 신청 시 이메일 표기가 다르면(대소문자 등) 못 찾음 → 양쪽 모두 정규화(D6).
- **[비밀값 커밋 사고]** 실수로 .env 커밋 → `.gitignore` 확인 + `.env.example`만 커밋.
- **[SQLite 임시 디스크]** 배포 재시작 시 신청 데이터 소실 가능(기존 이슈) → 과제 시연엔 무방, 영구화는 별도 change.

## Migration Plan

- 기존 데이터/스키마 변경 없음. 추가만 있음.
- 배포: Render 환경변수(SUPABASE_URL/ANON_KEY/SESSION_SECRET) 등록 후 재배포.
- 롤백: 인증 관련 라우트/미들웨어 제거 시 기존 비로그인 흐름 그대로 복귀.

## Open Questions

- 비밀번호 재설정(메일) 기능을 이번에 넣을지? (기본: 범위 밖)
- 로그인 사용자가 신청할 때 이메일을 자동 채워줄지? (편의 기능, 선택)
