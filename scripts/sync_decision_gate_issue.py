#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def fetch_issue_comments(repo: str, issue_number: int) -> list[dict[str, object]]:
    output = subprocess.check_output(
        [
            "gh",
            "issue",
            "view",
            str(issue_number),
            "--repo",
            repo,
            "--json",
            "comments",
        ],
        text=True,
    )
    payload = json.loads(output)
    comments = payload.get("comments", [])
    return comments if isinstance(comments, list) else []


def extract_decision_line(body: str) -> str | None:
    matches: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        lowered = line.casefold()
        if lowered == "decision: increment":
            matches.append("Decision: Increment")
        elif lowered == "decision: memo":
            matches.append("Decision: Memo")
        elif lowered == "decision: abstain":
            matches.append("Decision: Abstain")
    if len(matches) != 1:
        return None
    return matches[0]


def render_votes(comments: list[dict[str, object]]) -> str:
    lines = [
        "# Synced from GitHub decision-gate issue comments.",
        "# Only comments that contain an exact Decision line are included.",
        "# Allowed values: Decision: Increment | Decision: Memo | Decision: Abstain",
        "",
    ]
    included = 0
    for comment in comments:
        body = str(comment.get("body", ""))
        decision_line = extract_decision_line(body)
        if not decision_line:
            continue
        included += 1
        author = "unknown"
        author_data = comment.get("author")
        if isinstance(author_data, dict):
            author = str(author_data.get("login") or author)
        created_at = str(comment.get("createdAt", "")).strip()
        lines.extend(
            [
                f"Reviewer: {author}",
                decision_line,
                f"Source: GitHub issue comment on #{created_at}" if created_at else "Source: GitHub issue comment",
                "Reasoning:",
                body.strip(),
                "",
            ]
        )
    if included == 0:
        lines.extend(
            [
                "# No decision-bearing comments found yet.",
                "# Add reviewer comments to issue #16 using an exact Decision line.",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sync reviewer decision comments from the canonical GitHub issue into votes-raw.txt.")
    parser.add_argument("--repo", default="TakoVHS/CogniPrint")
    parser.add_argument("--issue", type=int, default=16)
    parser.add_argument("--output", type=Path, default=Path("docs/decisions/votes-raw.txt"))
    args = parser.parse_args(argv)

    comments = fetch_issue_comments(args.repo, args.issue)
    rendered = render_votes(comments)
    root = Path(__file__).resolve().parents[1]
    output_path = root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(f"Synced {len(comments)} comments from issue #{args.issue} into {output_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
