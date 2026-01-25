# GraphQL 소개

## 개요
GitHub GraphQL API를 사용하기 위한 용어와 개념을 설명하는 가이드 문서입니다.

## GraphQL 용어

GitHub GraphQL API는 REST API와 다른 아키텍처 및 개념적 변화를 나타냅니다.

## 스키마

스키마는 GraphQL API의 형식 시스템을 정의합니다. "클라이언트가 액세스할 수 있는 가능한 데이터(개체, 필드, 관계, 모든 것)의 전체 집합을 설명"합니다. 클라이언트 호출은 스키마에 대해 검증되고 실행됩니다.

## 필드

필드는 개체에서 검색할 수 있는 데이터 단위입니다. "GraphQL 쿼리 언어는 기본적으로 개체의 필드를 선택하는 것"입니다.

중요: 모든 필드가 스칼라 값을 반환할 때까지 중첩된 하위 필드를 추가해야 합니다.

## 인수

인수는 특정 필드에 연결된 키-값 쌍의 집합입니다. 일부 필드에는 인수가 필요하며, 변형(Mutations)에는 입력 개체가 필수입니다.

## 구현

GraphQL 스키마는 `implements` 용어로 개체가 인터페이스에서 상속되는 방식을 정의합니다.

### 예시 코드:
```graphql
interface X {
  some_field: String!
  other_field: String!
}

type Y implements X {
  some_field: String!
  other_field: String!
  new_field: String!
}
```

`!` 기호는 필드가 필수임을 의미합니다.

## Connection

연결을 사용하면 단일 GraphQL 호출로 관련 개체를 쿼리할 수 있습니다. 이는 REST API의 여러 호출을 대체합니다. 노드(점)와 에지(선)의 관계를 정의합니다.

## Edge

에지는 노드 간의 연결을 나타냅니다. 모든 `edges` 필드는 `node` 필드와 `cursor` 필드를 포함하며, 커서는 페이지 매김에 사용됩니다.

## 노드

노드는 개체의 일반 용어입니다. 직접 조회하거나 연결을 통해 액세스할 수 있습니다.

## GraphQL API 검색

GraphQL은 내적(Introspection)이 가능하므로 자체에 대한 정보를 쿼리할 수 있습니다.

### 모든 형식 나열:
```graphql
query {
  __schema {
    types {
      name
      kind
      description
      fields {
        name
      }
    }
  }
}
```

### 특정 형식 조회:
```graphql
query {
  __type(name: "Repository") {
    name
    kind
    description
    fields {
      name
    }
  }
}
```

### curl을 통한 내적 검사:
```shell
curl -H "Authorization: bearer TOKEN" https://api.github.com/graphql
```

### IDL 형식으로 스키마 반환:
```shell
curl -H "Authorization: bearer TOKEN" \
  -H "Accept: application/vnd.github.v4.idl" \
  https://api.github.com/graphql
```

**주의:** GET 요청은 내적 검사 쿼리에만 사용되며, 그 외에는 POST 메서드를 사용합니다.
