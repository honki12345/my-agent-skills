# Agent Skills

개인 에이전트 skills 모음

## 설치된 Skills

| Skill | 설명 | 트리거 | 생성일 |
|-------|------|--------|--------|
| `gh-cli` | GitHub CLI(gh) 통합 레퍼런스 (repo/issue/pr/actions/projects/releases 등) | GitHub CLI 명령어 사용/조회 작업 시 | 2026-02-21 |
| `pr-merge-conflict` | PR URL 기반 merge conflict 감지/원인 PR 추적 + 계획 문서 기반 충돌 해결 커밋/푸시 | `/pr-merge-conflict {pr-url}` 요청 시 | 2026-02-18 |
| `pr-ci-loop` | PR URL 기반 GitHub Actions CI 실패 분석/수정 커밋/푸시 + 성공까지 폴링 루프 | `/pr-ci-loop {pr-url}` 요청 시 | 2026-02-17 |
| `issue-worktree-plan` | 이슈 URL 기반으로 git worktree 브랜치 생성 + 계획 문서 생성 | `/issue-worktree-plan {issue-url}` 요청 시 | 2026-02-15 |
| `codebase-doc-writer` | 저장소 코드를 직접 읽어 기술 문서 패키지 생성/갱신 | 프로젝트 문서화, 위키 문서화, 코드 기준 문서 갱신 요청 시 | 2026-02-15 |
| `branch-doc-sync` | 현재 브랜치 변경분 기준으로 관리 문서를 전수 점검해 영향 판정 후 필요한 문서를 직접 수정 | 브랜치 변경사항 기준 문서 전수 점검/동기화 요청 시 | 2026-02-15 |
| `gh-review-triage` | PR 코멘트별 초안 판정 + 수동 텍스트 승인 루프 순차 확정 + 반영 후 계획 문서 업데이트 | PR 링크(또는 현재 브랜치 PR)로 리뷰 코멘트 판정을 요청할 때 | 2026-02-15 |
| `debug-loop` | 버그 재현 우선 + git/문서 기반 가설 검증 + 수정/로깅 반복 루프 + 마지막 문서 업데이트 점검 | `/debug-loop` 수동 호출 | 2026-02-14 |
| `implement-plan` | 계획 문서 기반 구현 + 이탈 시 승인 게이트 + 테스트 통과 시도 | `/implement-plan` 수동 호출 | 2026-02-14 |
| `plan-review` | 구현 계획 문서 6관점 순차 리뷰 + 수동 질의 시 권장안/이유 제시 + 관점6 질문 1개씩 선택 루프 + 반복 안정화 | `/plan-review` 수동 호출 | 2026-02-14 |
| `git-master` | Git 원자적 커밋 분리, 히스토리 정리, 변경 추적 | `/git-master` 수동 호출 | 2026-02-14 |
| `obsidian-cli` | Obsidian CLI 명령어 레퍼런스 | obsidian 명령어, 볼트 관리, 플러그인 관리 작업 시 | 2026-02-12 |
| `tanstack-query` | TanStack Query (React Query) v5 가이드 (72개 문서) | @tanstack/react-query 패키지 사용 시 | 2026-01-31 |
| `ship` | 변경사항 커밋/푸시 자동화 + PR GitHub Actions CI 폴링/실패 복구 | `ship` 또는 `ship {문서경로}` 요청 시 | 2026-01-30 |
| `github-graphql` | GitHub GraphQL API 가이드 (7개 문서) | GitHub API, GraphQL, contributionsCollection 키워드 | 2026-01-25 |
| `nestjs` | NestJS 프레임워크 가이드 (133개 문서) | NestJS 프로젝트, @nestjs 패키지 사용 시 | 2026-01-24 |
| `sqlite` | SQLite 데이터베이스 가이드 | .db/.sqlite 파일 작업, ORM 사용 시 | 2026-01-24 |
| `vercel-react-best-practices` | React/Next.js 성능 최적화 (45개 규칙) | React/Next.js 코드 작성/리뷰 시 | 2026-01-24 |
| `web-design-guidelines` | UI 코드 접근성/UX 리뷰 | UI 리뷰 요청 시 | 2026-01-24 |

## 사용법

