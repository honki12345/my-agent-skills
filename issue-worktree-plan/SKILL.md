---
name: issue-worktree-plan
description: "GitHub 이슈 URL을 인자로 받아 이슈 정보를 확인하고 git worktree 기반 작업 브랜치를 생성한 뒤 이슈 계획 문서를 만든다. 이슈 URL 기준으로 브랜치/worktree/계획 문서 초기화를 요청할 때 사용한다."
argument-hint: "[issue-url]"
disable-model-invocation: true
---

# Issue Worktree Plan

GitHub 이슈를 기준으로 작업 준비를 자동화하는 작업형 스킬이다.

핵심 원칙:

1. URL 검증 우선
- `$ARGUMENTS`가 유효한 GitHub issue URL인지 먼저 확인한다.

2. worktree 안전성 우선
- 기존 브랜치/워크트리와 충돌하면 덮어쓰지 않고 중단 후 선택지를 제시한다.

3. 문서 일관성 유지
- 계획 문서는 항상 `docs/plan/ISSUE_{번호}_{slug}.md` 형식으로 생성한다.

## 사용법

- 호출 예시: `/issue-worktree-plan https://github.com/org/repo/issues/123`
- 인자가 없으면 issue URL 입력을 요청하고 중단한다.

## 실행 워크플로우

### 1단계: 입력 파싱 및 검증

1. `$ARGUMENTS`에서 issue URL을 추출한다.
2. 아래 패턴과 일치하는지 확인한다.
- `https://github.com/{owner}/{repo}/issues/{number}`
3. owner/repo/issue_number를 파싱한다.
4. 형식이 맞지 않으면 예시를 보여주고 중단한다.

### 2단계: 이슈 메타데이터 확인

아래 명령으로 이슈 정보를 가져온다.

```bash
gh issue view "$ISSUE_URL" --json number,title,body,state,url
```

검증 항목:
- 조회 실패: `gh auth status` 확인 안내 후 중단
- `state`가 `OPEN`이 아닌 경우: 진행 여부를 사용자에게 확인

### 3단계: 저장소/기준 브랜치 확인

1. 현재 경로가 git 저장소인지 확인한다.
2. 저장소 루트를 구한다.
3. 기준 브랜치를 아래 우선순위로 결정한다.
- `origin/HEAD`가 가리키는 기본 브랜치
- `main`
- `master`
- 현재 체크아웃 브랜치

참고 명령:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
```

### 4단계: 브랜치명/워크트리 경로 결정

1. 이슈 제목을 slug로 정규화한다.
- branch slug: kebab-case (`-`)
- 문서 slug: snake_case (`_`)
2. 브랜치명을 만든다.
- `issue-{number}-{branch-slug}`
3. 워크트리 경로를 만든다.
- `${REPO_ROOT}/.worktrees/{branch-name}`

### 5단계: git worktree 생성

기본 명령:

```bash
git fetch origin "$DEFAULT_BRANCH"
git worktree add -b "$BRANCH_NAME" "$WORKTREE_PATH" "origin/$DEFAULT_BRANCH"
```

충돌 처리 규칙:
- 워크트리 경로가 이미 존재하면 중단하고 다른 경로를 요청한다.
- 브랜치가 이미 있고 다른 워크트리에 붙어 있으면 중단하고 기존 경로를 안내한다.
- 브랜치가 이미 있고 워크트리에 붙어 있지 않으면 아래로 연결한다.

```bash
git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"
```

### 6단계: 계획 문서 생성

1. `${WORKTREE_PATH}/docs/plan` 디렉토리를 생성한다.
2. 계획 문서 파일명을 만든다.
- `docs/plan/ISSUE_{number}_{doc-slug}.md`
3. 아래 템플릿으로 문서를 생성한다.

```markdown
# ISSUE #{번호} {이슈 제목}

## 메타 정보
- Issue URL: {이슈 URL}
- Issue 번호: {번호}
- 기준 브랜치: {기준 브랜치}
- 작업 브랜치: {작업 브랜치}
- Worktree 경로: {worktree 경로}
- 작성일: {YYYY-MM-DD}

## 배경/문제
{이슈 본문 요약 또는 원문 핵심}

## 목표
- [ ] 목표 1
- [ ] 목표 2

## 범위
### 포함
- {구현할 항목}

### 제외
- {이번 작업에서 하지 않을 항목}

## 구현 단계
1. [ ] 분석 및 재현
2. [ ] 구현
3. [ ] 테스트
4. [ ] 문서화/정리

## 리스크 및 확인 필요 사항
- {리스크}
- {확인 질문}

## 검증 계획
- [ ] 단위/통합 테스트
- [ ] 수동 시나리오 검증
```

이미 같은 파일이 있으면 덮어쓰기 전에 사용자 확인을 받는다.

### 7단계: 결과 보고

아래 항목을 한 번에 보고한다.
- issue URL / 제목 / 번호
- 기준 브랜치
- 생성된 작업 브랜치
- 생성된 worktree 경로
- 생성된 계획 문서 경로
- 다음 작업 시작 명령 (`cd {worktree}`)

## 금지 사항

- 기존 worktree 디렉토리를 무단 삭제/덮어쓰기
- 사용자 확인 없이 기존 계획 문서 덮어쓰기
- 이슈와 무관한 브랜치명/문서명 생성
