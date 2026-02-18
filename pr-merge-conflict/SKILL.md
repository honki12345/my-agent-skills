---
name: pr-merge-conflict
description: "GitHub PR URL을 인자로 받아 merge conflict(병합 충돌) 유무를 판정하고, 충돌이 없으면 즉시 종료한다. 충돌이 있으면 충돌 파일/원인 커밋을 추적해 어떤 PR/브랜치에서 유입된 변경인지 식별한 뒤, 양쪽 PR/이슈의 plans(또는 docs/plan) 문서를 찾아 의도한 구현을 모두 보존하는 형태로 충돌을 해결하고 commit+push 해서 PR이 다시 mergeable 해질 때까지 확인한다. PR 병합 충돌 해결을 요청받으면 사용한다."
argument-hint: "[pr-url]"
disable-model-invocation: true
---

# PR Merge Conflict

GitHub PR의 merge conflict(병합 충돌)를 `판정 -> 원인 추적 -> 계획 문서 합치기 -> 충돌 해결 구현 -> commit -> push -> 재판정` 루프로 해결한다.

핵심 원칙:

1. 충돌 없으면 즉시 종료
- `mergeable`이 `MERGEABLE`이면 작업을 시작하지 않는다.

2. 구현 보존 우선 (양쪽 다)
- 충돌은 "한쪽을 버리는 것"으로 해결하지 않는다.
- PR0(이번 PR) + PRx(충돌 원인 PR/브랜치)의 계획 문서 의도를 모두 보존하는 구현으로 통합한다.

3. 계획 문서가 소스 오브 트루스
- `plans/` 또는 `docs/plan/` 문서를 우선 탐색/참조한다.
- 계획이 서로 모순이면, 임의로 결정하지 말고 사용자에게 1개씩 질문으로 확정한다.

4. 최소 변경
- 충돌 해결에 필요한 최소한의 수정만 한다.
- 리네이밍/대규모 리팩토링/스타일 정리는 금지 (필요 시 별도 PR로 분리).

5. 브랜치/푸시 안전장치
- 현재 체크아웃 브랜치가 PR head branch와 다르면 즉시 중단한다.
- force push는 기본 금지. (rebase 선택 시에만 `--force-with-lease` 허용)

## 사용법

- `/pr-merge-conflict https://github.com/{owner}/{repo}/pull/{number}`
- 인자가 없으면 PR URL 입력을 요청하고 중단한다.

## 실행 워크플로우

### 0단계: 입력 검증 및 파싱

1. `$ARGUMENTS`에서 PR URL을 추출한다.
2. 아래 패턴과 일치하는지 확인한다.
- `https://github.com/{owner}/{repo}/pull/{number}`
3. 형식이 맞지 않으면 예시를 보여주고 중단한다.

파싱 예시:

```bash
PR_URL="$ARGUMENTS"
echo "$PR_URL" | grep -Eq '^https://github.com/[^/]+/[^/]+/pull/[0-9]+/?$'

OWNER=$(echo "$PR_URL" | sed -E 's@^https://github.com/([^/]+)/([^/]+)/pull/([0-9]+)/?$@\1@')
REPO=$(echo "$PR_URL" | sed -E 's@^https://github.com/([^/]+)/([^/]+)/pull/([0-9]+)/?$@\2@')
PR_NUMBER=$(echo "$PR_URL" | sed -E 's@^https://github.com/([^/]+)/([^/]+)/pull/([0-9]+)/?$@\3@')
REPO_NWO="$OWNER/$REPO"
```

### 1단계: 사전 체크 (저장소/인증/브랜치)

```bash
git rev-parse --is-inside-work-tree
gh auth status
```

현재 디렉토리의 저장소가 PR 저장소와 같은지 확인(권장):

```bash
LOCAL_REPO_NWO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
test "$LOCAL_REPO_NWO" = "$REPO_NWO"
```

### 2단계: PR merge conflict 유무 판정 (충돌 없으면 종료)

PR 메타데이터 수집:

```bash
PR_BASE_BRANCH=$(gh pr view -R "$REPO_NWO" "$PR_NUMBER" --json baseRefName --jq .baseRefName)
PR_HEAD_BRANCH=$(gh pr view -R "$REPO_NWO" "$PR_NUMBER" --json headRefName --jq .headRefName)
PR_HEAD_SHA=$(gh pr view -R "$REPO_NWO" "$PR_NUMBER" --json commits --jq '.commits[-1].oid')
PR_MERGEABLE=$(gh pr view -R "$REPO_NWO" "$PR_NUMBER" --json mergeable --jq .mergeable)
echo "$PR_MERGEABLE base=$PR_BASE_BRANCH head=$PR_HEAD_BRANCH sha=$PR_HEAD_SHA"
```

