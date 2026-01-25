# GitHub GraphQL API - 쿼리 참조

## 개요

이 문서는 GitHub GraphQL API의 쿼리 형식을 설명합니다. "쿼리 형식은 서버의 데이터를 검색하는 GraphQL 작업을 정의합니다."

## 쿼리 정보

모든 GraphQL 스키마에는 쿼리 및 변형 모두에 대한 루트 형식이 있습니다.

**중요 참고사항:** 사용자 액세스 토큰으로 만든 GitHub App 요청의 경우, 이슈와 끌어오기 요청에 대해 별도의 쿼리를 사용해야 합니다.

## 주요 쿼리 목록

### 코드 행동강령
| 쿼리 | 설명 |
|------|------|
| `codeOfConduct` | 키로 코드 행동강령 조회 |
| `codesOfConduct` | 코드 행동강령 목록 조회 |

### 엔터프라이즈
| 쿼리 | 설명 |
|------|------|
| `enterprise` | URL slug로 엔터프라이즈 조회 |
| `enterpriseAdministratorInvitation` | 관리자 초대 조회 |
| `enterpriseAdministratorInvitationByToken` | 토큰으로 관리자 초대 조회 |
| `enterpriseMemberInvitation` | 멤버 초대 조회 |
| `enterpriseMemberInvitationByToken` | 토큰으로 멤버 초대 조회 |

### 라이선스
| 쿼리 | 설명 |
|------|------|
| `license` | 키로 오픈소스 라이선스 조회 |
| `licenses` | 알려진 오픈소스 라이선스 목록 반환 |

### 마켓플레이스
| 쿼리 | 설명 |
|------|------|
| `marketplaceCategories` | 마켓플레이스 카테고리 알파벳순 조회 |
| `marketplaceCategory` | slug로 카테고리 조회 |
| `marketplaceListing` | 단일 마켓플레이스 목록 조회 |
| `marketplaceListings` | 마켓플레이스 목록 조회 |

### 메타데이터 및 노드
| 쿼리 | 설명 |
|------|------|
| `meta` | GitHub 인스턴스 정보 반환 |
| `node` | ID로 객체 조회 |
| `nodes` | ID 목록으로 노드 조회 |

### 조직 및 사용자
| 쿼리 | 설명 |
|------|------|
| `organization` | 로그인으로 조직 조회 |
| `user` | 로그인으로 사용자 조회 |
| `viewer` | 현재 인증된 사용자 정보 |

### 저장소
| 쿼리 | 설명 |
|------|------|
| `repository` | 소유자 및 저장소 이름으로 조회 |
| `repositoryOwner` | 로그인으로 저장소 소유자 조회 |

### 검색 및 리소스
| 쿼리 | 설명 |
|------|------|
| `search` | 최대 1,000개 결과를 반환하며 리소스 검색 |
| `resource` | URL로 리소스 조회 |

### 보안
| 쿼리 | 설명 |
|------|------|
| `securityAdvisories` | GitHub 보안 권고 조회 |
| `securityAdvisory` | GHSA ID로 보안 권고 조회 |
| `securityVulnerabilities` | GitHub 보안 권고로 문서화된 소프트웨어 취약점 조회 |

### 기타
| 쿼리 | 설명 |
|------|------|
| `rateLimit` | 클라이언트 속도 제한 정보 |
| `relay` | Relay 호환성을 위한 쿼리 객체 재노출 |
| `sponsorables` | GitHub Sponsors를 통해 후원할 수 있는 사용자 및 조직 |
| `topic` | 이름으로 주제 조회 |

## 인수 유형

쿼리는 다양한 인수를 지원합니다:

| 유형 | 설명 |
|------|------|
| `String` | 텍스트 값 |
| `Boolean` | 참/거짓 값 |
| `Int` | 정수 |
| `ID` | 고유 식별자 |
| `DateTime` | 날짜/시간 값 |
| `URI` | 웹 주소 |

## 추가 자료

- GraphQL API 정보
- 호환성이 손상되는 변경
- 속도 및 쿼리 제한
- GraphQL 소개 가이드
- GraphQL을 사용하여 호출 형성
