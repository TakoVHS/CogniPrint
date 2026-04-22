"""Campaign-level empirical workflows for CogniPrint."""

from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .perturbation import create_perturbation_lab
from .reporting.notes import generate_empirical_notes
from .workstation import DISCLAIMER, ensure_workspace


def run_campaign(config: dict[str, Any], *, config_path: Path, workspace: Path) -> Path:
    ensure_workspace(workspace)
    name = _required_string(config, "name")
    campaign_id = _slug(config.get("campaign_id") or name)
    campaign_dir = workspace / "campaigns" / campaign_id
    if campaign_dir.exists():
        raise FileExistsError(f"Campaign directory already exists: {campaign_dir}")
    for relative in ["studies", "reports", "exports", "latex"]:
        (campaign_dir / relative).mkdir(parents=True, exist_ok=True)

    base_dir = config_path.parent
    series_entries = config.get("series")
    if not isinstance(series_entries, list) or not series_entries:
        raise ValueError("Campaign config requires a non-empty `series` list.")

    series_records = []
    for index, entry in enumerate(series_entries, start=1):
        if not isinstance(entry, dict):
            raise ValueError("Each campaign series entry must be a mapping.")
        series_name = _required_string(entry, "name")
        lab_id = f"{campaign_id}-{_slug(series_name)}"
        lab_dir = create_perturbation_lab(
            workspace=workspace,
            name=series_name,
            lab_id=lab_id,
            baseline_file=_resolve(base_dir, _required_string(entry, "baseline_file")),
            light_file=_optional_path(base_dir, entry.get("light_file")),
            strong_file=_optional_path(base_dir, entry.get("strong_file")),
            variant_files=[_resolve(base_dir, str(path)) for path in entry.get("variant_files", [])],
            variant_folder=_optional_path(base_dir, entry.get("variant_folder")),
            cli_args={"campaign_config": str(config_path), "series_index": index},
        )
        study_copy = campaign_dir / "studies" / lab_id
        shutil.copytree(lab_dir / "study", study_copy)
        notes_dir = campaign_dir / "reports" / lab_id
        generate_empirical_notes(study_copy, notes_dir)
        series_records.append(
            {
                "series_name": series_name,
                "perturbation_dir": str(lab_dir),
                "study_dir": str(study_copy),
                "notes_dir": str(notes_dir),
            }
        )

    manifest = {
        "campaign_id": campaign_id,
        "name": name,
        "description": config.get("description"),
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "config_path": str(config_path),
        "series_count": len(series_records),
        "series": series_records,
        "interpretive_note": DISCLAIMER,
    }
    _write_json(campaign_dir / "manifest.json", manifest)
    summarize_campaign(campaign_dir)
    return campaign_dir


def summarize_campaign(campaign_dir: Path) -> Path:
    manifest_path = campaign_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"campaign_id": campaign_dir.name, "name": campaign_dir.name}
    rows = _collect_rows(campaign_dir)
    result = {
        "campaign_id": manifest.get("campaign_id", campaign_dir.name),
        "name": manifest.get("name", campaign_dir.name),
        "series_count": manifest.get("series_count", len({row["series_name"] for row in rows})),
        "comparison_count": len(rows),
        "rows": rows,
        "interpretive_note": DISCLAIMER,
    }
    _write_json(campaign_dir / "campaign-results.json", result)
    _write_csv(campaign_dir / "campaign-results.csv", rows)
    _write_summary(campaign_dir / "campaign-summary.md", result)
    _write_appendix(campaign_dir / "manuscript-appendix.md", result)
    _write_latex(campaign_dir / "latex" / "campaign-summary-table.tex", rows)
    reports_dir = campaign_dir / "reports"
    reports_dir.mkdir(exist_ok=True)
    _write_paper_materials(reports_dir, result)
    return campaign_dir


def _collect_rows(campaign_dir: Path) -> list[dict[str, Any]]:
    rows = []
    for study_dir in sorted((campaign_dir / "studies").iterdir() if (campaign_dir / "studies").exists() else []):
        if not study_dir.is_dir():
            continue
        aggregated_path = study_dir / "aggregated-results.json"
        if not aggregated_path.exists():
            continue
        aggregated = json.loads(aggregated_path.read_text(encoding="utf-8"))
        for row in aggregated.get("comparison_rows", []):
            rows.append(
                {
                    "series_name": aggregated.get("name", study_dir.name),
                    "study_id": aggregated.get("study_id", study_dir.name),
                    "variant_label": row.get("variant_label", "variant"),
                    "cosine_similarity": row.get("cosine_similarity"),
                    "euclidean_distance": row.get("euclidean_distance"),
                    "manhattan_distance": row.get("manhattan_distance"),
                    "interpretation": row.get("interpretation", "review in context"),
                }
            )
    return rows


