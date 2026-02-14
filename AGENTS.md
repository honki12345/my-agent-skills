# Claude Code Skills Repository

개인 Claude Code skills 저장소

> 공식 문서: https://code.claude.com/docs/en/skills

## 커밋 컨벤션

### 커밋 타입

| 타입 | 설명 |
|------|------|
| feat | 새로운 skill 추가 |
| fix | skill 버그 수정 |
| docs | 문서 수정 (README 등) |
| refactor | skill 구조 개선 |
| chore | 기타 작업 |

### 커밋 메시지 형식

```
{타입}: {설명}
```

**설명은 한글로 작성합니다.**

### 예시

- `feat: SQLite skill 추가`
- `fix: React 성능 규칙 오타 수정`
- `docs: README 업데이트`

---

## Skill 생성 이력

| 날짜 | Skill | 설명 |
|------|-------|------|
| 2026-02-14 | `plan-review` | 구현 계획 문서 4가지 관점 병렬 리뷰 (문서 정합성, 웹 검증, 코드 실현 가능성, 계획 품질) |
| 2026-02-14 | `git-master` | Git 워크플로우 자동화 (원자적 커밋, 히스토리 정리, 변경 추적) |
| 2026-02-12 | `obsidian-cli` | Obsidian CLI 명령어 레퍼런스 |
| 2026-01-31 | `tanstack-query` | TanStack Query (React Query) v5 가이드 (72개 공식 문서) |
| 2026-01-30 | `ship` | 변경사항 커밋 및 푸시 자동화 (수동 호출) |
| 2026-01-25 | `github-graphql` | GitHub GraphQL API 가이드 (7개 공식 문서) |
| 2026-01-24 | `nestjs` | NestJS 프레임워크 가이드 (133개 공식 문서) |
| 2026-01-24 | `sqlite` | SQLite ORM 사용자 가이드 |
| 2026-01-24 | `vercel-react-best-practices` | Vercel React/Next.js 성능 최적화 |
| 2026-01-24 | `web-design-guidelines` | Web Interface Guidelines UI 리뷰 |

---

## Skill 저장 위치

| 위치 | 경로 | 적용 범위 |
|------|------|----------|
| Enterprise | managed settings | 조직 전체 |
| **Personal** | `~/.claude/skills/<skill-name>/SKILL.md` | 모든 프로젝트 |
| Project | `.claude/skills/<skill-name>/SKILL.md` | 해당 프로젝트만 |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | 플러그인 활성화된 곳 |

> 같은 이름의 skill이 여러 위치에 있으면: Enterprise > Personal > Project 순으로 우선

---

## 디렉토리 구조

```
~/.claude/skills/
├── AGENTS.md               # 이 파일 (컨벤션 및 이력)
├── README.md               # Skills 목록 및 상세 설명
├── git-master/
│   └── SKILL.md            # Git 원자적 커밋/히스토리 정리
├── plan-review/
│   └── SKILL.md            # 계획 문서 4관점 병렬 리뷰
├── obsidian-cli/
│   └── SKILL.md            # Obsidian CLI 명령어 레퍼런스
├── nestjs/
│   ├── SKILL.md            # NestJS skill (요약)
│   └── docs/               # 133개의 공식 문서
├── sqlite/
│   └── SKILL.md            # SQLite skill (필수)
├── tanstack-query/
│   ├── SKILL.md            # TanStack Query skill (요약)
│   └── docs/               # 72개의 공식 문서
├── vercel-react-best-practices/
│   └── SKILL.md            # React/Next.js 성능 skill
└── web-design-guidelines/
    └── SKILL.md            # UI 리뷰 skill
```

### 지원 파일 포함 시

```
my-skill/
├── SKILL.md                # 메인 지침 (필수)
├── template.md             # Claude가 채울 템플릿
├── examples/
│   └── sample.md           # 예상 출력 예시
└── scripts/
    └── validate.sh         # Claude가 실행할 스크립트
```

> **Tip:** SKILL.md는 500줄 이하로 유지. 상세 참조는 별도 파일로 분리.

---

## Skill 생성 가이드

### 1. 디렉토리 생성

```bash
mkdir -p ~/.claude/skills/{skill-name}
```

### 2. SKILL.md 작성

```yaml
---
name: skill-name
description: Skill 설명. Claude가 자동 로드 여부를 결정할 때 사용.
---

# Skill 지침

여기에 Claude가 따를 지침을 작성합니다.
```

### 3. README.md 및 AGENTS.md 업데이트

