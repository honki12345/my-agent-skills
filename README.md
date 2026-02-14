# Claude Code Skills

개인 Claude Code skills 모음

## 설치된 Skills

| Skill | 설명 | 트리거 | 생성일 |
|-------|------|--------|--------|
| `plan-review` | 구현 계획 문서 4관점 병렬 리뷰 (문서 정합성, 웹 검증, 코드 실현 가능성, 계획 품질) | `/plan-review` 수동 호출 | 2026-02-14 |
| `git-master` | Git 원자적 커밋 분리, 히스토리 정리, 변경 추적 | `/git-master` 수동 호출 | 2026-02-14 |
| `obsidian-cli` | Obsidian CLI 명령어 레퍼런스 | obsidian 명령어, 볼트 관리, 플러그인 관리 작업 시 | 2026-02-12 |
| `tanstack-query` | TanStack Query (React Query) v5 가이드 (72개 문서) | @tanstack/react-query 패키지 사용 시 | 2026-01-31 |
| `github-graphql` | GitHub GraphQL API 가이드 (7개 문서) | GitHub API, GraphQL, contributionsCollection 키워드 | 2026-01-25 |
| `nestjs` | NestJS 프레임워크 가이드 (133개 문서) | NestJS 프로젝트, @nestjs 패키지 사용 시 | 2026-01-24 |
| `sqlite` | SQLite 데이터베이스 가이드 | .db/.sqlite 파일 작업, ORM 사용 시 | 2026-01-24 |
| `vercel-react-best-practices` | React/Next.js 성능 최적화 (45개 규칙) | React/Next.js 코드 작성/리뷰 시 | 2026-01-24 |
| `web-design-guidelines` | UI 코드 접근성/UX 리뷰 | UI 리뷰 요청 시 | 2026-01-24 |

## 사용법

이 디렉토리의 skills는 모든 프로젝트에서 자동으로 사용 가능합니다.

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