이 디렉토리의 skills는 모든 프로젝트에서 자동으로 사용 가능합니다.
필요한 스킬을 `/skill-name ...` 형태로 직접 호출하거나, 작업 맥락에 따라 자동 로드됩니다.

---

## Issue Worktree Plan Skill 상세

GitHub 이슈 URL 하나로 브랜치/worktree/계획 문서를 안전하게 초기화하는 작업형 스킬입니다.

### 트리거 및 입력

- 호출: `/issue-worktree-plan {issue-url}`
- URL 형식: `https://github.com/{owner}/{repo}/issues/{number}`
- 브랜치 규칙은 프로젝트 문서(`AGENTS.md`, `README.md`, `CONTRIBUTING.md`)를 우선 적용

### 핵심 절차

1. `gh issue view`로 이슈 상태/제목/본문을 확인합니다.
2. 기본 브랜치(`origin/HEAD` 우선)를 결정하고 브랜치명을 생성합니다.
3. `git worktree add -b ...`로 분리 작업 디렉토리를 만듭니다.
4. `docs/plan/ISSUE_{번호}_{slug}.md` 템플릿 문서를 생성합니다.
5. 기존 브랜치/워크트리/문서가 충돌하면 덮어쓰지 않고 확인 게이트를 거칩니다.

### 산출물

- 작업 브랜치와 worktree 경로 (`.worktrees/{branch}`)
- 이슈 기반 계획 문서 (`docs/plan/ISSUE_{번호}_{slug}.md`)
- 다음 작업 시작용 `cd {worktree}` 안내

### 사용 예시

```bash
/issue-worktree-plan https://github.com/org/repo/issues/123
```

---

## Codebase Doc Writer Skill 상세

저장소 구현을 직접 읽고 근거 기반 기술 문서를 만드는 작업형 스킬입니다.

### 트리거 및 입력

- 호출: `/codebase-doc-writer`
- 입력: 저장소 루트, 출력 경로, 범위(full/부분), 독자 대상(개발/운영/온보딩)

### 핵심 절차

1. 디렉토리/엔트리포인트/런타임 경계를 맵으로 정리합니다.
2. 코드/설정 기준으로 구현 사실을 추출합니다.
3. 개요/아키텍처/API/운영/기여 섹션을 코드 근거 기반으로 작성합니다.
4. 섹션별 `Sources` 경로를 남겨 추적성을 보장합니다.
5. 모호한 부분은 추정하지 않고 `unknown` 성격으로 명시합니다.

### 산출물

- 구현 기반 문서 패키지(신규 생성 또는 갱신)
- 모듈별 근거 경로가 포함된 문서
- 누락/불명확 영역 체크 결과

### 사용 예시

```bash
/codebase-doc-writer
```

---

## Branch Doc Sync Skill 상세

현재 브랜치의 변경사항을 기준으로 프로젝트의 관리 문서를 전수 점검하고, 문서별 영향 판정을 거쳐 필요한 문서를 직접 수정하는 스킬입니다.

### 트리거 및 입력

- 호출: `/branch-doc-sync`
- 입력: 기준 브랜치(`origin/main` 기본), 관리 문서 규칙, 변경 범위
- 지원 리소스: `scripts/generate_doc_impact_report.py`, `assets/config/docs-impact-map.yml`

### 핵심 절차

1. `git diff <base>...HEAD`로 브랜치 변경 파일을 수집합니다.
2. `git ls-files`로 관리 문서를 전수 인벤토리화합니다.
3. 문서별 결정을 `update / no-change / add`로 하나씩 확정합니다.
4. `update`/`add` 문서를 직접 수정하고 근거(`Sources`)를 남깁니다.
5. 명령어/경로/링크/환경변수 유효성을 검증합니다.

### 산출물

- 전 문서 의사결정 매트릭스(누락 없는 리뷰 결과)
- 수정된 문서들과 변경 근거
- 영향 요약 리포트(`references/report-format.md` 포맷)

### 사용 예시

```bash
/branch-doc-sync
```

---

## GH Review Triage Skill 상세

PR 링크를 입력받아 리뷰 코멘트의 반영 여부를 판단하고 실행 가능한 액션으로 정리하는 작업형 스킬입니다.

### 트리거 및 입력