판정:
- `MERGEABLE`: 즉시 종료 (충돌 해결 불필요)
- `CONFLICTING`: 다음 단계로 진행
- `UNKNOWN`: 10~30초 대기 후 최대 5회 재조회하고, 계속 `UNKNOWN`이면 현재 정보로 진행하되 마지막에 재검증한다.

### 3단계: 현재 브랜치 == PR head branch 검증 (불일치 시 중단)

```bash
CURRENT_BRANCH=$(git branch --show-current)
test -n "$CURRENT_BRANCH"
test "$CURRENT_BRANCH" = "$PR_HEAD_BRANCH"

CURRENT_SHA=$(git rev-parse HEAD)
test "$CURRENT_SHA" = "$PR_HEAD_SHA"

test -z "$(git status --porcelain)"
```

불일치 시 안내(예시):

```bash
echo "현재 브랜치가 PR head branch가 아닙니다."
echo "권장: gh pr checkout -R \"$REPO_NWO\" \"$PR_NUMBER\""
```

### 4단계: 충돌 파일/원인 커밋/원인 PR 추적

기본 접근:
- PR head branch(현재 브랜치)에 base branch를 합치는 과정에서 충돌 파일을 수집한다.
- 각 충돌 파일에 대해 merge-base 이후 양쪽(HEAD/base)에서 가장 최근에 해당 파일을 건드린 커밋을 후보로 잡고, 그 커밋이 어떤 PR에서 들어왔는지 매핑한다.

사전 fetch:

```bash
git fetch origin "$PR_BASE_BRANCH"
MB=$(git merge-base HEAD "origin/$PR_BASE_BRANCH")
echo "merge-base=$MB"
```

충돌 파일 수집(merge는 반드시 abort로 원복):

```bash
git merge --no-commit --no-ff "origin/$PR_BASE_BRANCH" || true
CONFLICT_FILES=$(git diff --name-only --diff-filter=U)
echo "$CONFLICT_FILES"
```

충돌이 재현되지 않으면:
- `git merge --abort`로 원복한다.
- GitHub의 `mergeable` 상태가 오래된 것일 수 있으니 다시 조회 후 종료하거나, 필요 시 `git fetch`/`gh pr view` 재시도한다.

원인 커밋/PR 매핑(파일별 반복):

```bash
for f in $CONFLICT_FILES; do
  echo "== $f =="

  HEAD_SIDE_SHA=$(git log -n 1 --format=%H "$MB..HEAD" -- "$f" || true)
  BASE_SIDE_SHA=$(git log -n 1 --format=%H "$MB..origin/$PR_BASE_BRANCH" -- "$f" || true)

  if test -n "$HEAD_SIDE_SHA"; then
    git show -s --date=short --format="head  %h %ad %an %s" "$HEAD_SIDE_SHA"
    gh api -H "Accept: application/vnd.github+json" "/repos/$REPO_NWO/commits/$HEAD_SIDE_SHA/pulls" --jq '.[].html_url' || true
  fi

  if test -n "$BASE_SIDE_SHA"; then
    git show -s --date=short --format="base  %h %ad %an %s" "$BASE_SIDE_SHA"
    gh api -H "Accept: application/vnd.github+json" "/repos/$REPO_NWO/commits/$BASE_SIDE_SHA/pulls" --jq '.[].html_url' || true
  fi
done
```

원복:

```bash
git merge --abort || true
test -z "$(git status --porcelain)"
```

추적 결과 정리:
- 충돌 파일들에서 반복 등장하는 `base-side PR URL`을 1~3개로 좁혀 "충돌 원인 PR 후보"로 선정한다.
- PR이 여러 개면, 우선순위는 (1) 충돌 파일에 가장 많이 등장, (2) 최근 머지, (3) 이번 PR과 동일 모듈/도메인 순으로 둔다.

### 5단계: PR0(이번 PR) + PRx(충돌 원인) 계획 문서(plans) 탐색

목표:
- PR0과 PRx가 각각 어떤 의도로 어떤 변경을 했는지 "문서로 확정"한 뒤, 충돌 해결 구현에서 둘 다 만족시킨다.

PR 정보에서 이슈 번호 후보를 뽑는다:

