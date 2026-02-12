---
name: obsidian-cli
description: Obsidian CLI 명령어 레퍼런스. obsidian 명령어, 볼트 관리, 파일 조작, 검색, 플러그인 관리, 개발자 도구 등. Obsidian CLI 관련 작업 시 자동 로드.
---

# Obsidian CLI Reference

Obsidian CLI는 터미널에서 Obsidian을 제어하는 CLI 도구. Obsidian 1.12+ (Early Access) 필요.

> Obsidian이 실행 중이어야 하며, 미실행 시 첫 명령이 Obsidian을 시작함.

## 기본 사용법

```bash
# 단일 명령 실행
obsidian <command> [params] [flags]

# TUI (대화형 터미널) 모드
obsidian
```

### 파라미터와 플래그

- **파라미터**: `key=value` 형식. 공백 포함 시 따옴표: `name="My Note"`
- **플래그**: 불리언 스위치. 이름만 포함: `silent`, `overwrite`
- **멀티라인**: `\n` (줄바꿈), `\t` (탭)
- **출력 복사**: `--copy` 추가

### 볼트/파일 타겟팅

```bash
# 볼트 지정 (첫 번째 파라미터)
obsidian vault="My Vault" <command>

# 파일 지정 (wikilink 방식 vs 정확한 경로)
obsidian read file=Recipe        # 이름으로 (wikilink 해석)
obsidian read path="folder/Recipe.md"  # 정확한 경로
```

- `file=<name>`: wikilink 방식 (확장자/경로 불필요)
- `path=<path>`: 볼트 루트 기준 정확한 경로

## 명령어 요약

### 일반

| 명령어 | 설명 |
|--------|------|
| `help` | 사용 가능한 명령어 목록 |
| `version` | Obsidian 버전 표시 |
| `reload` | 앱 창 새로고침 |
| `restart` | 앱 재시작 |

### 파일/폴더 관리

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `file` | 파일 정보 표시 | `file=`, `path=` |
| `files` | 볼트 파일 목록 | `folder=`, `ext=`, `total` |
| `folder` | 폴더 정보 | `path=` (required), `info=files\|folders\|size` |
| `folders` | 폴더 목록 | `folder=`, `total` |
| `open` | 파일 열기 | `file=`, `path=`, `newtab` |
| `create` | 파일 생성 | `name=`, `content=`, `template=`, `overwrite`, `silent` |
| `read` | 파일 읽기 | `file=`, `path=` |
| `append` | 파일 끝에 추가 | `content=` (required), `inline` |
| `prepend` | frontmatter 뒤에 추가 | `content=` (required), `inline` |
| `move` | 파일 이동/이름 변경 | `to=` (required) |
| `delete` | 파일 삭제 (기본: 휴지통) | `permanent` |

### Daily Notes

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `daily` | 오늘의 데일리 노트 열기 | `silent`, `paneType=` |
| `daily:read` | 데일리 노트 읽기 | - |
| `daily:append` | 데일리 노트 끝에 추가 | `content=` (required), `silent`, `inline` |
| `daily:prepend` | 데일리 노트 앞에 추가 | `content=` (required), `silent`, `inline` |

### 검색

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `search` | 볼트 텍스트 검색 | `query=` (required), `path=`, `limit=`, `format=`, `total`, `matches`, `case` |
| `search:open` | 검색 뷰 열기 | `query=` |

### 태그

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `tags` | 태그 목록 | `all`, `total`, `counts`, `sort=count` |
| `tag` | 태그 정보 | `name=` (required), `total`, `verbose` |

### 작업(Tasks)

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `tasks` | 작업 목록 | `all`, `daily`, `total`, `done`, `todo`, `verbose`, `status=` |
| `task` | 작업 표시/수정 | `ref=path:line`, `toggle`, `done`, `todo`, `status=` |

### 속성(Properties)

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `properties` | 속성 목록 | `all`, `total`, `counts`, `format=yaml\|tsv` |
| `property:set` | 속성 설정 | `name=` (required), `value=` (required), `type=` |
| `property:remove` | 속성 삭제 | `name=` (required) |
| `property:read` | 속성 읽기 | `name=` (required) |

### 링크

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `backlinks` | 백링크 목록 | `counts`, `total` |
| `links` | 아웃고잉 링크 목록 | `total` |
| `unresolved` | 미해결 링크 | `total`, `counts`, `verbose` |
| `orphans` | 들어오는 링크 없는 파일 | `total`, `all` |
| `deadends` | 나가는 링크 없는 파일 | `total`, `all` |

### 북마크

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `bookmarks` | 북마크 목록 | `total`, `verbose` |
| `bookmark` | 북마크 추가 | `file=`, `folder=`, `search=`, `url=`, `title=` |

### 플러그인

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `plugins` | 설치된 플러그인 목록 | `filter=core\|community`, `versions` |
| `plugins:enabled` | 활성화된 플러그인 목록 | `filter=`, `versions` |
| `plugin` | 플러그인 정보 | `id=` (required) |
| `plugin:enable` | 플러그인 활성화 | `id=` (required) |
| `plugin:disable` | 플러그인 비활성화 | `id=` (required) |
| `plugin:install` | 커뮤니티 플러그인 설치 | `id=` (required), `enable` |
| `plugin:uninstall` | 플러그인 삭제 | `id=` (required) |
| `plugin:reload` | 플러그인 재로드 | `id=` (required) |

