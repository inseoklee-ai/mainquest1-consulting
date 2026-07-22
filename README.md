# 중소기업 AI 도입 컨설팅 신청 (MainQuest1)

중소기업 대표가 **로그인 없이** 이메일·휴대폰번호만 남기면 "AI 도입 컨설팅"을 신청할 수 있는 웹 서비스입니다.

## 핵심 기능
- 로그인 없이 신청 (이메일 + 휴대폰번호)
- 한 사람당 1회만 신청 (중복 차단)
- **주 단위 정원 4명** — 정원 초과 절대 불가
- 내 신청 내역 조회 (이메일 + 휴대폰번호로)

## 기술 스택
- **Python + FastAPI + SQLite** (선정 근거는 [design.md](openspec/changes/add-consulting-application/design.md)의 `D0` 참조)

## 문서 (OpenSpec)
스펙 우선(Spec-Driven)으로 진행합니다. 변경 단위 `add-consulting-application`:
- [proposal.md](openspec/changes/add-consulting-application/proposal.md) — 왜/무엇을
- [spec.md](openspec/changes/add-consulting-application/specs/consulting-application/spec.md) — 요구사항·시나리오
- [design.md](openspec/changes/add-consulting-application/design.md) — 설계·스택 선정 근거
- [tasks.md](openspec/changes/add-consulting-application/tasks.md) — 구현 체크리스트

## 진행 상태
- [x] 0. 스펙 작성 (OpenSpec)
- [x] 1. GitHub 저장소 + 스펙 업로드
- [x] 2. PRD(기획 문서) 작성 → [docs/PRD.md](docs/PRD.md)
- [x] 3. 프로젝트 뼈대 (FastAPI) — `app/main.py`, 서버 기동 확인 (`/`, `/health`, `/docs`)
- [x] 4. 화면 만들기 — 홈/신청(`/apply`)/조회(`/my`) 화면 + 폼 전송 동작 확인
- [ ] 5. 화면 다듬기 (디자인)
- [ ] 6. 저장 + 정원 로직
- [ ] 7. 검증 + 배포
- [ ] 8. 로그인 (Supabase)
- [ ] 9. 신청을 '내 것'으로 연결

## 과제 제출물
- 실행 가능한 웹 서비스 (GitHub 저장소 / 배포 URL)
- 기획 문서 1장 (PRD)
- 회고록 1장
- 시연 영상 (3분 이내)
