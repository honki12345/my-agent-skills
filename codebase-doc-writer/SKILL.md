---
name: codebase-doc-writer
description: Read a software repository and generate or refresh technical documentation from source code and configuration. Use when asked to document a project, build a wiki-style doc set, or update docs based on implementation changes.
---

# Codebase Doc Writer

## Goal
Produce accurate, implementation-grounded documentation by reading the repository directly.

## Inputs
- Repository root path
- Target output paths (for example: `docs/overview.md`, `docs/architecture.md`)
- Scope (`full` or selected modules)
- Language and audience (developer/onboarding/ops)

## Workflow
1. Build a repo map.
- List directories and major entry points.
- Identify backend/frontend/runtime boundaries and external integrations.

2. Extract implementation facts.
- Prefer source over README claims when they conflict.
- Capture concrete references (file path + function/route/component).

3. Derive documentation sections.
- Overview: problem, capabilities, constraints.
- Architecture: components, data flow, boundaries.
- Runtime/API: endpoints, request/response behavior, auth, error paths.
- Configuration/Operations: env vars, deployment, observability.
- Contribution notes: tests, workflows, extension points.

4. Write docs with traceability.
- Keep every section verifiable from code.
- Add a short `Sources` line with relevant file paths.

5. Validate coverage and drift.
- Ensure all major modules are represented.
- Mark unknown/implicit behavior explicitly instead of guessing.

## Quality Rules
- Do not invent features.
- Prefer concise tables for config and endpoints.
- Use diagrams only when they improve comprehension.
- Keep docs update-friendly: stable headings and clear section ownership.

## Reference
- Use `references/doc-pack-template.md` as the default structure.