- 호출: `/gh-review-triage [pr-url] [plan-doc-path(optional)]`
- 인자 생략 시 현재 브랜치 PR을 자동 탐지합니다.
- 승인 입력은 `승인`, `승인 안 함`, `수정 지시: ...` 3가지로 제한됩니다.

### 핵심 절차

1. `gh` 인증/PR 접근 가능 여부를 확인합니다.
2. 인라인 리뷰/리뷰 코멘트/일반 코멘트를 모두 수집합니다.
3. 코멘트별 초안 판단(`반영/미반영/판단 보류`)을 근거와 함께 제시합니다.
4. 코멘트 단위로 수동 승인 루프를 순차 실행합니다.
5. 실제 반영이 발생하면 계획 문서(`PR 리뷰 반영 내역`)를 동기화합니다.

### 산출물

- 코멘트별 최종 판정 로그(`decision_log`)
- 반영 항목의 대상 파일/검증 계획
- 계획 문서 동기화 결과(`UPDATED/SKIPPED/FAILED`)

### 사용 예시

```bash
/gh-review-triage
/gh-review-triage https://github.com/org/repo/pull/123
/gh-review-triage https://github.com/org/repo/pull/123 docs/plan/feature-x.md
```

---

## Debug Loop Skill 상세

버그 상황에서 재현을 최우선으로 두고, 가설 검증 루프를 반복해 원인을 좁히는 디버깅 스킬입니다.

### 트리거 및 입력

- 호출: `/debug-loop "{버그상황}" "{로그}" "{문서경로(optional)}"`
- 입력 부족 시 재현 절차/기대값/실제값/스택트레이스/환경을 우선 요청합니다.
- 재현 전 임의 수정은 금지됩니다.

### 핵심 절차

1. 버그 재현 절차를 고정하고 재현 성공 여부를 기록합니다.
2. git 이력, 로그, 문서, 코드 컨텍스트를 함께 수집합니다.
3. 근거 기반 가설(권장 2~3개)을 만들고 하나씩 검증합니다.
4. `가설 -> 최소 수정/로깅 -> 재현 테스트` 루프를 반복합니다.
5. 테스트 안정화 후 문서 영향(`AGENTS.md`, `README.md`, `docs/`, `plans/`)을 점검합니다.

### 승인 게이트

- 방향 전환, 대규모 리팩토링, 위험한 마이그레이션, 계측 전략 변경 시 필수
- 승인 없이 범위 확장은 수행하지 않습니다.

### 사용 예시

```bash
/debug-loop "로그인 시 500 에러" "logs/server.log" "docs/plan/auth-hotfix.md"
```

---

## Implement Plan Skill 상세

계획 문서를 기준으로 구현을 수행하고, 계획 이탈 시 승인 절차를 강제하는 구현 스킬입니다.

### 트리거 및 입력

- 호출: `/implement-plan {plan-file-path}`
- 입력 파일이 없거나 경로가 잘못되면 중단 후 재입력을 요청합니다.
- 구현은 계획 문서 범위 밖으로 확장하지 않습니다.

### 핵심 절차

1. 계획 문서에서 목표/범위/제약/테스트 항목을 추출합니다.
2. 계획 단계 순서대로 구현하고 변경을 항목별로 매핑합니다.
3. 모순·모호성·계획 외 변경 필요 시 승인 게이트로 전환합니다.
4. 계획 내 테스트를 가능한 범위에서 모두 통과할 때까지 반복 시도합니다.
5. 최종 결과를 계획 대비 완료/미완료/리스크로 보고합니다.

### 승인 게이트

- 계획과 실제 코드 구조 불일치
- 계획 기술 선택이 현재 환경에서 불가
- 테스트 통과를 위해 계획 외 수정이 필요한 경우

### 사용 예시

```bash
/implement-plan docs/plan/feature-x.md
```

---

## Plan Review Skill 상세

구현 계획 문서를 6가지 관점으로 순차 리뷰하고, 수동 텍스트 승인 루프 기반으로 즉시 문서에 반영하는 인터랙티브 리뷰 스킬입니다.

### 트리거 및 입력

- 호출: `/plan-review {plan-file-path}`
- 승인 입력은 `승인`, `승인 안 함`, `수정 지시: ...`만 허용합니다.
- 관점 6 질의는 `선택: <번호|선택지>` 형식으로 질문 1개씩 순차 처리합니다.

