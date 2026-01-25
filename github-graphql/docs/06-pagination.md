# GraphQL API에서 페이지 매김 사용

## 페이지 매김 정보

GitHub의 GraphQL API는 단일 요청에서 가져올 수 있는 항목 수를 제한합니다. 모든 연결에 대해 `first` 또는 `last` 인수를 제공해야 하며, 값은 1~100 사이여야 합니다.

데이터가 지정된 항목 수보다 많으면 응답이 여러 "페이지"로 나뉩니다. 마지막 페이지가 아닌 경우 각 페이지에는 지정된 수의 항목이 포함됩니다.

## 쿼리에서 cursor 요청

커서를 사용하여 페이지가 나뉜 데이터를 탐색합니다. `pageInfo` 개체를 쿼리하여 첫 번째와 마지막 커서를 얻을 수 있습니다:

```graphql
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    pullRequests(first: 100, after: null) {
      nodes {
        createdAt
        number
        title
      }
      pageInfo {
        endCursor
        startCursor
        hasNextPage
        hasPreviousPage
      }
    }
  }
}
```

### pageInfo 필드

| 필드 | 설명 |
|------|------|
| `startCursor` | 페이지의 첫 번째 항목 커서 |
| `endCursor` | 페이지의 마지막 항목 커서 |
| `hasNextPage` | 다음 페이지 존재 여부 |
| `hasPreviousPage` | 이전 페이지 존재 여부 |

## 페이지당 항목 수 변경

`first` 및 `last` 인수는 반환되는 항목 수를 제어합니다. 최대 100개까지 요청 가능합니다. 속도 제한에 도달하지 않으려면 더 적은 수를 요청해야 할 수 있습니다.

## 페이지 매김을 사용하여 데이터 집합 트래버스

### 다음 페이지 조회 (정방향)

커서를 받으면 `after` 인수와 함께 사용하여 다음 페이지를 요청할 수 있습니다:

```graphql
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    pullRequests(first: 1, after: "Y3Vyc29yOnYyOpHOUH8B7g==") {
      nodes {
        createdAt
        number
        title
      }
      pageInfo {
        endCursor
        hasNextPage
        hasPreviousPage
      }
    }
  }
}
```

`hasNextPage`가 `false`를 반환할 때까지 새로운 `endCursor` 값으로 계속 요청합니다.

### 이전 페이지 조회 (역방향)

역방향 탐색의 경우 `last`를 사용하고 `startCursor`와 `before` 인수로 이전 페이지를 가져옵니다:

```graphql
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    pullRequests(last: 1, before: "R3Vyc29yOnYyOpHOHcfoOg==") {
      nodes {
        createdAt
        number
        title
      }
      pageInfo {
        startCursor
        hasPreviousPage
      }
    }
  }
}
```

## 페이지네이션 인수 요약

| 인수 | 방향 | 설명 |
|------|------|------|
| `first` | 정방향 | 처음부터 N개 항목 |
| `after` | 정방향 | 이 커서 이후 항목 |
| `last` | 역방향 | 마지막부터 N개 항목 |
| `before` | 역방향 | 이 커서 이전 항목 |

## 다음 단계

Octokit SDK와 `octokit/plugin-paginate-graphql` 플러그인을 사용하여 스크립트의 페이지 매김을 자동화할 수 있습니다.
