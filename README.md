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

---

## Issue Worktree Plan Skill 상세

GitHub 이슈 URL 하나로 작업용 worktree 브랜치와 계획 문서를 동시에 초기화하는 작업형 스킬입니다.

### 주요 내용

- GitHub issue URL 파싱 및 이슈 메타데이터(`gh issue view`) 확인
- 프로젝트에 브랜치 네이밍 컨벤션이 있으면 우선 준수하고, 없으면 기본 패턴(`issue-{번호}-{slug}`) 사용
- 브랜치명에는 `#` 문자를 포함하지 않으며, 이슈 번호는 `issue-{번호}` 패턴으로만 표현
- 기본 브랜치 기준 `git worktree add`로 분리 작업 디렉토리 생성
- `docs/plan/ISSUE_{번호}_{slug}.md` 규칙으로 계획 문서 생성
- 브랜치/워크트리/문서 충돌 시 덮어쓰기 없이 사용자 확인 게이트 적용

### 사용 예시

```
/issue-worktree-plan https://github.com/org/repo/issues/123
```

---

## Codebase Doc Writer Skill 상세

저장소 구현을 직접 읽고 근거 기반 기술 문서를 만드는 작업형 스킬입니다.

### 주요 내용

- 코드/설정/워크플로우를 기준으로 문서 구조를 설계
- 섹션별 `Sources` 근거 경로를 남겨 추적 가능성 유지
- 과도한 추정 없이 미확정 영역을 명시적으로 표시

### 사용 예시

```
/codebase-doc-writer
```

---

## Branch Doc Sync Skill 상세

현재 브랜치의 변경사항을 기준으로 프로젝트의 관리 문서를 전수 점검하고, 문서별 영향 판정을 거쳐 필요한 문서를 직접 수정하는 스킬입니다.

### 주요 내용

- `git diff <base>...HEAD` 기반 변경 파일 수집
- `git ls-files` 기반 관리 문서 목록 전수 수집(확장자/경로 규칙)
- 모든 관리 문서를 `update/no-change`로 하나씩 판정하고, 누락 문서는 `add` 후보로 분류
- 경로/영역 기준 문서 영향 매핑 + 대상 문서 직접 수정 + 근거(`Sources`)와 변경 요약 정리
- 명령/환경변수/링크 검증까지 포함한 문서 동기화 루프 수행

### 사용 예시

```
/branch-doc-sync
```

---

## GH Review Triage Skill 상세

PR 링크를 입력받아 리뷰 코멘트의 반영 여부를 판단하고 실행 가능한 액션으로 정리하는 작업형 스킬입니다.

### 주요 내용

- `gh` CLI로 인라인 코멘트/리뷰 코멘트/일반 코멘트를 모두 수집
- 코멘트별 초안 판정을 만든 뒤 수동 텍스트 승인 루프로 순차 확정
- `반영` 항목은 수정 대상, 변경 방향, 검증 방법까지 필수 제시
- 인자가 없으면 현재 브랜치에 연결된 PR을 `gh pr view`로 자동 탐지 후 진행
- 실제 반영이 수행되면 마지막에 계획 문서의 변경분까지 동기화
- 충돌 코멘트/범위 초과 리팩토링 필요 시 동일 수동 승인 게이트 적용

### 사용 예시

```
/gh-review-triage
/gh-review-triage https://github.com/org/repo/pull/123
```

---

## Debug Loop Skill 상세

버그 상황에서 재현을 최우선으로 두고, 가설 검증 루프를 반복해 원인을 좁히는 디버깅 스킬입니다.

### 주요 내용

- 재현 성공 전 임의 수정 금지
- git 변경 이력 + 로그 + 프로젝트 문서 기반 가설 수립
- `가설 -> 최소 수정/로깅 -> 재현 테스트` 반복
- 방향 전환/대규모 변경 필요 시 승인 게이트 적용
- 마무리 단계에서 인자로 받은 문서와 `AGENTS.md` 기반 문서 후보의 업데이트 필요 여부 점검

### 사용 예시

```bash
/debug-loop "로그인 시 500 에러" "logs/server.log" "docs/plan/auth-hotfix.md"
```

---

## Implement Plan Skill 상세

계획 문서를 기준으로 구현을 수행하고, 계획 이탈 시 승인 절차를 강제하는 구현 스킬입니다.

### 주요 내용