### 6개 리뷰 관점

1. 문서 정합성(프로젝트 문서와 충돌/누락 점검)
2. 웹 검증(기술 주장 최신성/정확성 검증)
3. 코드 실현 가능성(현재 코드베이스 기준 구현 가능성)
4. 테스트 계획 현실성/커버리지
5. 계획 품질(7개 차원 점수화)
6. 불확실성/애매성 질의(닫힌형 질문 + 권장안)

### 루프 규칙

- 관점별 제안이 없으면 `PASS_NO_ACTION`으로 자동 진행
- 반영 변경이 1건 이상이면 문서 갱신본 기준으로 다음 iteration 재실행
- 권장 `max_iterations = 3`

---

## Git Master Skill 상세

Git 작업을 `COMMIT/REBASE/HISTORY_SEARCH` 모드로 자동화하는 워크플로우 스킬입니다.

### 모드

- `COMMIT`: 변경을 논리 단위로 분리해 원자 커밋 생성
- `REBASE`: 히스토리 정리 전략(squash/reword/reorder/fixup) 제안 후 실행
- `HISTORY_SEARCH`: 파일/키워드/라인 기준 변경 이력 추적

### 핵심 규칙

- 커밋 전 파일을 실제로 읽고 기능 단위로 그룹화합니다.
- `git add .`/`git add -A` 대신 그룹별 명시 add를 사용합니다.
- 프로젝트 커밋 컨벤션(`AGENTS.md`)이 있으면 우선 적용합니다.
- `rebase`는 파괴적 작업으로 사용자 승인 후 실행합니다.

### 사용 예시

```bash
git-master
git-master commit
git-master rebase
git-master search 함수명
```

---

## Obsidian CLI Skill 상세

Obsidian CLI 명령어를 빠르게 찾아 실행할 수 있도록 정리한 레퍼런스 스킬입니다.

### 적용 조건

- Obsidian 1.12+ (Early Access) 환경
- `obsidian` 명령 기반 자동화가 필요한 경우
- 볼트/노트 조작, 검색, 플러그인/테마 관리, 개발자 도구 활용 시

### 커버 범위

- 파일/폴더/데일리 노트/검색/태그/작업/속성/링크
- 플러그인/템플릿/히스토리/Sync/Publish/워크스페이스
- 개발자 도구(`dev:console`, `dev:screenshot`, `eval`, `dev:dom`)
- 파라미터 규칙: `key=value`, 플래그, `file=` vs `path=` 타겟팅

### 사용 예시

```bash
obsidian search query="meeting notes" matches
obsidian daily:append content="- [ ] release checklist" silent
obsidian plugin:reload id=my-plugin
```

---

## GH CLI Skill 상세

GitHub CLI(`gh`)를 커맨드라인에서 사용할 때 필요한 명령 체계를 폭넓게 참조하는 레퍼런스 스킬입니다.

### 적용 조건

- GitHub 리포지토리/이슈/PR/Actions/릴리즈 운영 자동화 시
- `gh api`/`--json`/`--jq` 기반 스크립팅 시
- GitHub Enterprise hostname/토큰/권한 스코프 관리가 필요한 경우

### 커버 범위

- 핵심 명령군: `repo`, `issue`, `pr`, `run`, `workflow`, `project`, `release`, `gist`, `codespace`, `org`
- 인증/설정: `gh auth`, `gh config`, 환경변수(`GH_TOKEN`, `GH_HOST`, `GH_REPO`)
- 자동화: pagination, JSON 파싱(`--jq`), alias/extension, API/GraphQL 호출
- 운영 시나리오: PR 생성, CI 감시, 포크 동기화, 릴리즈 배포

### 사용 예시

```bash
/gh-cli
gh pr list
gh pr checks 123 --watch
gh run view --log-failed
```

---

## Ship Skill 상세

변경사항을 이슈/브랜치/커밋/검증/push/PR/CI 복구 루프까지 한 번에 진행하는 자동화 스킬입니다.

### 트리거 및 입력

- `ship`: 변경사항 분석 후 이슈 생성부터 시작
- `ship {문서경로}`: 계획 문서 기반으로 이슈 번호 재사용/생성 분기
- 프로젝트 컨벤션 문서(`ISSUE/BRANCH/COMMIT/PR`)를 우선 준수

