# GitHub GraphQL Objects: User and ContributionsCollection

## User Object

**User** 객체는 GitHub에 하나 이상의 계정을 가진 사람을 나타냅니다. User는 GitHub GraphQL API의 기본 엔터티로, `Actor` 인터페이스와 `Node` 인터페이스를 구현합니다.

### User 객체의 주요 특성

- 리포지토리와 상호작용
- 이슈 생성
- 풀 리퀘스트 제출
- GitHub 전반의 프로젝트에 기여

### User 쿼리 예시

```graphql
query($username: String!) {
  user(login: $username) {
    login
    name
    email
    bio
    avatarUrl
    createdAt
    contributionsCollection {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
  }
}
```

## ContributionsCollection Object

**ContributionsCollection** 객체는 분석을 위해 기여 데이터를 집계합니다. 이 객체는 사용자가 만든 기여 요약을 제공하여 지정된 기간 내 여러 기여 카테고리 및 리포지토리에 걸친 개발 활동을 포괄적으로 추적할 수 있게 합니다.

### 포함되는 기여 유형

| 기여 유형 | 설명 |
|----------|------|
| `CreatedCommitContribution` | 작성한 커밋 |
| `CreatedIssueContribution` | 생성한 이슈 |
| `CreatedPullRequestContribution` | 제출한 풀 리퀘스트 |
| `CreatedPullRequestReviewContribution` | 제공한 코드 리뷰 |
| `CreatedRepositoryContribution` | 생성한 새 리포지토리 |

### ContributionsCollection 주요 필드

```graphql
contributionsCollection(from: DateTime, to: DateTime) {
  # 총 기여 수
  totalCommitContributions
  totalIssueContributions
  totalPullRequestContributions
  totalPullRequestReviewContributions
  totalRepositoryContributions

  # 기여 캘린더
  contributionCalendar {
    totalContributions
    weeks {
      contributionDays {
        date
        contributionCount
      }
    }
  }

  # 리포지토리별 기여
  commitContributionsByRepository {
    repository {
      name
    }
    contributions {
      totalCount
    }
  }

  pullRequestContributionsByRepository {
    repository {
      name
    }
    contributions {
      totalCount
    }
  }
}
```

### 시간 범위 지정

`from`과 `to` 인수를 사용하여 특정 기간의 기여를 조회할 수 있습니다:

```graphql
query($username: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $username) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
      }
    }
  }
}
```

### 참고 사항

- 기본적으로 지난 1년간의 기여를 반환
- `from`/`to`로 최대 1년 범위 지정 가능
- 비공개 리포지토리 기여는 `restrictedContributionsCount`로 별도 집계