- 계획 문서의 목표/범위/제약 내에서만 구현
- 모순/불확실/계획 외 변경 필요 시 즉시 승인 요청
- 계획 문서에 테스트 항목이 있으면 전체 통과까지 반복 시도
- 결과 보고 시 계획 대비 완료 항목과 남은 리스크를 명시

### 사용 예시

```
/implement-plan docs/plan/feature-x.md
```

---

## Plan Review Skill 상세

구현 계획 문서를 6가지 관점으로 순차 리뷰하고, 수동 텍스트 승인 루프 기반으로 즉시 문서에 반영하는 인터랙티브 리뷰 스킬입니다.

### 주요 내용

- 관점별 요약 후 수동 텍스트로 `승인/승인 안 함/수정 지시: ...` 선택
- 승인 요청 시 항상 권장안과 권장 이유를 함께 제시
- 관점별 제안이 없으면 자동 `PASS_NO_ACTION` 처리
- `Other(다른 지시)` 또는 `수정 지시: ...` 입력 시 수정안 재제시 후 재승인
- 6개 관점 완료 후 승인 반영 변경이 있으면 다음 iteration 반복
- 테스트 계획의 현실성/커버리지를 별도 관점으로 강제 점검
- 불확실성/애매성 관점은 Summary 후 질문을 1개씩 제시하고, 각 질문에 권장 선택/이유를 함께 제공한 뒤 `선택: ...`으로 순차 확정
- 문서 정합성/코드 실현 가능성 분석 시 위치와 무관한 프로젝트 구조 문서(예: `AGENTS.md`, `README.md`, `docs/`, `plans/`)가 있으면 함께 대조

---

## Git Master Skill 상세

Git 작업을 `COMMIT/REBASE/HISTORY_SEARCH` 모드로 자동화하는 워크플로우 스킬입니다.

### 주요 내용

- 변경사항을 논리 단위로 분리해 원자적 커밋 생성
- rebase 전략(squash/reword/reorder/fixup) 제안
- 함수/파일/라인 기준 변경 이력 추적 지원
- 프로젝트별 커밋 컨벤션이 있으면 우선 적용

### 사용 예시

```
git-master
git-master commit
git-master rebase
git-master search 함수명
```

---

## Obsidian CLI Skill 상세

Obsidian CLI 명령어를 빠르게 찾아 실행할 수 있도록 정리한 레퍼런스 스킬입니다.

### 주요 내용

- 파일/폴더/검색/태그/작업/속성 조작 명령 정리
- 플러그인/템플릿/히스토리/Sync/Publish 명령 포함
- 볼트 타겟팅(`vault=`, `file=`, `path=`) 패턴 가이드 제공
- TUI 모드/파라미터/플래그 사용법 포함

---

## GH CLI Skill 상세

GitHub CLI(`gh`)를 커맨드라인에서 사용할 때 필요한 명령 체계를 폭넓게 참조하는 레퍼런스 스킬입니다.

### 주요 내용

- `repo`/`issue`/`pr`/`run`/`workflow`/`project`/`release`/`gist`/`codespace`/`org` 명령군 정리
- `gh auth` 기반 인증/계정 전환/토큰/권한 스코프 관리 절차 포함
- `gh config` 및 주요 환경변수(`GH_TOKEN`, `GH_HOST`, `GH_REPO` 등) 사용 패턴 제공
- `gh api`, `search`, `extension` 등 고급 명령과 자동화 활용 시나리오 커버

### 사용 예시

```bash
/gh-cli
gh pr list
gh run view --log-failed
```

---

## Ship Skill 상세

변경사항을 이슈/브랜치/커밋/검증/push/PR/CI 복구 루프까지 한 번에 진행하는 자동화 스킬입니다.

### 주요 내용

- `ship` 또는 `ship {문서경로}`로 이슈 생성/재사용 분기
- 브랜치 생성 및 원자적 커밋(`git-master` COMMIT 절차 사용)
- push 전 필수 체크리스트(CI/문서 동기화/도메인 스킬 검토)
- PR 생성 후 GitHub Actions CI 상태만 주기적으로 폴링하고 실패 시 run 로그 기반 분석 수행
- 실패 원인 수정 커밋/push 후 CI 재확인 루프를 반복
- 최종 결과에 이슈/브랜치/커밋/PR, 리뷰/검증 결과, CI 폴링/복구 이력을 함께 요약

### 사용 예시