### 핵심 절차

1. 변경사항 분석 후 이슈/브랜치를 준비합니다.
2. `git-master`를 이용해 원자적 커밋을 생성합니다.
3. `docs/plan/` 이슈 문서가 있으면 별도 docs 커밋으로 분리합니다.
4. push 전 도메인 스킬 리뷰와 CI/문서 동기화 체크를 수행합니다.
5. PR 생성 후 GitHub Actions만 폴링하고 실패 시 복구 루프를 실행합니다.

### 산출물

- 이슈/브랜치/커밋/PR 링크
- push 전 검증/리뷰 로그
- CI 폴링 횟수 및 실패 복구 이력

### 사용 예시

```bash
ship
ship docs/plan/ISSUE_123_feature.md
```

---

## PR Merge Conflict Skill 상세

PR URL을 받아 merge conflict 여부를 확인하고, 충돌이 없으면 종료합니다. 충돌이 있으면 충돌 파일을 기준으로 원인 커밋을 추적해 어떤 PR/브랜치에서 유입된 변경인지 식별한 뒤, 양쪽(이번 PR + 충돌 원인 PR/이슈)의 plans(또는 docs/plan) 문서를 찾아 의도한 구현을 모두 보존하는 형태로 충돌을 해결하고 commit+push 합니다.

### 트리거 및 입력

- 호출: `/pr-merge-conflict {pr-url}`
- URL 형식: `https://github.com/{owner}/{repo}/pull/{number}`
- 현재 브랜치가 PR head branch와 일치해야 진행됩니다.

### 핵심 절차

1. `mergeable` 상태를 확인해 충돌이 없으면 즉시 종료합니다.
2. `git merge --no-commit`과 `merge-base` 기반으로 충돌 파일/원인 커밋을 추적합니다.
3. `/commits/{sha}/pulls` 조회로 원인 PR 후보를 식별합니다.
4. PR0/PRx의 `plans/` 또는 `docs/plan/` 문서를 찾아 의도를 병합합니다.
5. 최소 수정으로 해결 후 commit/push 하고 mergeable 상태를 재확인합니다.

### 보호 규칙

- 한쪽 구현을 임의 삭제하는 해결 금지
- 충돌 해결과 무관한 대규모 리팩토링 금지
- force push는 사용자 확인 및 rebase 선택 상황에서만 허용

### 사용 예시

```bash
/pr-merge-conflict https://github.com/org/repo/pull/123
```

---

## PR CI Loop Skill 상세

PR URL을 기준으로 현재 브랜치가 PR head branch와 일치하는지 검증한 뒤, GitHub Actions CI 실패를 분석/수정 커밋/푸시하고 성공까지 폴링으로 확인하는 작업형 스킬입니다.

### 트리거 및 입력

- 호출: `/pr-ci-loop {pr-url}`
- URL 형식: `https://github.com/{owner}/{repo}/pull/{number}`
- PR head branch 불일치 시 즉시 중단합니다.

### 핵심 절차

1. PR 파싱 후 현재 저장소/브랜치/sha 일치 여부를 검증합니다.
2. GitHub Actions run만 폴링합니다(코드리뷰 체크 제외).
3. 실패 run에서 `gh run view --log-failed`로 원인을 추출합니다.
4. 최소 수정 후 commit/push 하고 다시 폴링 루프로 복귀합니다.
5. 전부 `success/skipped/neutral`이 되면 종료합니다.

### 중단 조건

- 동일 실패 패턴 2회 이상 반복
- 권한/시크릿/외부 장애로 자동 수정 불가
- workflow 자체 미설정/조회 불가 상태 지속

### 사용 예시

```bash
/pr-ci-loop https://github.com/org/repo/pull/123
```

---

## SQLite Skill 상세

TypeORM/Prisma 등 ORM 사용 시 알아야 할 SQLite 특성을 정리한 가이드입니다.

### 적용 조건

- `.db`, `.sqlite` 파일 작업 시
- TypeORM/Prisma 등 ORM으로 SQLite를 운영/마이그레이션할 때
- 락/동시성/성능/백업 이슈 점검이 필요할 때

### 핵심 체크리스트

