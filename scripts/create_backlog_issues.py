#!/usr/bin/env python3
"""Create the VitalCare Release 1 backlog as GitHub issues.

Reads backlog/backlog.json and, for each item, creates a GitHub issue with
labels for epic, priority and type. Issues that already exist (same "[ID]"
prefix in the title) are skipped, so the script is safe to run more than once.

Only the GitHub REST API is used (through `gh api`), so the script also works
where GraphQL is unavailable. Adding issues to a GitHub Project (--project) is
the one step that needs GraphQL.

Requirements:
  - Python 3.9+
  - GitHub CLI (gh) installed and authenticated: `gh auth login`

Usage:
  # Preview what would be created (default, changes nothing):
  python scripts/create_backlog_issues.py --repo jeinando/VitalCare-Platform

  # Create labels and issues:
  python scripts/create_backlog_issues.py --repo jeinando/VitalCare-Platform --apply

  # Also add every new issue to a GitHub Project (number from the project URL):
  python scripts/create_backlog_issues.py --repo jeinando/VitalCare-Platform --apply \
      --project 1 --project-owner jeinando
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

BACKLOG_FILE = Path(__file__).resolve().parent.parent / "backlog" / "backlog.json"

EPIC_COLORS = {
    "E0": "6e7781",
    "E1": "0969da",
    "E2": "1b7c83",
    "E3": "1a7f37",
    "E4": "bf8700",
    "E5": "bc4c00",
    "E6": "cf222e",
    "E7": "bf3989",
    "E8": "8250df",
    "E9": "54aeff",
    "E10": "4ac26b",
}

PRIORITY_LABELS = {
    "Must": ("priority: must", "b60205", "MoSCoW: required for Release 1"),
    "Should": ("priority: should", "d93f0b", "MoSCoW: important, not blocking"),
    "Could": ("priority: could", "0e8a16", "MoSCoW: nice to have"),
    "Won't": ("priority: won't", "cccccc", "MoSCoW: out of this release"),
}

TYPE_LABELS = {
    "story": ("type: user story", "c5def5", "User-facing functionality"),
    "technical": ("type: technical", "bfd4f2", "Technical enabler"),
}


def run_gh(args: list[str], dry_run: bool, allow_fail: bool = False) -> subprocess.CompletedProcess | None:
    """Run a gh command, or print it when dry_run is True."""
    if dry_run:
        print("  [dry-run] gh " + " ".join(f'"{a}"' if " " in a else a for a in args))
        return None
    result = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0 and not allow_fail:
        sys.exit(f"gh {' '.join(args)} failed:\n{result.stderr.strip() or result.stdout.strip()}")
    return result


def api_post_json(path: str, payload: dict, dry_run: bool, method: str = "POST", allow_fail: bool = False):
    """Send a JSON payload to the GitHub REST API through `gh api`."""
    if dry_run:
        print(f"  [dry-run] gh api {path} --method {method} ({payload.get('title') or payload.get('name')})")
        return None
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as body_file:
        json.dump(payload, body_file, ensure_ascii=False)
        body_path = body_file.name
    try:
        return run_gh(["api", path, "--method", method, "--input", body_path], dry_run=False, allow_fail=allow_fail)
    finally:
        Path(body_path).unlink(missing_ok=True)


def epic_label(epic: str) -> tuple[str, str]:
    """Return the label name and color for an epic such as 'E3 Cotizador por reglas'."""
    code = epic.split(" ", 1)[0]
    return f"epic: {epic}", EPIC_COLORS.get(code, "ededed")


def build_body(item: dict) -> str:
    """Build the Markdown body of an issue from a backlog item."""
    criteria = "\n".join(f"- [ ] {line}" for line in item["acceptance_criteria"])
    references = item.get("references") or "None"
    return (
        f"## User story\n\n{item['story']}\n\n"
        f"## Acceptance criteria\n\n{criteria}\n\n"
        "## Details\n\n"
        "| Field | Value |\n| --- | --- |\n"
        f"| Backlog ID | {item['id']} |\n"
        f"| Epic | {item['epic']} |\n"
        f"| Priority | {item['priority']} |\n"
        f"| Story points (initial estimate) | {item['points']} |\n"
        f"| References | {references} |\n\n"
        "## Definition of Ready\n\n"
        "Before moving this issue to *Ready*, check the Definition of Ready in "
        "`docs/process/definition-of-ready-and-done.md`.\n"
    )


def ensure_labels(repo: str, items: list[dict], dry_run: bool) -> None:
    """Create or update every label the backlog needs."""
    print("Labels:")
    labels: dict[str, tuple[str, str]] = {}
    for item in items:
        name, color = epic_label(item["epic"])
        labels[name] = (color, f"Epic {item['epic']}")
    for name, color, description in PRIORITY_LABELS.values():
        labels[name] = (color, description)
    for name, color, description in TYPE_LABELS.values():
        labels[name] = (color, description)

    for name, (color, description) in labels.items():
        payload = {"name": name, "color": color, "description": description}
        result = api_post_json(f"repos/{repo}/labels", payload, dry_run, allow_fail=True)
        if result is not None and result.returncode != 0:
            # The label already exists: update its color and description instead.
            encoded = urllib.parse.quote(name, safe="")
            api_post_json(f"repos/{repo}/labels/{encoded}", payload, dry_run=False, method="PATCH")
        if not dry_run:
            print(f"  label ready: {name}")


def existing_ids(repo: str) -> set[str]:
    """Return backlog IDs that already have an issue, based on the '[ID]' title prefix."""
    result = run_gh(
        ["api", f"repos/{repo}/issues?state=all&per_page=100", "--paginate", "--jq", ".[].title"],
        dry_run=False,
    )
    ids = set()
    for title in result.stdout.splitlines():
        if title.startswith("[") and "]" in title:
            ids.add(title[1:title.index("]")])
    return ids


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", required=True, help="owner/repo, e.g. jeinando/VitalCare-Platform")
    parser.add_argument("--apply", action="store_true", help="create labels and issues (default is a dry run)")
    parser.add_argument("--project", type=int, help="GitHub Project number to add new issues to")
    parser.add_argument("--project-owner", help="owner of the GitHub Project (user or organization)")
    args = parser.parse_args()

    if args.project and not args.project_owner:
        parser.error("--project requires --project-owner")

    # Keep accented characters readable on Windows consoles.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    dry_run = not args.apply
    items = json.loads(BACKLOG_FILE.read_text(encoding="utf-8"))
    print(f"{len(items)} backlog items loaded from {BACKLOG_FILE.name}")
    if dry_run:
        print("Dry run: nothing will be created. Add --apply to create.\n")

    ensure_labels(args.repo, items, dry_run)

    skip = set() if dry_run else existing_ids(args.repo)
    created, skipped = 0, 0
    print("\nIssues:")
    for item in items:
        if item["id"] in skip:
            print(f"  skip {item['id']} (already exists)")
            skipped += 1
            continue

        title = f"[{item['id']}] {item['title']}"
        labels = [
            epic_label(item["epic"])[0],
            PRIORITY_LABELS[item["priority"]][0],
            TYPE_LABELS[item["type"]][0],
        ]
        payload = {"title": title, "body": build_body(item), "labels": labels}
        result = api_post_json(f"repos/{args.repo}/issues", payload, dry_run)
        url = json.loads(result.stdout)["html_url"] if result is not None else ""

        if url and args.project:
            run_gh(["project", "item-add", str(args.project), "--owner", args.project_owner, "--url", url], dry_run)

        print(f"  {'would create' if dry_run else 'created'} {title}" + (f" -> {url}" if url else ""))
        created += 1

    print(f"\nDone: {created} {'to create' if dry_run else 'created'}, {skipped} skipped.")


if __name__ == "__main__":
    main()
