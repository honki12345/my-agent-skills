# GraphQL을 사용하여 호출 형성

## 개요

이 GitHub 문서는 GraphQL API를 사용하여 쿼리와 변형을 작성하고 실행하는 방법을 설명합니다.

## GraphQL을 사용하여 인증

세 가지 인증 방식을 지원합니다:

1. **Personal Access Token** - "issues:read" 같은 권한을 지정하여 토큰 생성
2. **GitHub App** - 조직이나 다른 사용자를 대신하여 API 사용
3. **OAuth App** - 웹 애플리케이션 또는 장치 흐름을 통한 권한 부여

## GraphQL 엔드포인트

GitHub.com의 GraphQL API 엔드포인트:
```
https://api.github.com/graphql
```

## GraphQL과 통신

GraphQL 작업은 JSON으로 인코딩된 본문을 사용하는 POST 요청입니다.

**curl 예시:**
```bash
curl -H "Authorization: bearer TOKEN" -X POST -d " \
 { \
   \"query\": \"query { viewer { login }}\" \
 } \
" https://api.github.com/graphql
```

## 쿼리와 변형

**쿼리** - 데이터 조회 (GET처럼 작동)
```graphql
query {
  JSON-OBJECT-TO-RETURN
}
```

**변형** - 데이터 수정 (POST/PATCH/DELETE처럼 작동)
```graphql
mutation {
  MUTATION-NAME(input: {MUTATION-NAME-INPUT!}) {
    MUTATION-NAME-PAYLOAD
  }
}
```

## 변수 사용

변수를 통해 쿼리를 동적으로 만듭니다:

```graphql
query($number_of_repos:Int!) {
  viewer {
    name
    repositories(last: $number_of_repos) {
      nodes {
        name
      }
    }
  }
}
variables {
  "number_of_repos": 3
}
```

세 단계: 변수 정의 → 작업에 인수로 전달 → 작업 내에서 사용

## 예제 쿼리

octocat/Hello-World 리포지토리의 종료된 이슈 20개 조회:

```graphql
query {
  repository(owner:"octocat", name:"Hello-World") {
    issues(last:20, states:CLOSED) {
      edges {
        node {
          title
          url
          labels(first:5) {
            edges {
              node {
                name
              }
            }
          }
        }
      }
    }
  }
}
```

## 예제 변형

이슈에 반응 추가:

```graphql
query FindIssueID {
  repository(owner:"octocat", name:"Hello-World") {
    issue(number:349) {
      id
    }
  }
}

mutation AddReactionToIssue {
  addReaction(input:{subjectId:"MDU6SXNzdWUyMzEzOTE1NTE=",content:HOORAY}) {
    reaction {
      content
    }
    subject {
      id
    }
  }
}
```

**반응 콘텐츠 값:**
- `+1` → 👍
- `-1` → 👎
- `laugh` → 😄
- `confused` → 😕
- `heart` → ❤️
- `hooray` → 🎉
- `rocket` → 🚀
- `eyes` → 👀

## 추가 참고 자료

- 페이지 매김
- 조각 (Fragments)
- 인라인 조각
- 지시문 (Directives)
