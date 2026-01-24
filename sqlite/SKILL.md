---
name: sqlite
description: SQLite 데이터베이스 가이드. TypeORM/Prisma 등 ORM 사용 시 알아야 할 SQLite 특성, 마이그레이션 제한사항, 동시성 처리, 성능 최적화 참조. .db, .sqlite 파일 작업 시 자동 적용.
---

# SQLite 가이드 (ORM 사용자용)

## 필수 초기 설정

```sql
PRAGMA journal_mode = WAL;        -- 동시성 향상 (필수)
PRAGMA synchronous = NORMAL;      -- 성능/안전성 균형
PRAGMA foreign_keys = ON;         -- 외래키 강제 (기본값 OFF!)
PRAGMA busy_timeout = 5000;       -- 잠금 대기 5초
PRAGMA cache_size = -64000;       -- 64MB 캐시
```

> TypeORM에서는 `extra` 옵션으로 설정

---

## 핵심 Quirks (함정)

### 1. Foreign Key 기본 비활성화
```
매 연결마다 PRAGMA foreign_keys = ON 필요!
ORM 설정에서 반드시 활성화할 것
```

### 2. 유연한 타입 시스템
```
INTEGER 컬럼에 문자열 삽입 가능 (에러 안 남!)
해결: STRICT 테이블 사용 (SQLite 3.37.0+)
```

### 3. PRIMARY KEY가 NULL 허용
```
NOT NULL 명시 필요: id INTEGER PRIMARY KEY NOT NULL
```

### 4. BOOLEAN/DATETIME 타입 없음
```
Boolean: 0/1 정수로 저장
DateTime: TEXT('YYYY-MM-DD HH:MM:SS'), INTEGER(Unix timestamp), REAL(Julian day)
```

### 5. 대소문자 구분
```
ASCII만 NOCASE 지원, 유니코드 대소문자 구분됨
```

---

## 마이그레이션 제한사항 (중요!)

### ALTER TABLE 지원 현황

| 작업 | 지원 | 버전 |
|------|------|------|
| 테이블 이름 변경 | ✅ | - |
| 컬럼 이름 변경 | ✅ | 3.25.0+ |
| 컬럼 추가 | ✅ | - |
| 컬럼 삭제 | ✅ | 3.35.0+ |
| 컬럼 타입 변경 | ❌ | - |
| 제약조건 추가/삭제 | ❌ | - |
| PRIMARY KEY 변경 | ❌ | - |

### 컬럼 추가 제한
```
- PRIMARY KEY/UNIQUE 불가
- NOT NULL 시 기본값 필수
- GENERATED ALWAYS ... STORED 불가
```

### 컬럼 삭제 불가 조건
```
- PRIMARY KEY 또는 UNIQUE
- 인덱스에 포함됨
- FOREIGN KEY에 사용됨
- 트리거/뷰에 참조됨
```

### 타입 변경이 필요한 경우
```
1. 새 테이블 생성
2. 데이터 복사
3. 기존 테이블 삭제
4. 새 테이블 이름 변경
5. 인덱스/트리거/뷰 재생성
```

> TypeORM: synchronize:false 권장, 마이그레이션 직접 작성

---

## 동시성 & 락킹

### 5가지 락 상태
| 상태 | 설명 |
|------|------|
| UNLOCKED | 락 없음 |
| SHARED | 읽기 중 (다중 허용) |
| RESERVED | 쓰기 예정 (단일) |
| PENDING | 쓰기 대기 (새 읽기 차단) |
| EXCLUSIVE | 쓰기 중 (단독) |

### SQLITE_BUSY 에러
```
원인: 다른 연결이 락 보유 중
해결:
1. busy_timeout 설정 (PRAGMA busy_timeout = 5000)
2. WAL 모드 사용
3. 재시도 로직 구현
```

### WAL 모드 장점
```
- 읽기/쓰기 동시 가능
- 더 빠른 성능
- 읽기가 쓰기를 차단하지 않음
```

### WAL 모드 주의사항
```
- 네트워크 드라이브 미지원
- -wal, -shm 추가 파일 생성
- 100MB+ 트랜잭션은 롤백 저널이 나음
```

---

## 제한사항

| 항목 | 기본값 | 최대값 |
|------|--------|--------|
| DB 크기 | - | 281 TB |
| 행 크기 | 1 GB | 2 GB |
| 컬럼 수 | 2,000 | 32,767 |
| JOIN 테이블 | - | 64 |
| ATTACH DB 수 | 10 | 125 |
| SQL 길이 | 1 GB | 1 GB |

### 실제 권장값
```
컬럼 수: 100개 이하 (정규화 권장)
동시 연결: WAL 모드로 동시성 확보
```

---

## 백업

### 안전한 백업 방법
```
1. 온라인 백업 API 사용 (sqlite3_backup_*)
2. VACUUM INTO 'backup.db'
3. .backup 명령 (CLI)
```

### 주의사항
```
- 단순 파일 복사 시 쓰기 중이면 손상 가능
- WAL 모드: -wal, -shm 파일도 함께 백업 필요
- 백업 중에도 읽기/쓰기 가능 (온라인 백업)
```

---

## 인덱스 최적화

### 인덱스 사용 조건
```
복합 인덱스 (a, b, c)의 경우:
✅ WHERE a=? AND b=? AND c=?
✅ WHERE a=? AND b=?
✅ WHERE a=?
❌ WHERE b=?  (첫 컬럼 없음)
❌ WHERE a=? OR b=?  (OR 조건)
```

### ANALYZE 필수
```sql
ANALYZE;  -- 통계 수집
PRAGMA optimize;  -- 연결 종료 전 실행
```

### EXPLAIN 사용
```sql
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = ?;
-- SEARCH TABLE users USING INDEX idx_email (email=?)
```

---

## TypeORM 연동

### DataSource 설정
```typescript
{
  type: 'sqlite',
  database: 'db.sqlite',
  synchronize: false,  // 프로덕션에서 false!
}
```

### better-sqlite3 드라이버 PRAGMA 설정
```typescript
{
  type: 'better-sqlite3',
  prepareDatabase: (db) => {
    db.pragma('journal_mode = WAL');
    db.pragma('foreign_keys = ON');
    db.pragma('busy_timeout = 5000');
  }
}
```

### 날짜 타입 주의
```typescript
// SQLite는 Date 타입이 없음
@Column({ type: 'text' })  // ISO8601 문자열
createdDate: string;

// 또는 timestamp
@Column({ type: 'integer' })
createdAt: number;  // Unix timestamp
```

### 마이그레이션 주의사항
```typescript
// 컬럼 타입 변경 시 직접 SQL 작성 필요
public async up(queryRunner: QueryRunner): Promise<void> {
  // 1. 임시 테이블 생성
  // 2. 데이터 복사
  // 3. 원본 삭제
  // 4. 이름 변경
}
```

---

## 참조 링크

- [Quirks](https://www.sqlite.org/quirks.html) - 함정과 주의사항
- [Pragmas](https://www.sqlite.org/pragma.html) - 설정 옵션
- [ALTER TABLE](https://www.sqlite.org/lang_altertable.html) - 스키마 변경
- [WAL Mode](https://www.sqlite.org/wal.html) - 동시성 향상
- [Locking](https://www.sqlite.org/lockingv3.html) - 락킹 메커니즘
- [Limits](https://www.sqlite.org/limits.html) - 제한사항
- [Query Optimizer](https://www.sqlite.org/optoverview.html) - 쿼리 최적화
