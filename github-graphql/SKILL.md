---
name: github-graphql
description: GitHub GraphQL API 가이드. GraphQL 쿼리 작성, Rate Limit 처리, User/ContributionsCollection 조회, 페이지네이션 등. GitHub API, GraphQL, contributionsCollection 키워드 또는 GitHub API 관련 코드 작업 시 자동 로드.
---

# GitHub GraphQL API 가이드

GitHub GraphQL API를 사용한 데이터 조회 및 조작을 위한 참조 문서입니다.

## 핵심 요약

### 엔드포인트

```
POST https://api.github.com/graphql
```

### 인증

```bash
curl -H "Authorization: Bearer {TOKEN}" \
  -X POST \
  -d '{"query": "query { viewer { login }}"}' \
  https://api.github.com/graphql
```

### Rate Limit

| 인증 방식 | 제한 |
|----------|------|
| Personal Access Token | 시간당 5,000 포인트 |
| GitHub App (Enterprise Cloud) | 시간당 10,000 포인트 |
| GitHub Actions GITHUB_TOKEN | 리포지토리당 시간당 1,000 포인트 |

**상태 확인 헤더:**
- `x-ratelimit-remaining`: 잔여 포인트
- `x-ratelimit-reset`: 재설정 시간 (Unix timestamp)

### 자주 사용하는 쿼리

#### 사용자 기여 조회

```graphql
query($username: String!) {
  user(login: $username) {
    contributionsCollection {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
  }
}
```

#### Rate Limit 확인

```graphql
query {
  rateLimit {
    limit
    remaining
    used
    resetAt
  }
}
```

#### 페이지네이션

```graphql
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    issues(first: 100, after: $cursor) {
      nodes { title }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
```

## 상세 문서

| 문서 | 설명 |
|------|------|
| [GraphQL 소개](docs/01-introduction-to-graphql.md) | 기본 개념, 스키마, 필드, Connection |
| [호출 형성](docs/02-forming-calls-with-graphql.md) | 인증, 쿼리/뮤테이션 작성법, 변수 사용 |
| [Rate Limits](docs/03-rate-limits.md) | 속도 제한, 포인트 계산, 최적화 전략 |
| [쿼리 참조](docs/04-queries-reference.md) | 루트 쿼리 목록 (user, repository 등) |
| [User/ContributionsCollection](docs/05-objects-user-contributions.md) | 사용자 기여 데이터 조회 |
| [페이지네이션](docs/06-pagination.md) | 커서 기반 페이지 매김 |
| [전역 노드 ID](docs/07-global-node-ids.md) | REST ↔ GraphQL 간 ID 활용 |

## 참조 링크

- [GitHub GraphQL API 공식 문서](https://docs.github.com/ko/graphql)
- [GraphQL Explorer](https://docs.github.com/ko/graphql/overview/explorer)