- 필수 PRAGMA: `journal_mode=WAL`, `foreign_keys=ON`, `busy_timeout` 설정
- Quirks: 유연한 타입, BOOLEAN/DATETIME 부재, NULL/PK/UNIQUE 특성
- 마이그레이션 제한: `ALTER TABLE` 범위, 타입 변경 시 테이블 재생성 패턴
- 동시성/락킹: `SQLITE_BUSY` 대응, WAL 장단점, 스레드 모드
- 성능: 인덱스 조건, `ANALYZE`, `EXPLAIN QUERY PLAN`
- ORM 연동: TypeORM `synchronize:false`, `better-sqlite3` PRAGMA 초기화
- 고급 항목: In-Memory DB, Generated Columns, AUTOINCREMENT 전략

### 참조 문서

| 주제 | 링크 |
|------|------|
| Quirks (함정) | https://www.sqlite.org/quirks.html |
| Pragmas (설정) | https://www.sqlite.org/pragma.html |
| ALTER TABLE | https://www.sqlite.org/lang_altertable.html |
| WAL Mode | https://www.sqlite.org/wal.html |
| Locking | https://www.sqlite.org/lockingv3.html |
| Limits | https://www.sqlite.org/limits.html |
| Query Optimizer | https://www.sqlite.org/optoverview.html |

---

## Vercel React Best Practices Skill 상세

Vercel Engineering에서 제공하는 React/Next.js 성능 최적화 가이드입니다.

### 적용 조건

- React 컴포넌트/Next.js 페이지 작성 또는 리팩토링 시
- 클라이언트/서버 데이터 패칭 병목(waterfall) 제거가 필요할 때
- 번들 크기 및 렌더링 성능 최적화 리뷰 시

### 규칙 카테고리 (우선순위)

| 우선순위 | 카테고리 | 영향도 |
|----------|----------|--------|
| 1 | Eliminating Waterfalls | CRITICAL |
| 2 | Bundle Size Optimization | CRITICAL |
| 3 | Server-Side Performance | HIGH |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH |
| 5 | Re-render Optimization | MEDIUM |
| 6 | Rendering Performance | MEDIUM |
| 7 | JavaScript Performance | LOW-MEDIUM |
| 8 | Advanced Patterns | LOW |

### 활용 포인트

- 규칙 파일 prefix(`async-`, `bundle-`, `server-`, `client-`...)로 빠른 탐색
- 각 규칙 파일에서 anti-pattern vs 권장 코드 예시를 바로 비교
- 전체 통합 문서는 `vercel-react-best-practices/AGENTS.md` 참고

---

## Web Design Guidelines Skill 상세

UI 코드를 Web Interface Guidelines에 따라 리뷰하는 skill입니다.

### 동작 방식

1. 매 리뷰마다 최신 가이드라인 원문을 먼저 fetch
2. 지정 파일(또는 패턴)을 읽고 전체 규칙을 적용
3. 결과를 `file:line` 중심의 terse 포맷으로 출력

### 가이드 소스

- `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`

### 사용 예시

```bash
/web-design-guidelines src/components/**/*.tsx
```

---

## GitHub GraphQL Skill 상세

GitHub GraphQL API를 사용한 데이터 조회를 위한 가이드입니다.

### 적용 조건

- GitHub API/GraphQL 쿼리 작성 및 검증 시
- `contributionsCollection`/페이지네이션/rate limit 최적화가 필요할 때
- REST ↔ GraphQL ID 연동이 필요한 작업

### 핵심 내용

- 엔드포인트: `POST https://api.github.com/graphql`
- 인증: `Authorization: Bearer {TOKEN}`
- Rate limit: PAT 기준 시간당 5,000 포인트
- 주요 패턴: contributions 조회, `rateLimit` 쿼리, cursor pagination

### 포함 문서

| 문서 | 설명 |
|------|------|
| GraphQL 소개 | 기본 개념, 스키마, 필드 |
| 호출 형성 | 인증, 쿼리 작성법 |
| Rate Limits | 속도 제한, 최적화 |
| 쿼리 참조 | 루트 쿼리 목록 |
| User/ContributionsCollection | 사용자 기여 데이터 |
| 페이지네이션 | 커서 기반 페이징 |
| 전역 노드 ID | REST-GraphQL ID 연동 |

---

## TanStack Query Skill 상세

