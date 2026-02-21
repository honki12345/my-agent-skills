#!/usr/bin/env python3
"""Generate documentation-impact report from local branch diff.

Usage:
  python scripts/generate_doc_impact_report.py --base origin/main
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


DEFAULT_MAP_PATH = Path(".github/docs-impact-map.yml")
DEFAULT_OUTPUT_DIR = Path("docs/impact-reports")
DEFAULT_DOC_EXTENSIONS = (".md", ".mdx", ".rst", ".adoc")
DEFAULT_DOC_PATH_PATTERNS = ("docs/**", "doc/**", "runbooks/**")
DEFAULT_DOC_EXCLUDE_PATTERNS = (".github/**",)


@dataclass
class ChangedFile:
    path: str
    status: str


@dataclass
class DocReviewDecision:
    path: str
    decision: str
    reasons: list[str]
    sources: list[str]


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def path_matches(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return path == prefix or path.startswith(f"{prefix}/")
    return PurePosixPath(path).match(pattern)


def load_mapping(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"rules": [], "heuristics": {}}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    data.setdefault("rules", [])
    data.setdefault("heuristics", {})
    return data


def get_changed_files(base: str, head: str) -> list[ChangedFile]:
    try:
        diff_output = run_git("diff", "--name-status", f"{base}...{head}")
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        raise RuntimeError(f"git diff failed for range {base}...{head}: {stderr}") from exc

    files: list[ChangedFile] = []
    if not diff_output:
        return files

    for raw in diff_output.splitlines():
        parts = raw.split("\t")
        if not parts:
            continue

        status = parts[0]
        # Rename format: R100 <old> <new> -> use new path
        if status.startswith("R") and len(parts) >= 3:
            path = parts[2]
        elif len(parts) >= 2:
            path = parts[1]
        else:
            continue

        files.append(ChangedFile(path=path, status=status))

    return files


def get_tracked_files() -> list[str]:
    output = run_git("ls-files")
    if not output:
        return []
    return [line.strip() for line in output.splitlines() if line.strip()]


def get_document_inventory(
    tracked_files: list[str], heuristics: dict[str, Any]
) -> list[str]:
    configured_exts = heuristics.get("doc_extensions")
    if isinstance(configured_exts, list) and configured_exts:
        doc_extensions = tuple(
            ext if ext.startswith(".") else f".{ext}"
            for ext in configured_exts
            if isinstance(ext, str) and ext.strip()
        )
    else:
        doc_extensions = DEFAULT_DOC_EXTENSIONS

    configured_patterns = heuristics.get("doc_path_patterns")
    if isinstance(configured_patterns, list) and configured_patterns:
        doc_path_patterns = tuple(
            pattern for pattern in configured_patterns if isinstance(pattern, str) and pattern.strip()
        )
    else:
        doc_path_patterns = DEFAULT_DOC_PATH_PATTERNS

    configured_excludes = heuristics.get("doc_exclude_patterns")
    if isinstance(configured_excludes, list) and configured_excludes:
        doc_exclude_patterns = tuple(
            pattern for pattern in configured_excludes if isinstance(pattern, str) and pattern.strip()
        )
    else:
        doc_exclude_patterns = DEFAULT_DOC_EXCLUDE_PATTERNS

    configured_include = heuristics.get("doc_include_files")
    doc_include_files: set[str] = set()
    if isinstance(configured_include, list):
        doc_include_files = {
            path for path in configured_include if isinstance(path, str) and path.strip()
        }

    inventory: list[str] = []
    for path in tracked_files:
        lower = path.lower()
        matched = lower.endswith(doc_extensions) or any(
            path_matches(path, pattern) for pattern in doc_path_patterns
        )
        if not matched and path in doc_include_files:
            matched = True
        if not matched:
            continue
        if any(path_matches(path, pattern) for pattern in doc_exclude_patterns):
            continue
        inventory.append(path)

    return sorted(set(inventory))


def apply_mapping_rules(
    files: list[ChangedFile], rules: list[dict[str, Any]]
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    impacted_docs: dict[str, list[str]] = defaultdict(list)
    doc_to_sources: dict[str, list[str]] = defaultdict(list)

    for changed in files:
        for rule in rules:
            patterns = rule.get("match", [])
            docs = rule.get("docs", [])
            rule_id = rule.get("id", "unnamed-rule")

            if any(path_matches(changed.path, pattern) for pattern in patterns):
                for doc_path in docs:
                    impacted_docs[doc_path].append(
                        f"Rule `{rule_id}` matched `{changed.path}`"
                    )
                    doc_to_sources[doc_path].append(changed.path)

    return impacted_docs, doc_to_sources


def apply_heuristics(
    files: list[ChangedFile],
    impacted_docs: dict[str, list[str]],
    doc_to_sources: dict[str, list[str]],
    heuristics: dict[str, Any],
) -> None:
    include_markdown_changes = bool(heuristics.get("include_markdown_changes", True))
    include_readme_by_default = bool(heuristics.get("include_readme_by_default", True))

    for changed in files:
        path = changed.path
        lower = path.lower()

        if include_markdown_changes and lower.endswith(".md"):
            impacted_docs[path].append("Markdown file changed directly")
            doc_to_sources[path].append(path)

        if path.startswith("api/"):
            impacted_docs["api/README.md"].append("Backend/API implementation changed")
            impacted_docs["README.md"].append("Top-level docs should reflect backend/API behavior")
            doc_to_sources["api/README.md"].append(path)
            doc_to_sources["README.md"].append(path)
        elif path.startswith("src/"):
            impacted_docs["README.md"].append("Frontend/runtime behavior changed")
            doc_to_sources["README.md"].append(path)
        elif path.startswith("tests/") or path.startswith("test/"):
            impacted_docs["tests/README.md"].append("Test behavior/layout changed")
            impacted_docs["README.md"].append("Top-level test instructions may need updates")
            doc_to_sources["tests/README.md"].append(path)
            doc_to_sources["README.md"].append(path)
        elif path.startswith(".github/workflows/"):
            impacted_docs["README.md"].append("CI/CD workflow changed")
            doc_to_sources["README.md"].append(path)
        elif path in {"Dockerfile", "Dockerfile-ollama-local", "docker-compose.yml", "run.sh"}:
            impacted_docs["README.md"].append("Deployment/runtime changed")
            impacted_docs["Ollama-instruction.md"].append("Container/Ollama runtime changed")
            doc_to_sources["README.md"].append(path)
            doc_to_sources["Ollama-instruction.md"].append(path)

    if include_readme_by_default:
        has_non_doc_change = any(not f.path.lower().endswith(".md") for f in files)
        if has_non_doc_change and "README.md" not in impacted_docs:
            impacted_docs["README.md"].append("Default docs review for code changes")
            for f in files:
                doc_to_sources["README.md"].append(f.path)


def dedupe_in_place(values: dict[str, list[str]]) -> None:
    for key, items in values.items():
        seen: set[str] = set()
        deduped: list[str] = []
        for item in items:
            if item not in seen:
                deduped.append(item)
                seen.add(item)
        values[key] = deduped


def build_doc_review_decisions(
    doc_inventory: list[str],
    impacted_docs: dict[str, list[str]],
    doc_to_sources: dict[str, list[str]],
) -> tuple[list[DocReviewDecision], list[DocReviewDecision]]:
    decisions: list[DocReviewDecision] = []
    inventory_set = set(doc_inventory)

    for doc_path in doc_inventory:
        reasons = impacted_docs.get(doc_path, [])
        sources = doc_to_sources.get(doc_path, [])
        if reasons:
            decision = "update"
            final_reasons = reasons
            final_sources = sources
        else:
            decision = "no-change"
            final_reasons = ["No matching rule/heuristic for current branch diff"]
            final_sources = []

        decisions.append(
            DocReviewDecision(
                path=doc_path,
                decision=decision,
                reasons=final_reasons,
                sources=final_sources,
            )
        )

    missing_candidates: list[DocReviewDecision] = []
    for doc_path in sorted(impacted_docs.keys()):
        if doc_path in inventory_set:
            continue
        missing_candidates.append(
            DocReviewDecision(
                path=doc_path,
                decision="add",
                reasons=impacted_docs.get(doc_path, []),
                sources=doc_to_sources.get(doc_path, []),
            )
        )

    return decisions, missing_candidates


def render_report(
    base: str,
    head: str,
    branch: str,
    files: list[ChangedFile],
    doc_inventory: list[str],
    decisions: list[DocReviewDecision],
    missing_candidates: list[DocReviewDecision],
    impacted_docs: dict[str, list[str]],
    doc_to_sources: dict[str, list[str]],
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lines: list[str] = []

    lines.append(f"# Branch Documentation Impact Report ({branch})")
    lines.append("")
    lines.append(f"Generated at: `{now}`")
    lines.append(f"Diff range: `{base}...{head}`")
    lines.append(f"Managed docs reviewed: `{len(doc_inventory)}`")
    lines.append(
        "Decision counts: "
        f"`update={sum(1 for d in decisions if d.decision == 'update')}`, "
        f"`no-change={sum(1 for d in decisions if d.decision == 'no-change')}`, "
        f"`add={len(missing_candidates)}`"
    )
    lines.append("")

    lines.append("## Changed Files")
    lines.append("")
    lines.append("| Status | Path |")
    lines.append("|---|---|")
    for f in files:
        lines.append(f"| `{f.status}` | `{f.path}` |")
    lines.append("")

    lines.append("## Managed Documentation Inventory")
    lines.append("")
    lines.append("| Doc Path | Decision | Why | Matched Source Files |")
    lines.append("|---|---|---|---|")
    for decision in decisions:
        reasons = "; ".join(decision.reasons)
        sources = ", ".join(f"`{p}`" for p in decision.sources)
        lines.append(
            f"| `{decision.path}` | `{decision.decision}` | {reasons} | {sources if sources else '-'} |"
        )
    lines.append("")

    lines.append("## Missing Documentation Candidates")
    lines.append("")
    if not missing_candidates:
        lines.append("- None")
    else:
        lines.append("| Doc Path | Decision | Why | Matched Source Files |")
        lines.append("|---|---|---|---|")
        for decision in missing_candidates:
            reasons = "; ".join(decision.reasons)
            sources = ", ".join(f"`{p}`" for p in decision.sources)
            lines.append(
                f"| `{decision.path}` | `{decision.decision}` | {reasons} | {sources if sources else '-'} |"
            )
    lines.append("")

    lines.append("## Documentation Impact Candidates")
    lines.append("")
    lines.append("| Doc Path | Why Impacted | Matched Source Files |")
    lines.append("|---|---|---|")
    for doc_path in sorted(impacted_docs.keys()):
        reasons = "; ".join(impacted_docs[doc_path])
        sources = ", ".join(f"`{p}`" for p in doc_to_sources.get(doc_path, []))
        lines.append(f"| `{doc_path}` | {reasons} | {sources} |")
    lines.append("")

    lines.append("## Update Checklist")
    lines.append("")
    for doc_path in sorted(d.path for d in decisions if d.decision == "update"):
        lines.append(f"- [ ] Update `{doc_path}`")
    for decision in missing_candidates:
        lines.append(f"- [ ] Add `{decision.path}`")
    lines.append("- [ ] Review all managed docs and confirm `no-change` decisions are valid")
    lines.append("- [ ] Validate commands and configuration snippets")
    lines.append("- [ ] Verify links and file-path references")
    lines.append("")

    return "\n".join(lines)


def sanitize_branch_name(branch: str) -> str:
    value = branch.replace("/", "-").replace(" ", "-")
    return "".join(ch for ch in value if ch.isalnum() or ch in {"-", "_", "."}).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate docs-impact report from local branch diff.")
    parser.add_argument("--base", default="origin/main", help="Base ref for diff (default: origin/main)")
    parser.add_argument("--head", default="HEAD", help="Head ref for diff (default: HEAD)")
    parser.add_argument("--map", dest="map_path", default=str(DEFAULT_MAP_PATH), help="Mapping file path")
    parser.add_argument("--output", default="", help="Output markdown path")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    if not repo_root.exists():
        print(f"Repository root does not exist: {repo_root}", file=sys.stderr)
        return 2

    try:
        # Ensure git commands run in repo root
        previous = Path.cwd()
        try:
            os.chdir(repo_root)
            branch = run_git("rev-parse", "--abbrev-ref", "HEAD")
            files = get_changed_files(args.base, args.head)
            mapping = load_mapping(Path(args.map_path))
            tracked_files = get_tracked_files()
        finally:
            os.chdir(previous)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        print(f"git command failed: {stderr}", file=sys.stderr)
        return 1

    impacted_docs, doc_to_sources = apply_mapping_rules(files, mapping.get("rules", []))
    apply_heuristics(files, impacted_docs, doc_to_sources, mapping.get("heuristics", {}))
    dedupe_in_place(impacted_docs)
    dedupe_in_place(doc_to_sources)
    doc_inventory = get_document_inventory(tracked_files, mapping.get("heuristics", {}))
    decisions, missing_candidates = build_doc_review_decisions(
        doc_inventory=doc_inventory,
        impacted_docs=impacted_docs,
        doc_to_sources=doc_to_sources,
    )

    report = render_report(
        base=args.base,
        head=args.head,
        branch=branch,
        files=files,
        doc_inventory=doc_inventory,
        decisions=decisions,
        missing_candidates=missing_candidates,
        impacted_docs=impacted_docs,
        doc_to_sources=doc_to_sources,
    )

    output_path: Path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = DEFAULT_OUTPUT_DIR / f"branch-{sanitize_branch_name(branch)}-impact.md"

    if not output_path.is_absolute():
        output_path = repo_root / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