```bash
# PR0
gh pr view -R "$REPO_NWO" "$PR_NUMBER" --json title,body,headRefName,baseRefName,url

# PRx (URL이 있으면)
PRX_URL="https://github.com/$REPO_NWO/pull/123" # 예시
gh pr view "$PRX_URL" --json title,body,headRefName,baseRefName,url
```

이슈 번호 추정 규칙(우선순위):
1. 브랜치명에 `issue-{number}-` 패턴이 있으면 그 번호 사용
2. PR 제목/본문에서 `Fixes #123`, `Closes #123`, `Resolves #123` 패턴 우선
3. 그 외 `#123` 패턴은 후보로만 수집하고, PR 번호와 혼동되지 않게 검증

plans 문서 위치 후보:
- `docs/plan/`
- `plans/`

탐색:

```bash
# PR URL로 직접 검색
rg -n "$PR_URL|pull/$PR_NUMBER" docs/plan plans 2>/dev/null || true

# 이슈 번호가 있으면 (예: 123)
ISSUE_NUMBER="123"
ls docs/plan 2>/dev/null | rg -n "ISSUE_${ISSUE_NUMBER}_" || true
find plans -type f -maxdepth 4 2>/dev/null | rg -n "ISSUE_${ISSUE_NUMBER}_" || true
```

문서가 여러 개면:
- 가장 최신(날짜/최근 수정) 문서 1개를 기준으로 삼고, 나머지는 "참고"로만 읽는다.
- 확신이 없으면 사용자에게 "어느 문서가 authoritative 인지" 1개 질문으로 확정한다.

문서를 못 찾으면:
- PR 본문에 링크된 문서/이슈를 추가로 확인한다.
- 그래도 없으면 사용자에게 계획 문서 경로를 요청하고 중단한다. (의도 보존이 불가능)

### 6단계: 충돌 해결 구현 (의도 보존)

전략 선택:
- 기본값: `merge`로 base를 PR head에 합친다. (force push 없이 해결 가능)
- 프로젝트가 linear history를 강제하거나, merge commit을 원치 않으면 `rebase`를 선택하되 `--force-with-lease` 전제다.

#### 옵션 A) merge (기본값)

```bash
git fetch origin "$PR_BASE_BRANCH"
git merge "origin/$PR_BASE_BRANCH"
```

충돌 파일에 대해:
- 충돌 마커(`<<<<<<<`, `=======`, `>>>>>>>`)를 제거한다.
- PR0 계획 문서의 요구사항을 모두 체크한다.
- PRx 계획 문서의 요구사항도 모두 체크한다.
- 같은 기능을 다른 방식으로 구현한 경우: API/스키마/호출부 호환을 유지하는 방향으로 "통합 구현"을 만든다.

해결 후:

```bash
git diff --name-only --diff-filter=U # 비어 있어야 함
git status
git add -A
git commit
```

#### 옵션 B) rebase (선택)

```bash
git fetch origin "$PR_BASE_BRANCH"
git rebase "origin/$PR_BASE_BRANCH"
```

충돌 해결 후:

```bash
git add -A
git rebase --continue
```

rebase 완료 후 push:

```bash
git push --force-with-lease
```

### 7단계: 검증 -> push -> mergeable 재확인

검증:
- 계획 문서에 적힌 테스트/검증 절차를 우선 실행한다.
- 없으면 프로젝트의 최소 CI 대체로 `test`, `lint`, `build` 중 가능한 것을 실행한다.

push:

```bash
git push
```

mergeable 재확인:

```bash
gh pr view -R "$REPO_NWO" "$PR_NUMBER" --json mergeable --jq .mergeable
```

여전히 `CONFLICTING`이면:
- base branch가 더 업데이트됐을 수 있으니 `git fetch origin "$PR_BASE_BRANCH"` 후 4~7단계를 반복한다.

### 8단계: 결과 보고

아래를 한 번에 보고한다.
- PR URL / PR 번호
- base/head 브랜치
- 충돌 원인 PR 후보(가능하면 링크)
- 참조한 계획 문서 경로(PR0/PRx 각각)
- 생성된 커밋 SHA
- 최종 `mergeable` 상태

## 금지 사항

- 현재 브랜치가 PR head branch가 아닌 상태에서 커밋/푸시
- 계획 문서를 확인하지 않고 임의로 한쪽 구현을 삭제하는 해결
- 사용자 확인 없이 force push (`--force`, `--force-with-lease`)
- 충돌 해결과 무관한 대규모 리팩토링/정리 커밋 섞기

