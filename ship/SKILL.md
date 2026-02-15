---
name: ship
description: 변경사항 커밋/푸시 워크플로우 자동화. 이슈 생성, 브랜치 생성, 원자적 커밋, 검증, push, PR 생성 후 CI 폴링/실패 복구까지 한 번에 진행해 달라는 명시적 요청에서 사용한다.
---

# 변경사항 커밋 및 푸시

현재 변경사항을 분석하여 이슈 생성 → 브랜치 생성 → 원자적 커밋 → CI → 푸시 → PR → CI 폴링/실패 복구까지 자동화합니다.

## 사용법

- `ship` - 변경사항 분석 후 새 이슈 생성하여 진행
- `ship {문서경로}` - 지정된 계획 문서를 참조하여 진행 (이슈 번호 추출)

## 컨벤션 참조

| 항목 | 참조 문서 |
|------|----------|
| 이슈 템플릿 | @.github/ISSUE_TEMPLATE/feature.md |
| 브랜치 네이밍 | @docs/conventions/BRANCH_STRATEGY.md |
| 커밋 메시지 | @docs/conventions/COMMIT_CONVENTION.md |
| PR 작성 | @docs/conventions/PR_CONVENTION.md |

---

## 실행 단계

### 1단계: 변경사항 분석

```bash
git status --porcelain
git diff --name-only
```

### 2단계: 계획 문서 확인

**`ship {문서경로}` 시:**
- 문서 읽고 이슈 번호/작업 내용 추출
- 이슈 번호 있으면 사용, 없으면 문서 기반 이슈 생성

**`ship` 시:**
- 변경사항 분석 후 직접 이슈 생성

### 3단계: 이슈 생성 (필요 시)

@.github/ISSUE_TEMPLATE/feature.md 템플릿 따라 생성

### 4단계: 브랜치 생성

@docs/conventions/BRANCH_STRATEGY.md 규칙 따라 생성

### 5단계: 원자적 커밋

> `git-master` 스킬을 호출해 COMMIT 절차를 수행한다.
> 변경사항을 논리적 단위로 분리하고 원자적 커밋을 생성한다.
> 프로젝트에 @docs/conventions/COMMIT_CONVENTION.md 가 있으면 해당 규칙을 따른다.

### 6단계: 이슈 관련 문서 커밋

> **중요**: `docs/plan/` 디렉토리에 현재 작업 중인 이슈 관련 문서가 있는지 확인

```bash
# 이슈 번호로 관련 문서 검색
ls docs/plan/ | grep -i "ISSUE_{이슈번호}"
```

**문서가 존재하면:**
1. 해당 문서를 staging에 추가
2. 별도 커밋으로 분리: `docs: 이슈 #{번호} 계획 문서`

### 7단계: push 전 필수 순서

> **중요: 아래 체크리스트를 순서대로 실행하고, 각 단계 완료 후 다음으로 진행**
> - 프로젝트 컨벤션에 정의된 자동화 절차가 있으면 그 절차를 우선 적용할 것
> - 스킬이 있는 항목은 해당 스킬을 사용해 검증할 것

**체크리스트 (순서대로 실행 필수):**

- [ ] 1. 변경사항을 `backend/frontend/database/ui/ux` 및 관련 라이브러리/프레임워크로 분류하고, 해당 도메인과 매칭되는 스킬이 있으면 모두 검토/리뷰 실행
  - 예: `vercel-react-best-practices`, `web-design-guidelines`, `nestjs`, `sqlite`, `tanstack-query`, `github-graphql`
- [ ] 2. 프로젝트의 CI 절차 실행 (docs만 변경 시 스킵)
- [ ] 3. 프로젝트의 문서 동기화 절차 실행 (코드 변경 시)
- [ ] 4. 이슈 업데이트 (`gh issue edit`)
- [ ] 5. push

**리뷰 실행 결과 기록(필수):**
- 실행한 리뷰/검증 스킬명
- 대상(파일/모듈)
- 결과(문제 없음/수정 필요)와 근거
- 수정 필요 시 반영 커밋 또는 미반영 사유

```bash
git push -u origin {브랜치명}
```

### 8단계: PR 생성

@docs/conventions/PR_CONVENTION.md 템플릿 따라 PR 생성

```bash
gh pr create --repo boostcampwm2025/web19-estrogenquattro \
  --title "{타입}: {설명}" \
  --body "..."
```

### 9단계: PR CI 폴링 및 실패 복구 루프

> **핵심**: 8단계에서 생성한 PR의 CI가 모두 통과할 때까지 계속 폴링한다.
> 실패가 발생하면 즉시 분석하고 수정 커밋을 반영한 뒤 다시 폴링한다.

**PR 식별자 확보**

```bash
PR_NUMBER="{8단계에서 생성한 PR 번호}"
POLL_INTERVAL_SEC=60
```

**상태 폴링 (60초 간격 반복)**

```bash
gh pr view "$PR_NUMBER" --json statusCheckRollup --jq '
  .statusCheckRollup[] |
  [.name // .context, (.conclusion // .status // .state // "PENDING"), (.detailsUrl // .targetUrl // "")] |
  @tsv
'
```

**상태 판정 규칙**
- `SUCCESS`만 남으면 종료
- `PENDING/IN_PROGRESS/QUEUED/EXPECTED/WAITING`이 하나라도 있으면 `sleep "$POLL_INTERVAL_SEC"` 후 재조회
- `FAILURE/ERROR/CANCELLED/TIMED_OUT`이 하나라도 있으면 아래 실패 복구 절차 수행

**실패 복구 절차**
1. 최신 실패 run 식별

```bash
HEAD_BRANCH=$(gh pr view "$PR_NUMBER" --json headRefName --jq .headRefName)
gh run list --limit 50 --json databaseId,headBranch,event,status,conclusion,name,url,createdAt --jq \
  ".[] | select(.headBranch == \"$HEAD_BRANCH\" and .event == \"pull_request\") | [.databaseId, .name, .status, .conclusion, .url] | @tsv"
```

2. 실패 로그 수집

```bash
gh run view {RUN_ID} --log-failed
```

3. `debug-loop` 스킬과 도메인 스킬을 사용해 원인 재현/분석 후 수정 반영
4. 필요한 로컬 테스트/검증 실행
5. 수정사항 commit + push
6. PR에 실패 원인/수정 내용/검증 결과 업데이트

```bash
gh pr comment "$PR_NUMBER" --body "CI 실패 원인, 수정 내용, 검증 결과 요약"
```

7. 9단계 폴링 루프로 복귀

**예외 처리**
- 동일 실패 패턴이 2회 이상 반복되면 원인과 대안을 정리해 사용자 승인 후 진행
- 권한/시크릿/외부 장애 등 자동 수정 불가 사유는 즉시 보고하고 필요한 수동 조치를 명시

### 10단계: 결과 출력

아래 항목을 함께 요약 출력한다.
- 이슈/브랜치/커밋/PR 정보
- push 전 리뷰/검증 실행 결과
  - 실행한 스킬 목록
  - 결과 요약(문제 없음/수정 반영/미반영)
  - 미반영 항목이 있으면 사유와 후속 액션
- PR CI 폴링/복구 결과
  - 폴링 횟수와 최종 상태
  - 실패 발생 시 원인 요약, 수정 커밋, 재검증 결과