- README.md의 "설치된 Skills" 테이블에 추가
- AGENTS.md의 "Skill 생성 이력" 테이블에 추가

### 4. 커밋 및 push

```bash
cd ~/.claude/skills
git add -A
git commit -m "feat: {skill-name} skill 추가"
git push
```

---

## YAML Frontmatter 필드

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | 아니오 | Skill 이름. 생략 시 디렉토리명 사용. 소문자, 숫자, 하이픈만 (최대 64자) |
| `description` | **권장** | Skill 설명. Claude가 자동 로드 여부 결정에 사용 |
| `argument-hint` | 아니오 | 자동완성 시 표시할 힌트. 예: `[issue-number]`, `[filename] [format]` |
| `disable-model-invocation` | 아니오 | `true`: Claude 자동 로드 차단 (수동 `/name` 호출만 허용) |
| `user-invocable` | 아니오 | `false`: `/` 메뉴에서 숨김 (사용자 직접 호출 불가) |
| `allowed-tools` | 아니오 | 권한 요청 없이 사용 가능한 도구. 예: `Read, Grep, Glob` |
| `model` | 아니오 | Skill 활성 시 사용할 모델 |
| `context` | 아니오 | `fork`: 격리된 subagent 컨텍스트에서 실행 |
| `agent` | 아니오 | `context: fork` 시 사용할 subagent 타입 (`Explore`, `Plan`, `general-purpose`) |
| `hooks` | 아니오 | Skill 라이프사이클에 범위 지정된 hooks |

### 문자열 치환

| 변수 | 설명 |
|------|------|
| `$ARGUMENTS` | Skill 호출 시 전달된 인자. 없으면 끝에 `ARGUMENTS: <value>` 추가됨 |
| `${CLAUDE_SESSION_ID}` | 현재 세션 ID |

---

## Skill 유형

### 참조 콘텐츠 (Reference)

코드 작성 시 적용할 지식: 컨벤션, 패턴, 스타일 가이드, 도메인 지식

```yaml
---
name: api-conventions
description: 이 코드베이스의 API 설계 패턴
---

API 엔드포인트 작성 시:
- RESTful 네이밍 컨벤션 사용
- 일관된 에러 형식 반환
- 요청 검증 포함
```

### 작업 콘텐츠 (Task)

특정 작업을 위한 단계별 지침: 배포, 커밋, 코드 생성

```yaml
---
name: deploy
description: 프로덕션 배포
context: fork
disable-model-invocation: true
---

애플리케이션 배포:
1. 테스트 스위트 실행
2. 애플리케이션 빌드
3. 배포 대상으로 push
```

> **Tip:** 부작용이 있는 작업은 `disable-model-invocation: true` 설정

---

## 호출 제어

| Frontmatter | 사용자 호출 | Claude 호출 | 컨텍스트 로드 |
|-------------|------------|-------------|--------------|
| (기본값) | O | O | description 항상 로드, 호출 시 전체 로드 |
| `disable-model-invocation: true` | O | X | 컨텍스트에 포함 안 됨 |
| `user-invocable: false` | X | O | description 항상 로드, 호출 시 전체 로드 |

### 사용 예시

- **배포, 커밋 등 부작용 있는 작업**: `disable-model-invocation: true`
- **배경 지식 (사용자가 직접 호출할 필요 없음)**: `user-invocable: false`

---

## 고급 패턴

### 동적 컨텍스트 주입

`!`command`` 문법으로 셸 명령 실행 후 결과를 주입:

```yaml
---
name: pr-summary
description: PR 변경사항 요약
context: fork
agent: Explore
---

## PR 컨텍스트
- PR diff: !`gh pr diff`
- PR 코멘트: !`gh pr view --comments`

## 작업
이 PR을 요약...
```

### Subagent에서 실행

`context: fork` 추가 시 격리된 환경에서 실행:

```yaml
---
name: deep-research
description: 주제 심층 조사
context: fork
agent: Explore
---

$ARGUMENTS 에 대해 철저히 조사:

1. Glob, Grep으로 관련 파일 찾기
2. 코드 읽고 분석
3. 파일 참조와 함께 발견 사항 요약
```

### 도구 제한

```yaml
---
name: safe-reader
description: 수정 없이 파일 읽기만
allowed-tools: Read, Grep, Glob
---
```

---

## 참고 자료

- [공식 Skills 문서](https://code.claude.com/docs/en/skills)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Plugins](https://code.claude.com/docs/en/plugins)
- [Hooks](https://code.claude.com/docs/en/hooks)
- [Permissions](https://code.claude.com/docs/en/iam)
