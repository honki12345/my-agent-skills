---
name: branch-doc-sync
description: Analyze current branch changes against a base branch, build a full inventory of managed docs, review each doc for impact, and directly edit all required docs. Use when asked to sync docs with branch changes before merge, release, or PR review.
---

# Branch Doc Sync

## Goal
Keep documentation aligned with implementation changes in the current working branch by reviewing all managed docs one by one.

## Skill Resources
- Mapping template: `assets/config/docs-impact-map.yml`
- Local impact analyzer: `scripts/generate_doc_impact_report.py`
- Impact summary format: `references/report-format.md`

## Inputs
- Base branch (default: `origin/main`; fallback: `main`)
- Scope (`all changed files` or selected paths)
- Managed-doc definition (`doc_extensions`, `doc_path_patterns`, include/exclude patterns)
- Language and style requirements

## Workflow
1. Collect branch deltas.
- Run `git diff --name-status <base>...HEAD` to capture changed files.
- Group changes by feature area (API, frontend, config, CI/CD, tests, deployment).

2. Build full managed-doc inventory.
- Run `git ls-files` and enumerate all tracked docs using extension/path rules.
- Default doc rules: `.md`, `.mdx`, `.rst`, `.adoc`, plus `docs/**`/`doc/**`/`runbooks/**`.
- Allow project-specific overrides in mapping heuristics.

3. Map code changes to doc targets.
- Prefer explicit mapping file when present (for example `.github/docs-impact-map.yml`).
- If mapping is absent, derive by path heuristics and ownership.

4. Perform exhaustive doc-by-doc review.
- For every managed doc in inventory, assign exactly one decision:
  - `update`: existing content is stale or incomplete.
  - `no-change`: still accurate for current diff.
- For mapped docs that do not exist in inventory, mark `add`.
- Do not skip docs; if inventory is large, review in batches and preserve full coverage.

5. Generate an impact summary.
- Use `scripts/generate_doc_impact_report.py` for deterministic inventory + decision matrix output.
- Follow `references/report-format.md` for final summary structure.

6. Edit docs directly.
- Read each `update`/`add` target doc before editing.
- Update affected docs in place with concrete behavior/config/command changes.
- Keep headings stable and preserve existing document style.
- Add short evidence notes (`Sources`) where appropriate.

7. Validate doc quality.
- Confirm every managed doc has a review decision in the matrix.
- Verify commands, env vars, file paths, and links.
- Ensure no claims contradict code/config.
- Summarize what was changed and why.

## Guardrails
- Do not edit product code unless explicitly requested.
- Do not invent undocumented behavior.
- Prefer minimal, targeted edits over broad rewrites.
- Do not mark `no-change` without a concrete reason tied to current diff.
- If evidence is insufficient, mark TODO/assumption explicitly.

## References
- Use `references/report-format.md` for impact summary/checklist format.