```
ship
ship docs/plan/ISSUE_123_feature.md
```

---

## PR Merge Conflict Skill 상세

PR URL을 받아 merge conflict 여부를 확인하고, 충돌이 없으면 종료합니다. 충돌이 있으면 충돌 파일을 기준으로 원인 커밋을 추적해 어떤 PR/브랜치에서 유입된 변경인지 식별한 뒤, 양쪽(이번 PR + 충돌 원인 PR/이슈)의 plans(또는 docs/plan) 문서를 찾아 의도한 구현을 모두 보존하는 형태로 충돌을 해결하고 commit+push 합니다.

### 주요 내용

- PR mergeable 상태(`mergeable`) 확인: 충돌 없으면 즉시 종료
- `git merge --no-commit`로 충돌 파일 목록 수집 및 `merge-base` 기준 양쪽 커밋 후보 추적
- `gh api .../commits/{sha}/pulls`로 충돌 원인 커밋 ↔ PR 매핑 (가능한 경우)
- 각 PR/이슈의 `plans/` 또는 `docs/plan/` 문서 탐색 후 요구사항 병합
- 충돌 해결 구현 후 commit/push, PR이 다시 mergeable 해질 때까지 재확인

### 사용 예시

```
/pr-merge-conflict https://github.com/org/repo/pull/123
```

---

## PR CI Loop Skill 상세

PR URL을 기준으로 현재 브랜치가 PR head branch와 일치하는지 검증한 뒤, GitHub Actions CI 실패를 분석/수정 커밋/푸시하고 성공까지 폴링으로 확인하는 작업형 스킬입니다.

### 주요 내용

- PR URL 파싱 및 저장소/PR 번호 식별
- 현재 브랜치 == PR head branch 불일치 시 즉시 실패
- GitHub Actions run만 대상으로 CI 상태 폴링 (CodeRabbit/Copilot 등 코드리뷰 체크 제외)
- 실패 run 로그(`gh run view --log-failed`) 기반 원인 분석 및 최소 수정
- 수정 커밋/push 후 CI 재확인 루프 반복
- 동일 실패 반복/권한/시크릿/외부 장애 등 자동 수정 불가 시 중단 후 보고

### 사용 예시

```
/pr-ci-loop https://github.com/org/repo/pull/123
```

---

## SQLite Skill 상세

TypeORM/Prisma 등 ORM 사용 시 알아야 할 SQLite 특성을 정리한 가이드입니다.

### 주요 내용

- **필수 초기 설정**: WAL 모드, Foreign Key 활성화
- **핵심 Quirks**: FK 기본 비활성화, 유연한 타입, NULL PK 허용
- **마이그레이션 제한**: ALTER TABLE 제한사항, 컬럼 타입 변경 불가
- **동시성 & 락킹**: 5가지 락 상태, BUSY 에러 해결, WAL 모드
- **제한사항**: DB 크기, 컬럼 수, JOIN 테이블 수
- **백업**: 안전한 백업 방법
- **인덱스 최적화**: 복합 인덱스, ANALYZE, EXPLAIN
- **TypeORM 연동**: DataSource 설정, 날짜 타입 주의

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

## Vercel React Best Practices 상세

Vercel Engineering에서 제공하는 React/Next.js 성능 최적화 가이드입니다.

### 규칙 카테고리 (우선순위순)

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

---

## Web Design Guidelines 상세

UI 코드를 Web Interface Guidelines에 따라 리뷰하는 skill입니다.

### 사용법

```
/web-design-guidelines <파일 또는 패턴>
```

### 체크 항목

- 접근성 (Accessibility)
- UX 패턴
- 웹 인터페이스 가이드라인 준수

---

## GitHub GraphQL Skill 상세

GitHub GraphQL API를 사용한 데이터 조회를 위한 가이드입니다.

### 주요 내용

- **기본 개념**: 스키마, 필드, Connection, Edge, Node
- **인증 및 호출**: Bearer 토큰, 쿼리/뮤테이션 작성법
- **Rate Limit**: 시간당 5,000 포인트, 헤더 확인, 최적화 전략
- **주요 쿼리**: user, repository, viewer, rateLimit
- **ContributionsCollection**: 사용자 기여 데이터 조회
- **페이지네이션**: 커서 기반 페이지 매김
- **전역 노드 ID**: REST ↔ GraphQL 간 ID 활용

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