def _write_summary(path: Path, result: dict[str, Any]) -> None:
    lines = [
        "# CogniPrint Empirical Campaign Summary",
        "",
        f"- Campaign: `{result['name']}`",
        f"- Series count: `{result['series_count']}`",
        f"- Comparison rows: `{result['comparison_count']}`",
        "",
        "## Interpretation Boundary",
        "",
        DISCLAIMER,
        "",
        "## Observed Patterns",
        "",
        "| Series | Variant | Cosine similarity signal | Euclidean distance metric | Comparative regularity |",
        "|---|---|---:|---:|---|",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['series_name']} | {row['variant_label']} | `{row['cosine_similarity']}` | `{row['euclidean_distance']}` | {row['interpretation']} |"
        )
    lines.extend(["", "Use this campaign summary to select follow-up studies and draft empirical appendices.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_appendix(path: Path, result: dict[str, Any]) -> None:
    lines = [
        "# Empirical Appendix Draft",
        "",
        "This appendix summarizes repeated CogniPrint perturbation series as profile-level observations.",
        "",
        "## Campaign Design",
        "",
        f"The campaign `{result['name']}` contains `{result['series_count']}` perturbation series and `{result['comparison_count']}` comparison rows.",
        "",
        "## Summary Table",
        "",
        "| Series | Variant | Profile shift metric | Stability signal |",
        "|---|---|---:|---|",
    ]
    for row in result["rows"]:
        lines.append(f"| {row['series_name']} | {row['variant_label']} | `{row['euclidean_distance']}` | {row['interpretation']} |")
    lines.extend(["", "All statements should remain tied to observed metric patterns and repeated local validation.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_paper_materials(reports_dir: Path, result: dict[str, Any]) -> None:
    materials = {
        "paper-outline.md": [
            "# Follow-Up Preprint Outline",
            "",
            "## Working Focus",
            "Empirical stability of CogniPrint profile representations under controlled text perturbations.",
            "",
            "## Sections",
            "- Introduction and motivation",
            "- Deterministic profile construction",
            "- Perturbation campaign design",
            "- Observed stability patterns",
            "- Limitations and future validation",
            "",
        ],
        "methods-section-draft.md": [
            "# Methods Section Draft",
            "",
            f"The campaign contains `{result['series_count']}` locally reproducible perturbation series. Each series compares one baseline profile against controlled variants and records metric deltas, profile shifts, and comparison signals.",
            "",
        ],
        "results-section-draft.md": [
            "# Results Section Draft",
            "",
            f"The campaign produced `{result['comparison_count']}` comparison rows. The results should be described as observed profile shifts and comparative regularities across controlled variants.",
            "",
        ],
        "limitations-section-draft.md": [
            "# Limitations Section Draft",
            "",
            "The current campaign is local and exploratory. Results depend on sample selection, edit design, and text length. Additional corpora and repeated studies are required before broader claims are appropriate.",
            "",
        ],
    }
    for filename, lines in materials.items():
        (reports_dir / filename).write_text("\n".join(lines), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["series_name", "study_id", "variant_label", "cosine_similarity", "euclidean_distance", "manhattan_distance", "interpretation"])
        writer.writeheader()
        writer.writerows(rows)


def _write_latex(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [r"\begin{tabular}{llrr}", r"\hline", r"Series & Variant & Cosine signal & Euclidean metric \\", r"\hline"]
    for row in rows:
        series = _latex_escape(str(row["series_name"]))
        variant = _latex_escape(str(row["variant_label"]))
        lines.append(f"{series} & {variant} & {row['cosine_similarity']} & {row['euclidean_distance']} \\\\")
    lines.extend([r"\hline", r"\end{tabular}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Campaign config requires non-empty string field: {key}")
    return value


def _optional_path(base_dir: Path, value: Any) -> Path | None:
    if value is None:
        return None
    return _resolve(base_dir, str(value))


def _resolve(base_dir: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base_dir / path).resolve()


def _slug(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")[:80] or "campaign"


def _latex_escape(value: str) -> str:
    return value.replace("&", r"\&").replace("_", r"\_").replace("%", r"\%")