### 템플릿

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `templates` | 템플릿 목록 | `total` |
| `template:read` | 템플릿 읽기 | `name=` (required), `resolve`, `title=` |
| `template:insert` | 템플릿 삽입 | `name=` (required) |

### 파일 히스토리 & Diff

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `diff` | 버전 비교 | `from=`, `to=`, `filter=local\|sync` |
| `history` | 로컬 히스토리 목록 | `file=`, `path=` |
| `history:read` | 히스토리 버전 읽기 | `version=` |
| `history:restore` | 히스토리 버전 복원 | `version=` (required) |

### Sync

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `sync` | 동기화 일시정지/재개 | `on`, `off` |
| `sync:status` | 동기화 상태 | - |
| `sync:history` | 파일 동기화 히스토리 | `total` |
| `sync:read` | 동기화 버전 읽기 | `version=` (required) |
| `sync:restore` | 동기화 버전 복원 | `version=` (required) |
| `sync:deleted` | 삭제된 파일 목록 | `total` |

### Publish

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `publish:site` | 퍼블리시 사이트 정보 | - |
| `publish:list` | 퍼블리시된 파일 목록 | `total` |
| `publish:status` | 퍼블리시 변경사항 | `new`, `changed`, `deleted` |
| `publish:add` | 파일 퍼블리시 | `changed` |
| `publish:remove` | 퍼블리시 해제 | - |

### 볼트/워크스페이스

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `vault` | 볼트 정보 | `info=name\|path\|files\|folders\|size` |
| `vaults` | 알려진 볼트 목록 | `total`, `verbose` |
| `workspace` | 워크스페이스 트리 | `ids` |
| `workspaces` | 저장된 워크스페이스 목록 | `total` |
| `workspace:save` | 워크스페이스 저장 | `name=` |
| `workspace:load` | 워크스페이스 로드 | `name=` (required) |
| `workspace:delete` | 워크스페이스 삭제 | `name=` (required) |
| `tabs` | 열린 탭 목록 | `ids` |
| `tab:open` | 새 탭 열기 | `group=`, `file=`, `view=` |
| `recents` | 최근 파일 목록 | `total` |

### 테마/스니펫

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `themes` | 설치된 테마 목록 | `versions` |
| `theme:set` | 활성 테마 설정 | `name=` (required) |
| `theme:install` | 커뮤니티 테마 설치 | `name=` (required), `enable` |
| `theme:uninstall` | 테마 삭제 | `name=` (required) |
| `snippets` | CSS 스니펫 목록 | - |
| `snippet:enable` | CSS 스니펫 활성화 | `name=` (required) |
| `snippet:disable` | CSS 스니펫 비활성화 | `name=` (required) |

### 기타

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `outline` | 파일 헤딩 구조 | `format=tree\|md`, `total` |
| `aliases` | 별칭 목록 | `all`, `total`, `verbose` |
| `wordcount` | 단어/문자 수 | `words`, `characters` |
| `random` | 랜덤 노트 열기 | `folder=`, `newtab`, `silent` |
| `unique` | 고유 노트 생성 | `name=`, `content=`, `silent` |
| `web` | URL을 웹 뷰어에서 열기 | `url=` (required), `newtab` |

### Bases

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `bases` | .base 파일 목록 | - |
| `base:views` | 현재 base 뷰 목록 | - |
| `base:create` | base 뷰에 항목 생성 | `name=`, `content=`, `silent`, `newtab` |
| `base:query` | base 쿼리/결과 반환 | `file=`, `view=`, `format=json\|csv\|tsv\|md\|paths` |

### 개발자 도구

| 명령어 | 설명 | 주요 파라미터 |
|--------|------|---------------|
| `devtools` | 개발자 도구 토글 | - |
| `dev:debug` | Chrome DevTools 디버거 연결 | `on`, `off` |
| `dev:cdp` | Chrome DevTools Protocol 명령 | `method=` (required), `params=` |
| `dev:errors` | JS 에러 표시 | `clear` |
| `dev:screenshot` | 스크린샷 (base64 PNG) | `path=` |
| `dev:console` | 콘솔 메시지 표시 | `limit=`, `level=`, `clear` |
| `dev:css` | CSS 검사 | `selector=` (required), `prop=` |
| `dev:dom` | DOM 요소 쿼리 | `selector=` (required), `attr=`, `css=`, `text`, `inner`, `all` |
| `dev:mobile` | 모바일 에뮬레이션 토글 | `on`, `off` |
| `eval` | JavaScript 실행 | `code=` (required) |

## 실용 예시

```bash
# 데일리 노트에 할 일 추가
obsidian daily:append content="- [ ] Buy groceries" silent

# 볼트 전체 검색
obsidian search query="meeting notes" matches

# 템플릿으로 새 노트 생성
obsidian create name="Trip to Paris" template=Travel

# 태그 카운트 포함 목록
obsidian tags all counts sort=count

# 플러그인 개발 시 리로드
obsidian plugin:reload id=my-plugin

# 앱 콘솔에서 JS 실행
obsidian eval code="app.vault.getFiles().length"

# 파일 버전 비교
obsidian diff file=README from=1 to=3

# 스크린샷 촬영
obsidian dev:screenshot path=screenshot.png

# 작업 완료 처리
obsidian task ref="Recipe.md:8" done

# 속성 설정
obsidian property:set name=status value=draft type=text
```
