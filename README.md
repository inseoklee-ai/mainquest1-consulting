# 중소기업 AI 도입 컨설팅 신청 (MainQuest1)

중소기업 대표가 **로그인 없이** 이메일·휴대폰번호만 남기면 "AI 도입 컨설팅"을 신청할 수 있는 웹 서비스입니다.

🌐 **배포 URL: https://mainquest1-consulting.onrender.com** (Render, 무료 플랜 — 첫 접속 시 최대 ~50초 로딩)

## 핵심 기능
- 로그인 없이 신청 (이메일 + 휴대폰번호)
- 한 사람당 1회만 신청 (중복 차단)
- **주 단위 정원 4명** — 정원 초과 절대 불가
- 내 신청 내역 조회 (이메일 + 휴대폰번호로)

## 기술 스택
- **Python + FastAPI + SQLite** (선정 근거는 [design.md](openspec/changes/add-consulting-application/design.md)의 `D0` 참조)
- 인증(심화): **Supabase Auth** — 선택적 로그인, 신청 데이터는 SQLite 유지(하이브리드)

## 문서 (docs/)
| 문서 | 내용 |
|------|------|
| [PRD.md](docs/PRD.md) | 기획 문서 1장 — 서비스 개요·타겟·해결 문제, 도메인 연결 문장 |
| [RETROSPECTIVE.md](docs/RETROSPECTIVE.md) | 회고록 — 오늘 결정한 것·참은 것, AI 협업하며 배운 점·어려웠던 점 |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | 서비스 구조 흐름도 — 4계층(화면·라우트·로직·데이터) + 다이어그램 |
| [RUN.md](docs/RUN.md) | 로컬 실행 방법 + 테스트 실행법 |
| [DEPLOY.md](docs/DEPLOY.md) | Render 배포 가이드 + 환경변수 등록 절차 |
| [SUBMISSION.md](docs/SUBMISSION.md) | 과제 제출 안내 — 루브릭 항목별 증거 매핑 |
| [AI_COLLABORATION.md](docs/AI_COLLABORATION.md) | AI 협업 기록(대화 원본) 틀 |

## 스펙 문서 (OpenSpec)
스펙 우선(Spec-Driven)으로 진행합니다.

**변경 단위 `add-consulting-application`** (핵심 신청 기능):
- [proposal.md](openspec/changes/add-consulting-application/proposal.md) — 왜/무엇을
- [spec.md](openspec/changes/add-consulting-application/specs/consulting-application/spec.md) — 요구사항·시나리오
- [design.md](openspec/changes/add-consulting-application/design.md) — 설계·스택 선정 근거
- [tasks.md](openspec/changes/add-consulting-application/tasks.md) — 구현 체크리스트

**변경 단위 `add-supabase-auth`** (선택적 로그인):
- [proposal.md](openspec/changes/add-supabase-auth/proposal.md) · [design.md](openspec/changes/add-supabase-auth/design.md) · [tasks.md](openspec/changes/add-supabase-auth/tasks.md)
- 스펙: [user-auth](openspec/changes/add-supabase-auth/specs/user-auth/spec.md) · [consulting-application(확장)](openspec/changes/add-supabase-auth/specs/consulting-application/spec.md)

## 진행 상태
- [x] 0. 스펙 작성 (OpenSpec)
- [x] 1. GitHub 저장소 + 스펙 업로드
- [x] 2. PRD(기획 문서) 작성 → [docs/PRD.md](docs/PRD.md)
- [x] 3. 프로젝트 뼈대 (FastAPI) — `app/main.py`, 서버 기동 확인 (`/`, `/health`, `/docs`)
- [x] 4. 화면 만들기 — 홈/신청(`/apply`)/조회(`/my`) 화면 + 폼 전송 동작 확인
- [x] 5. 화면 다듬기 — 디자인 시스템(인디고 톤/카드/반응형/다크모드) 적용
- [x] 6. 저장 + 정원 — SQLite 저장, 형식검증, 중복차단, 주 4명 정원(동시성 안전), 내역조회 · 테스트 14개 통과
- [x] 7. 검증 + 배포 — 테스트 통과 + Render 배포(라이브 신청/조회 검증 완료)
- [x] 8. 로그인 (Supabase) — 선택적 회원가입/로그인/로그아웃, 서버 세션
- [x] 9. 신청을 '내 것'으로 — 로그인 시 검증된 이메일로 내 신청 자동 조회

## 과제 제출물
- ✅ 실행 가능한 웹 서비스 — [GitHub](https://github.com/inseoklee-ai/mainquest1-consulting) / [배포 URL](https://mainquest1-consulting.onrender.com)
- ✅ 기획 문서 1장 — [docs/PRD.md](docs/PRD.md)
- ✅ 회고록 1장 — [docs/RETROSPECTIVE.md](docs/RETROSPECTIVE.md)
- 제출 방법·루브릭 증거 매핑 → [docs/SUBMISSION.md](docs/SUBMISSION.md)

## 테스트
- 스펙 시나리오 자동 테스트 21개 통과 (`tests/`) — 형식검증·중복차단·주4명 정원·동시성·조회·세션
