---
name: branch-doc-sync
description: Analyze current branch changes against a base branch, identify documentation that should be updated, and directly edit those docs. Use when asked to sync docs with branch changes before merge, release, or PR review.
---

# Branch Doc Sync

## Goal
Keep documentation aligned with implementation changes in the current working branch.

## Skill Resources
- Mapping template: `assets/config/docs-impact-map.yml`
- Local impact analyzer: `scripts/generate_doc_impact_report.py`
- Impact summary format: `references/report-format.md`

## Inputs
- Base branch (default: `origin/main`; fallback: `main`)
- Scope (`all changed files` or selected paths)
- Documentation targets (`README`, `docs/**`, module docs, runbooks)
- Language and style requirements

## Workflow
1. Collect branch deltas.
- Run `git diff --name-status <base>...HEAD` to capture changed files.
- Group changes by feature area (API, frontend, config, CI/CD, tests, deployment).

2. Map code changes to doc targets.
- Prefer explicit mapping file when present (for example `.github/docs-impact-map.yml`).
- If mapping is absent, derive by path heuristics and ownership.

3. Decide update actions.
- `update`: existing doc section is stale.
- `add`: missing section is required by new behavior.
- `no-change`: change is internal and docs remain valid.

4. Generate an impact summary.
- Use `scripts/generate_doc_impact_report.py` when a quick deterministic report is needed.
- Follow `references/report-format.md` for final summary structure.

5. Edit docs directly.
- Update affected docs in place with concrete behavior/config/command changes.
- Keep headings stable and preserve existing document style.
- Add short evidence notes (`Sources`) where appropriate.

6. Validate doc quality.
- Verify commands, env vars, file paths, and links.
- Ensure no claims contradict code/config.
- Summarize what was changed and why.

## Guardrails
- Do not edit product code unless explicitly requested.
- Do not invent undocumented behavior.
- Prefer minimal, targeted edits over broad rewrites.
- If evidence is insufficient, mark TODO/assumption explicitly.

## References
- Use `references/report-format.md` for impact summary/checklist format.
