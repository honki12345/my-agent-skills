# 전역 노드 ID 사용

## 개요

이 문서는 REST API를 통해 얻은 전역 노드 ID를 GraphQL 작업에서 활용하는 방법을 설명합니다.

## REST와 GraphQL의 노드 ID 필드명 차이

- **REST API**: 전역 노드 ID 필드명은 `node_id`
- **GraphQL**: `node` 인터페이스의 `id` 필드

## 3단계 프로세스

전역 노드 ID 활용 방법:

1. **REST 엔드포인트 호출**: 개체의 `node_id`를 반환하는 REST API 호출
2. **GraphQL 형식 확인**: 개체 형식을 파악
3. **직접 노드 조회**: ID와 형식을 사용한 GraphQL 쿼리 실행

## 코드 예시

### 1단계: REST API 호출

```shell
curl -i --header "Authorization: Bearer YOUR-TOKEN" https://api.github.com/user
```

응답에 포함된 `node_id` 값: `MDQ6VXNlcjU4MzIzMQ==`

### 2단계: GraphQL 형식 확인

```graphql
query {
  node(id:"MDQ6VXNlcjU4MzIzMQ==") {
     __typename
  }
}
```

결과: `User` 형식

### 3단계: 인라인 조각을 사용한 데이터 조회

```graphql
query {
  node(id:"MDQ6VXNlcjU4MzIzMQ==") {
   ... on User {
      name
      login
    }
  }
}
```

## 활용 예시

### 여러 노드 한 번에 조회

```graphql
query {
  nodes(ids: ["MDQ6VXNlcjU4MzIzMQ==", "MDEwOlJlcG9zaXRvcnkxMjM0NTY="]) {
    __typename
    ... on User {
      login
      name
    }
    ... on Repository {
      name
      owner {
        login
      }
    }
  }
}
```

### Mutation에서 노드 ID 사용

```graphql
mutation {
  addReaction(input: {
    subjectId: "MDU6SXNzdWUyMzEzOTE1NTE=",
    content: THUMBS_UP
  }) {
    reaction {
      content
    }
  }
}
```

## 마이그레이션 시 활용

API 버전 간 전환 시 전역 노드 ID를 유지하면 개체 참조를 쉽게 유지할 수 있습니다. REST API에서 GraphQL로 마이그레이션할 때 특히 유용합니다.

## 노드 ID 구조

노드 ID는 Base64로 인코딩되어 있으며, 디코딩하면 객체 유형과 식별자 정보를 포함합니다:

```
MDQ6VXNlcjU4MzIzMQ==  →  04:User583231
```

단, 이 내부 구조에 의존하지 않는 것이 좋습니다. GitHub에서 형식을 변경할 수 있습니다.
