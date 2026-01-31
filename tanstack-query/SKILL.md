---
name: tanstack-query
description: TanStack Query (React Query) v5 가이드. useQuery, useMutation, useInfiniteQuery 등 훅 사용법, 캐싱, 무효화, SSR, Suspense, Optimistic Updates 패턴. @tanstack/react-query 패키지 또는 React Query 관련 코드 작업 시 자동 로드.
---

# TanStack Query (React Query) v5 가이드

> 공식 문서: https://tanstack.com/query/latest

## 핵심 개념

### Query 기본

```tsx
import { useQuery } from '@tanstack/react-query'

const { data, isLoading, error } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
})
```

### Query Keys

- 배열 형태로 정의: `['todos']`, `['todos', { status: 'done' }]`
- 키는 직렬화 가능해야 함
- 객체 내부 키 순서는 무관: `{ a: 1, b: 2 }` === `{ b: 2, a: 1 }`

### Important Defaults (v5)

- `staleTime`: 기본 0 (즉시 stale)
- `gcTime`: 기본 5분 (이전 cacheTime)
- `refetchOnWindowFocus`: 기본 true
- `refetchOnReconnect`: 기본 true
- `retry`: 기본 3회

## 주요 Hooks

### useQuery
데이터 조회용. 자세한 옵션은 `docs/reference/useQuery.md` 참조.

### useMutation
데이터 변경용. 자세한 옵션은 `docs/reference/useMutation.md` 참조.

### useInfiniteQuery
무한 스크롤용. 자세한 옵션은 `docs/reference/useInfiniteQuery.md` 참조.

### useSuspenseQuery
React Suspense와 함께 사용. 자세한 옵션은 `docs/reference/useSuspenseQuery.md` 참조.

## 자주 사용되는 패턴

### Query Invalidation (캐시 무효화)

```tsx
const queryClient = useQueryClient()

// 특정 쿼리 무효화
queryClient.invalidateQueries({ queryKey: ['todos'] })

// 부분 매칭
queryClient.invalidateQueries({ queryKey: ['todos'], exact: false })
```

### Optimistic Updates

```tsx
useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] })
    const previousTodos = queryClient.getQueryData(['todos'])
    queryClient.setQueryData(['todos'], (old) => [...old, newTodo])
    return { previousTodos }
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context.previousTodos)
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['todos'] })
  },
})
```

### Dependent Queries

```tsx
const { data: user } = useQuery({
  queryKey: ['user', email],
  queryFn: () => getUser(email),
})

const { data: projects } = useQuery({
  queryKey: ['projects', user?.id],
  queryFn: () => getProjects(user.id),
  enabled: !!user?.id, // user가 있을 때만 실행
})
```

### Prefetching

```tsx
// 마우스 호버 시 prefetch
const prefetchTodo = async (id) => {
  await queryClient.prefetchQuery({
    queryKey: ['todo', id],
    queryFn: () => fetchTodo(id),
  })
}
```

## 문서 구조

- `docs/overview.md` - TanStack Query 개요
- `docs/quick-start.md` - 빠른 시작 가이드
- `docs/typescript.md` - TypeScript 사용법
- `docs/guides/` - 35개의 상세 가이드
  - `queries.md` - Query 기초
  - `mutations.md` - Mutation 기초
  - `caching.md` - 캐싱 전략
  - `query-invalidation.md` - 캐시 무효화
  - `optimistic-updates.md` - Optimistic Updates
  - `infinite-queries.md` - 무한 스크롤
  - `suspense.md` - Suspense 통합
  - `ssr.md`, `advanced-ssr.md` - SSR 가이드
  - `testing.md` - 테스트 가이드
- `docs/reference/` - 20개의 React Hook/컴포넌트 API 레퍼런스
- `docs/core-reference/` - 9개의 코어 클래스 API 레퍼런스

## v5 마이그레이션 주요 변경사항

자세한 내용은 `docs/guides/migrating-to-v5.md` 참조.

- `cacheTime` → `gcTime` 으로 이름 변경
- `useQuery`의 `onSuccess`, `onError`, `onSettled` 콜백 제거
- `status`에서 `loading` → `pending`으로 변경
- `isLoading` → `isPending` (캐시 데이터 없이 로딩 중)
- `isInitialLoading` → `isLoading` (백그라운드 포함 모든 로딩)
