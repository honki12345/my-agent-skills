# Claude Code Skills

개인 Claude Code skills 모음

## 설치된 Skills

| Skill | 설명 | 트리거 | 생성일 |
|-------|------|--------|--------|
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

