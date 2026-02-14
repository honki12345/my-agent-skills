---
name: git-master
description: "Git 워크플로우 자동화(원자적 커밋 분리, 히스토리 정리, 변경 추적). 커밋 분리, rebase 계획/실행, 변경 이력 추적을 요청할 때 사용한다."
---

# Git Master

변경사항을 이해하고 논리적 단위로 원자적 커밋을 생성합니다.

## 3가지 모드

사용자 요청에 따라 자동으로 모드를 선택한다. 명시적 지정도 가능.

```
git-master              → 변경사항 분석 후 자동 모드 선택
git-master commit       → COMMIT 모드 강제
git-master rebase       → REBASE 모드 강제
git-master search 함수명 → HISTORY_SEARCH 모드
```

---

## MODE 1: COMMIT (원자적 커밋)

변경사항을 분석하여 논리적 단위로 분리하고 각각 원자적 커밋을 생성한다.

### 워크플로우

#### 1단계: 변경사항 파악

```bash
git status --porcelain
git diff --stat
git diff --cached --stat
git diff
git diff --cached
```

- staged와 unstaged 변경사항 모두 확인
- untracked 파일도 포함

#### 2단계: 변경 내용 이해

각 파일의 변경 내용을 **실제로 읽고 이해**한다:

- 어떤 기능이 추가/수정/삭제되었는지
- 파일 간의 관계 (같은 기능에 속하는 파일들)
- 변경의 성격 (기능 추가, 버그 수정, 리팩토링, 스타일, 테스트, 문서 등)

#### 3단계: 논리적 그룹으로 분류

변경 파일을 논리적 단위로 그룹핑:

- **같은 기능**의 파일들 → 하나의 커밋
- **리팩토링/스타일** 변경 → 기능과 분리된 별도 커밋
- **테스트** → 구현과 같은 커밋 또는 별도 커밋
- **설정/인프라** 변경 → 별도 커밋
- **문서** 변경 → 별도 커밋

**파일 수 기반 분리 기준:**

| 파일 수 | 전략 |
|---------|------|
| 1~3개 | 단일 커밋 가능 |
| 4~10개 | 2~3개 커밋으로 분리 검토 |
| 10개 초과 | 반드시 논리적 단위로 분리 |

#### 4단계: 커밋 계획 제시

실행 전에 커밋 계획을 사용자에게 보여준다:

```
## 커밋 계획

1. feat(auth): 로그인 기능 추가
   - src/auth/login.ts
   - src/auth/login.test.ts

2. refactor(utils): 헬퍼 함수 정리
   - src/utils/helper.ts

3. docs: README 업데이트
   - README.md
```

> **중요**: 사용자 확인 후 실행한다.

#### 5단계: 순서대로 커밋 실행

```bash
git add <파일1> <파일2>
git commit -m "<메시지>"
```

- 각 그룹별로 `git add` → `git commit` 순서대로 실행
- `git add .` 또는 `git add -A`는 사용하지 않는다

### 커밋 메시지 규칙 (Conventional Commits)

```
<type>(<scope>): <subject>

[body]
```

**type:**

| 타입 | 설명 |
|------|------|
| feat | 새로운 기능 |
| fix | 버그 수정 |
| refactor | 리팩토링 (기능 변경 없음) |
| style | 코드 스타일/포맷 (기능 변경 없음) |
| test | 테스트 추가/수정 |
| docs | 문서 변경 |
| chore | 빌드/설정/도구 변경 |
| perf | 성능 개선 |
| ci | CI 설정 변경 |

**규칙:**
- scope: 변경 대상 모듈/컴포넌트 (선택)
- subject: 50자 이내, 명령형, 마침표 없음
- body: 72자 줄바꿈, "왜" 변경했는지 설명 (선택)

**프로젝트별 컨벤션 우선:**
- 커밋 전 프로젝트 루트의 `AGENTS.md`를 확인하여 커밋 컨벤션이 있으면 그것을 따른다
- 프로젝트 컨벤션이 없으면 위의 Conventional Commits 규칙을 기본으로 사용

---

## MODE 2: REBASE (히스토리 정리)

> **주의**: `git rebase` 명령은 파괴적 작업이므로 반드시 사용자 승인이 필요하다.

### 워크플로우

#### 1단계: 히스토리 확인

```bash
git log --oneline -20
```

#### 2단계: 정리 전략 제시

정리 대상 커밋 범위와 전략을 제안한다:

- **squash**: 관련 커밋 합치기 (예: "fix typo" 연속 커밋)
- **reword**: 커밋 메시지 수정
- **reorder**: 커밋 순서 재배치
- **fixup**: squash와 동일하지만 메시지 버림

```
## Rebase 계획

대상: HEAD~5 (최근 5개 커밋)

1. pick   abc1234 feat(auth): 로그인 구현
2. squash def5678 fix: 로그인 오타 수정
3. squash ghi9012 fix: 로그인 버그 수정
4. pick   jkl3456 feat(auth): 회원가입 구현
5. reword mno7890 wip → feat(auth): 비밀번호 재설정

결과: 3개 커밋으로 정리
```

#### 3단계: 사용자 확인 후 실행

> **반드시 사용자 승인을 받은 후 실행한다.**

---

## MODE 3: HISTORY_SEARCH (변경 추적)

특정 코드/파일의 변경 이력을 추적한다.

### 워크플로우

#### 1단계: 검색 대상 파악

사용자가 지정한 파일, 함수, 키워드를 기준으로 검색 전략을 결정한다.

#### 2단계: 이력 조회

**파일 기반:**
```bash
git log --oneline --follow -- <파일경로>
git log -p -- <파일경로>
```

**키워드/함수 기반:**
```bash
git log -S "<키워드>" --oneline
git log -G "<패턴>" --oneline
```

**특정 라인 기반:**
```bash
git log -L <시작>,<끝>:<파일>
git blame <파일>
```

#### 3단계: 변경 맥락 요약

조회한 이력을 정리하여 보여준다:

- **언제** 변경되었는지 (날짜, 커밋)
- **누가** 변경했는지 (작성자)
- **왜** 변경했는지 (커밋 메시지, diff 맥락)
- 변경의 **흐름** (시간순 변천사)
