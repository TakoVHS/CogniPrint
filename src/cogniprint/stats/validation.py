"""Generate statistical validation summaries from existing CogniPrint artifacts."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import fmean, median
from typing import Any

from .bootstrap import bootstrap_mean_interval
from .effect_size import hedges_g


def generate_statistical_validation(*, campaign_root: Path, benchmark_samples_csv: Path, output_dir: Path) -> Path:
    campaign_rows = _load_campaign_rows(campaign_root)
    benchmark_rows = _load_benchmark_rows(benchmark_samples_csv)
    output_dir.mkdir(parents=True, exist_ok=True)

    metric_values = {
        "cosine_similarity": [row["cosine_similarity"] for row in campaign_rows],
        "euclidean_distance": [row["euclidean_distance"] for row in campaign_rows],
        "manhattan_distance": [row["manhattan_distance"] for row in campaign_rows],
    }
    overall_summary = {
        metric: _metric_summary(values) for metric, values in metric_values.items()
    }
    bootstrap_summary = {
        metric: bootstrap_mean_interval(values) for metric, values in metric_values.items()
    }
    variance_summary = _variance_summary(campaign_rows)
    axis_summary = _axis_summary(campaign_rows)
    effect_size_summary = _effect_size_summary(campaign_rows)
    benchmark_summary = _benchmark_summary(benchmark_rows)
    counts = _counts_payload(campaign_rows, benchmark_rows, axis_summary)
    manifest = _manifest_payload(counts)

    _write_json(output_dir / "manifest.json", manifest)
    _write_json(output_dir / "counts.json", counts)
    _write_json(output_dir / "overall-metrics.json", overall_summary)
    _write_json(output_dir / "bootstrap-summary.json", bootstrap_summary)
    _write_json(output_dir / "variance-summary.json", variance_summary)
    _write_json(output_dir / "effect-size-summary.json", effect_size_summary)
    _write_json(output_dir / "benchmark-coverage-summary.json", benchmark_summary)
    _write_json(output_dir / "axis-ablation-summary.json", axis_summary)
    _write_axis_csv(output_dir / "axis-ablation-summary.csv", axis_summary)
    _write_methods_summary(output_dir / "methods-summary.md", counts)
    _write_results_summary(output_dir / "results-summary.md", counts, overall_summary, axis_summary, variance_summary, effect_size_summary)
    _write_limitations_summary(output_dir / "limitations-summary.md", counts)
    _write_readme(output_dir / "README.md", counts)
    return output_dir


def _load_campaign_rows(campaign_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for campaign_dir in sorted(campaign_root.iterdir()):
        payload_path = campaign_dir / "campaign-results.json"
        if not payload_path.exists():
            continue
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        for row in payload.get("rows", []):
            axis = _axis_from_variant_label(str(row.get("variant_label", "")))
            rows.append(
                {
                    "campaign_id": payload.get("campaign_id", campaign_dir.name),
                    "variant_label": str(row.get("variant_label", "")),
                    "axis": axis,
                    "cosine_similarity": float(row.get("cosine_similarity", 0.0)),
                    "euclidean_distance": float(row.get("euclidean_distance", 0.0)),
                    "manhattan_distance": float(row.get("manhattan_distance", 0.0)),
                }
            )
    return rows


def _load_benchmark_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _metric_summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "median": None, "min": None, "max": None}
    return {
        "count": len(values),
        "mean": round(fmean(values), 6),
        "median": round(float(median(values)), 6),
        "min": round(min(values), 6),
        "max": round(max(values), 6),
    }


def _variance_summary(campaign_rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_campaign: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in campaign_rows:
        by_campaign[row["campaign_id"]].append(row)
    per_campaign = []
    cosine_means = []
    euclidean_means = []
    for campaign_id, rows in sorted(by_campaign.items()):
        cosine_values = [row["cosine_similarity"] for row in rows]
        euclidean_values = [row["euclidean_distance"] for row in rows]
        cosine_mean = fmean(cosine_values)
        euclidean_mean = fmean(euclidean_values)
        cosine_means.append(cosine_mean)
        euclidean_means.append(euclidean_mean)
        per_campaign.append(
            {
                "campaign_id": campaign_id,
                "comparison_count": len(rows),
                "cosine_similarity_variance": round(_sample_variance(cosine_values), 6),
                "euclidean_distance_variance": round(_sample_variance(euclidean_values), 6),
                "mean_cosine_similarity": round(cosine_mean, 6),
                "mean_euclidean_distance": round(euclidean_mean, 6),
            }
        )
    return {
        "per_campaign": per_campaign,
        "between_campaign_variance": {
            "mean_cosine_similarity": round(_sample_variance(cosine_means), 6) if cosine_means else None,
            "mean_euclidean_distance": round(_sample_variance(euclidean_means), 6) if euclidean_means else None,
        },
    }


def _axis_summary(campaign_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_axis: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in campaign_rows:
        by_axis[row["axis"]].append(row)
    summary = []
    for axis, rows in sorted(by_axis.items()):
        cosine = [row["cosine_similarity"] for row in rows]
        euclidean = [row["euclidean_distance"] for row in rows]
        summary.append(
            {
                "axis": axis,
                "row_count": len(rows),
                "campaign_count": len({row["campaign_id"] for row in rows}),
                "mean_cosine_similarity": round(fmean(cosine), 6),
                "mean_euclidean_distance": round(fmean(euclidean), 6),
                "cosine_bootstrap": bootstrap_mean_interval(cosine),
                "euclidean_bootstrap": bootstrap_mean_interval(euclidean),
            }
        )
    return summary


def _effect_size_summary(campaign_rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_axis: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in campaign_rows:
        by_axis[row["axis"]].append(row)
    reference = by_axis.get("light_edit", [])
    reference_cosine = [row["cosine_similarity"] for row in reference]
    reference_euclidean = [row["euclidean_distance"] for row in reference]
    comparisons = []
    for axis, rows in sorted(by_axis.items()):
        if axis == "light_edit":
            continue
        comparisons.append(
            {
                "axis": axis,
                "cosine_similarity_hedges_g": hedges_g(reference_cosine, [row["cosine_similarity"] for row in rows]),
                "euclidean_distance_hedges_g": hedges_g(reference_euclidean, [row["euclidean_distance"] for row in rows]),
            }
        )
    return {
        "reference_axis": "light_edit",
        "reference_count": len(reference),
        "comparisons": comparisons,
    }


def _benchmark_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    baselines = [row for row in rows if row["relation_type"] == "baseline"]
    variants = [row for row in rows if row["relation_type"] != "baseline"]
    languages = Counter(row["language"] for row in baselines)
    source_classes = Counter(row["source_class"] for row in baselines)
    axes = Counter(row["relation_type"] for row in variants)
    return {
        "released_baselines": len(baselines),
        "released_variants": len(variants),
        "languages": dict(sorted(languages.items())),
        "source_classes": dict(sorted(source_classes.items())),
        "perturbation_axes": dict(sorted(axes.items())),
    }


def _counts_payload(
    campaign_rows: list[dict[str, Any]],
    benchmark_rows: list[dict[str, str]],
    axis_summary: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "snapshot_id": "statistical-validation-v1",
        "empirical_campaign_count": len({row["campaign_id"] for row in campaign_rows}),
        "empirical_comparison_row_count": len(campaign_rows),
        "benchmark_baseline_count": sum(1 for row in benchmark_rows if row["relation_type"] == "baseline"),
        "benchmark_variant_count": sum(1 for row in benchmark_rows if row["relation_type"] != "baseline"),
        "benchmark_language_count": len({row["language"] for row in benchmark_rows if row["relation_type"] == "baseline"}),
        "benchmark_source_class_count": len({row["source_class"] for row in benchmark_rows if row["relation_type"] == "baseline"}),
        "axis_count": len(axis_summary),
    }


def _manifest_payload(counts: dict[str, Any]) -> dict[str, Any]:
    return {
        "snapshot_id": "statistical-validation-v1",
        "status": "initial descriptive statistical validation layer",
        "empirical_campaign_count": counts["empirical_campaign_count"],
        "empirical_comparison_row_count": counts["empirical_comparison_row_count"],
        "benchmark_baseline_count": counts["benchmark_baseline_count"],
        "benchmark_variant_count": counts["benchmark_variant_count"],
        "guardrail": "These outputs provide initial descriptive validation summaries and bootstrap intervals. They do not claim inferential certainty or publication-level completion.",
    }


def _write_axis_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "axis",
                "row_count",
                "campaign_count",
                "mean_cosine_similarity",
                "mean_euclidean_distance",
                "cosine_bootstrap_lower",
                "cosine_bootstrap_upper",
                "euclidean_bootstrap_lower",
                "euclidean_bootstrap_upper",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "axis": row["axis"],
                    "row_count": row["row_count"],
                    "campaign_count": row["campaign_count"],
                    "mean_cosine_similarity": row["mean_cosine_similarity"],
                    "mean_euclidean_distance": row["mean_euclidean_distance"],
                    "cosine_bootstrap_lower": row["cosine_bootstrap"]["lower"],
                    "cosine_bootstrap_upper": row["cosine_bootstrap"]["upper"],
                    "euclidean_bootstrap_lower": row["euclidean_bootstrap"]["lower"],
                    "euclidean_bootstrap_upper": row["euclidean_bootstrap"]["upper"],
                }
            )


def _write_methods_summary(path: Path, counts: dict[str, Any]) -> None:
    lines = [
        "# Statistical Validation v1 Methods Summary",
        "",
        "This package aggregates campaign-level comparison rows and benchmark-subset coverage rows into an initial descriptive validation layer.",
        "",
        "## Inputs",
        "",
        f"- empirical campaigns reviewed: `{counts['empirical_campaign_count']}`",
        f"- empirical comparison rows reviewed: `{counts['empirical_comparison_row_count']}`",
        f"- public benchmark baselines reviewed: `{counts['benchmark_baseline_count']}`",
        f"- public benchmark variants reviewed: `{counts['benchmark_variant_count']}`",
        "",
        "## Implemented summaries",
        "",
        "- bootstrap percentile intervals for mean metric values;",
        "- per-axis descriptive summaries;",
        "- within-campaign and between-campaign variance summaries;",
        "- Hedges' g comparisons against the light-edit reference axis.",
        "",
        "No statistical significance claims are made in this layer.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_results_summary(
    path: Path,
    counts: dict[str, Any],
    overall_summary: dict[str, Any],
    axis_summary: list[dict[str, Any]],
    variance_summary: dict[str, Any],
    effect_size_summary: dict[str, Any],
) -> None:
    strongest = max(axis_summary, key=lambda row: row["mean_euclidean_distance"], default=None)
    mildest = min(axis_summary, key=lambda row: row["mean_euclidean_distance"], default=None)
    lines = [
        "# Statistical Validation v1 Results Summary",
        "",
        f"The current validation layer summarizes `{counts['empirical_comparison_row_count']}` empirical comparison rows and `{counts['benchmark_variant_count']}` released benchmark variants.",
        "",
        "## Overall metric summaries",
        "",
        f"- mean cosine similarity: `{overall_summary['cosine_similarity']['mean']}`",
        f"- mean Euclidean distance: `{overall_summary['euclidean_distance']['mean']}`",
        f"- mean Manhattan distance: `{overall_summary['manhattan_distance']['mean']}`",
        "",
    ]
    if strongest and mildest:
        lines.extend(
            [
                "## Axis-level observed pattern",
                "",
                f"- largest mean Euclidean shift in current campaign rows: `{strongest['axis']}` at `{strongest['mean_euclidean_distance']}`",
                f"- smallest mean Euclidean shift in current campaign rows: `{mildest['axis']}` at `{mildest['mean_euclidean_distance']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Variance note",
            "",
            f"- between-campaign variance of mean Euclidean distance: `{variance_summary['between_campaign_variance']['mean_euclidean_distance']}`",
            f"- light-edit reference rows available for effect-size comparison: `{effect_size_summary['reference_count']}`",
            "",
            "These values should be read as descriptive stability tendencies and perturbation-effect summaries rather than definitive inferential results.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_limitations_summary(path: Path, counts: dict[str, Any]) -> None:
    lines = [
        "# Statistical Validation v1 Limitations Summary",
        "",
        "- campaign-level row counts remain modest for stronger inferential interpretation;",
        "- bootstrap intervals summarize observed variation but do not replace a broader benchmark program;",
        "- the benchmark subset remains excerpt-based and currently covers only three languages;",
        "- no random perturbation baseline is implemented in this layer yet;",
        "- no significance testing is claimed in this layer.",
        "",
        f"Current empirical campaign count: `{counts['empirical_campaign_count']}`.",
        f"Current benchmark baseline count: `{counts['benchmark_baseline_count']}`.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_readme(path: Path, counts: dict[str, Any]) -> None:
    lines = [
        "# Statistical Validation v1",
        "",
        "This directory contains the first implemented descriptive statistical validation layer for CogniPrint.",
        "",
        "## Current coverage",
        "",
        f"- empirical campaigns reviewed: `{counts['empirical_campaign_count']}`",
        f"- empirical comparison rows reviewed: `{counts['empirical_comparison_row_count']}`",
        f"- public benchmark baselines reviewed: `{counts['benchmark_baseline_count']}`",
        f"- public benchmark variants reviewed: `{counts['benchmark_variant_count']}`",
        "",
        "## Guardrail",
        "",
        "These outputs are validation-oriented descriptive summaries. They do not claim inferential certainty or a completed statistical program.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _axis_from_variant_label(label: str) -> str:
    mapping = {
        "edited.txt": "light_edit",
        "strongly-edited.txt": "strong_rewrite",
        "01_punctuation_cleanup.txt": "punctuation_cleanup",
        "02_minor_lexical_substitution.txt": "minor_lexical_substitution",
        "03_sentence_split_merge.txt": "sentence_split_merge",
        "04_word_order_shift.txt": "word_order_shift",
        "05_compressed_version.txt": "compressed_version",
        "06_expanded_version.txt": "expanded_version",
        "07_formalized_style.txt": "formalized_style",
        "08_informalized_style.txt": "informalized_style",
        "09_strong_rewrite_same_claim.txt": "strong_rewrite_same_claim",
        "10_translated_or_crosslingual.txt": "translated_or_crosslingual",
    }
    return mapping.get(label, _slug(label))


def _slug(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "_" for char in value).strip("_") or "variant"


def _sample_variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = fmean(values)
    return sum((value - mean) ** 2 for value in values) / (len(values) - 1)


def _write_json(path: Path, payload: dict[str, Any] | list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
