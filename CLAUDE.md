# Claude Code Skills Repository

개인 Claude Code skills 저장소

## 커밋 컨벤션

### 커밋 타입

| 타입 | 설명 |
|------|------|
| feat | 새로운 skill 추가 |
| fix | skill 버그 수정 |
| docs | 문서 수정 (README 등) |
| refactor | skill 구조 개선 |
| chore | 기타 작업 |

### 커밋 메시지 형식

```
{타입}: {설명}
```

**설명은 한글로 작성합니다.**

### 예시

- `feat: SQLite skill 추가`
- `fix: React 성능 규칙 오타 수정`
- `docs: README 업데이트`

---

## Skill 생성 이력

| 날짜 | Skill | 설명 |
|------|-------|------|
| 2026-01-24 | `sqlite` | SQLite ORM 사용자 가이드 |
| 2026-01-24 | `vercel-react-best-practices` | Vercel React/Next.js 성능 최적화 |
| 2026-01-24 | `web-design-guidelines` | Web Interface Guidelines UI 리뷰 |

---

## 디렉토리 구조

```
~/.claude/skills/
├── CLAUDE.md           # 이 파일 (컨벤션 및 이력)
├── README.md           # Skills 목록 및 상세 설명
├── sqlite/
│   └── SKILL.md        # SQLite skill
├── vercel-react-best-practices/
│   └── SKILL.md        # React/Next.js 성능 skill
└── web-design-guidelines/
    └── SKILL.md        # UI 리뷰 skill
```

---

## 사용법

이 디렉토리(`~/.claude/skills/`)의 skills는 모든 프로젝트에서 자동으로 적용됩니다.

### 새 skill 추가 시

1. `{skill-name}/SKILL.md` 생성
2. YAML frontmatter 작성 (`name`, `description`)
3. README.md 테이블에 추가
4. 이 파일의 "Skill 생성 이력" 테이블에 추가
5. 커밋 및 push