TanStack Query (React Query) v5 공식 문서 기반 개발 레퍼런스입니다. 72개의 문서를 포함합니다.

### 적용 조건

- `@tanstack/react-query` 훅(`useQuery`, `useMutation`, `useInfiniteQuery`) 사용 시
- 캐싱/무효화/낙관적 업데이트/SSR/Suspense 설계 시
- v5 마이그레이션 체크가 필요한 리팩토링 시

### 핵심 패턴

- Query key 설계와 invalidate 범위 관리
- mutation 라이프사이클 기반 optimistic update/rollback
- dependent query, prefetch, infinite query, suspense 통합
- v5 변경점(`cacheTime -> gcTime`, loading 상태명 변경) 점검

### 문서 카테고리

| 카테고리 | 문서 수 | 주요 내용 |
|----------|--------|----------|
| 루트 | 8개 | Overview, Quick Start, Installation, TypeScript 등 |
| Guides | 35개 | Queries, Mutations, Caching, Invalidation, SSR, Suspense 등 |
| Reference | 20개 | useQuery, useMutation, useInfiniteQuery, useSuspenseQuery 등 |
| Core Reference | 9개 | QueryClient, QueryCache, MutationCache 등 |

### 주요 가이드

| 가이드 | 설명 |
|--------|------|
| queries.md | Query 기초 |
| mutations.md | Mutation 기초 |
| caching.md | 캐싱 전략 |
| query-invalidation.md | 캐시 무효화 |
| optimistic-updates.md | 낙관적 업데이트 |
| infinite-queries.md | 무한 스크롤 |
| suspense.md | React Suspense 통합 |
| ssr.md, advanced-ssr.md | 서버 사이드 렌더링 |
| testing.md | 테스트 작성 |

### 구조

```
tanstack-query/
├── SKILL.md           # 요약 및 핵심 패턴
└── docs/              # 72개의 상세 문서
    ├── overview.md
    ├── quick-start.md
    ├── guides/        # 35개 가이드
    ├── reference/     # 20개 React Hook API
    └── core-reference/ # 9개 Core API
```

---

## NestJS Skill 상세

NestJS 공식 문서 기반 개발 레퍼런스입니다. 133개의 문서를 포함합니다.

### 적용 조건

- NestJS 프로젝트(`@nestjs/*`) 코드 작성/리뷰 시
- `.controller.ts`, `.service.ts`, `.module.ts`, `.guard.ts`, `.pipe.ts`, `.interceptor.ts` 작업 시
- GraphQL/WebSocket/Microservice/OpenAPI 구현 시

### 핵심 패턴

- 요청 처리 체인: `Middleware -> Guards -> Interceptors(pre) -> Pipes -> Controller -> Interceptors(post) -> ExceptionFilter`
- 모듈 경계(Imports/Providers/Exports)와 DI 중심 설계
- DTO + `ValidationPipe` 기반 입력 검증
- 가드/인터셉터/필터의 역할 분리

### 문서 카테고리

| 카테고리 | 문서 수 | 주요 내용 |
|----------|--------|----------|
| Overview | 11개 | Controllers, Providers, Modules, Guards, Pipes 등 |
| Fundamentals | 12개 | DI, Dynamic Modules, Lifecycle, Testing 등 |
| Techniques | 20개 | Configuration, Database, Validation, Caching 등 |
| Security | 7개 | Authentication, Authorization, CORS 등 |
| GraphQL | 18개 | Resolvers, Mutations, Subscriptions, Federation 등 |
| WebSockets | 6개 | Gateways, Adapters 등 |
| Microservices | 12개 | Redis, Kafka, RabbitMQ, gRPC 등 |
| OpenAPI | 8개 | Swagger 문서화 |
| CLI | 5개 | 프로젝트 생성, 워크스페이스 |
| Recipes | 20개 | TypeORM, Prisma, Passport, Hot Reload 등 |
| FAQ | 9개 | 일반적인 오류, 서버리스 등 |
| 기타 | 8개 | 배포, 마이그레이션, Devtools |

### 구조

```
nestjs/
├── SKILL.md           # 요약 및 핵심 패턴
└── docs/              # 133개의 상세 문서
    ├── controllers.md
    ├── fundamentals/
    ├── techniques/
    ├── security/
    ├── graphql/
    └── ...
```
