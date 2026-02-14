---
name: ship
description: 변경사항 커밋/푸시 워크플로우 자동화. 이슈 생성, 브랜치 생성, 원자적 커밋, 검증, push, PR 생성을 한 번에 진행해 달라는 명시적 요청에서 사용한다.
---

# 변경사항 커밋 및 푸시

현재 변경사항을 분석하여 이슈 생성 → 브랜치 생성 → 원자적 커밋 → CI → 푸시까지 자동화합니다.

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

> `git-master` 스킬의 COMMIT 절차를 따라 변경사항을 논리적 단위로 분리하고 원자적 커밋을 생성한다.
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

- [ ] 1. frontend/ 변경 시 `vercel-react-best-practices` 스킬로 리뷰 실행
- [ ] 2. frontend/ 변경 시 `web-design-guidelines` 스킬로 리뷰 실행
- [ ] 3. backend/ 변경 시 `sqlite` 스킬로 리뷰 실행
- [ ] 4. backend/ 변경 시 `nestjs` 스킬로 리뷰 실행
- [ ] 5. 프로젝트의 CI 절차 실행 (docs만 변경 시 스킵)
- [ ] 6. 프로젝트의 문서 동기화 절차 실행 (코드 변경 시)
- [ ] 7. 이슈 업데이트 (`gh issue edit`)
- [ ] 8. push

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

### 9단계: 결과 출력

이슈/브랜치/커밋/PR 정보 요약 출력
