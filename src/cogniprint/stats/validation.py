"""Generate statistical validation summaries from existing CogniPrint artifacts."""

from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from statistics import fmean, median
from typing import Any

from cogniprint.analysis import analyze_text, compare_profiles

from .bootstrap import bootstrap_mean_interval
from .effect_size import hedges_g

THRESHOLD_GRIDS = [
    {"name": "strict", "low_max": 0.5, "moderate_max": 2.0},
    {"name": "current", "low_max": 1.0, "moderate_max": 4.0},
    {"name": "relaxed", "low_max": 1.5, "moderate_max": 5.0},
]


def generate_statistical_validation(*, campaign_root: Path, benchmark_samples_csv: Path, output_dir: Path) -> Path:
    campaign_rows = _load_campaign_rows(campaign_root)
    benchmark_rows = _load_benchmark_rows(benchmark_samples_csv)
    benchmark_comparisons = _build_benchmark_comparisons(benchmark_samples_csv, benchmark_rows)
    output_dir.mkdir(parents=True, exist_ok=True)

    metric_values = {
        "cosine_similarity": [row["cosine_similarity"] for row in campaign_rows],
        "euclidean_distance": [row["euclidean_distance"] for row in campaign_rows],
        "manhattan_distance": [row["manhattan_distance"] for row in campaign_rows],
    }
    overall_summary = {metric: _metric_summary(values) for metric, values in metric_values.items()}
    bootstrap_summary = {metric: bootstrap_mean_interval(values) for metric, values in metric_values.items()}
    variance_summary = _variance_summary(campaign_rows)
    campaign_axis_summary = _axis_summary(campaign_rows)
    benchmark_axis_summary = _axis_summary(benchmark_comparisons)
    effect_size_summary = _effect_size_summary(campaign_rows)
    benchmark_summary = _benchmark_summary(benchmark_rows)
    random_baseline_summary = _random_baseline_summary(benchmark_comparisons)
    threshold_sensitivity = _threshold_sensitivity(campaign_rows, benchmark_comparisons)
    benchmark_campaign_bridge = _benchmark_campaign_bridge(campaign_axis_summary, benchmark_axis_summary)
    counts = _counts_payload(campaign_rows, benchmark_rows, campaign_axis_summary, benchmark_axis_summary)
    manifest = _manifest_payload(counts)

    _write_json(output_dir / "manifest.json", manifest)
    _write_json(output_dir / "counts.json", counts)
    _write_json(output_dir / "overall-metrics.json", overall_summary)
    _write_json(output_dir / "bootstrap-summary.json", bootstrap_summary)
    _write_json(output_dir / "variance-summary.json", variance_summary)
    _write_json(output_dir / "effect-size-summary.json", effect_size_summary)
    _write_json(output_dir / "benchmark-coverage-summary.json", benchmark_summary)
    _write_json(output_dir / "axis-ablation-summary.json", campaign_axis_summary)
    _write_json(output_dir / "benchmark-axis-summary.json", benchmark_axis_summary)
    _write_json(output_dir / "benchmark-campaign-bridge.json", benchmark_campaign_bridge)
    _write_json(output_dir / "random-baseline-summary.json", random_baseline_summary)
    _write_json(output_dir / "threshold-sensitivity.json", threshold_sensitivity)
    _write_axis_csv(output_dir / "axis-ablation-summary.csv", campaign_axis_summary)
    _write_axis_csv(output_dir / "benchmark-axis-summary.csv", benchmark_axis_summary)
    _write_bridge_csv(output_dir / "benchmark-campaign-bridge.csv", benchmark_campaign_bridge)
    _write_random_baseline_csv(output_dir / "random-baseline-summary.csv", random_baseline_summary)
    _write_threshold_csv(output_dir / "threshold-sensitivity.csv", threshold_sensitivity)
    _write_methods_summary(output_dir / "methods-summary.md", counts)
    _write_results_summary(
        output_dir / "results-summary.md",
        counts,
        overall_summary,
        campaign_axis_summary,
        benchmark_axis_summary,
        variance_summary,
        effect_size_summary,
        random_baseline_summary,
        threshold_sensitivity,
        benchmark_campaign_bridge,
    )
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
                    "source": "campaign",
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


def _build_benchmark_comparisons(samples_csv: Path, rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    repo_root = _repo_root_from_samples_csv(samples_csv)
    baseline_rows = {row["sample_id"]: row for row in rows if row["relation_type"] == "baseline"}
    profiles = {
        row["sample_id"]: analyze_text(_resolve_repo_path(repo_root, row["file_path"]).read_text(encoding="utf-8"))
        for row in rows
    }
    comparisons: list[dict[str, Any]] = []
    for row in rows:
        if row["relation_type"] == "baseline":
            continue
        baseline_id = row["baseline_sample_id"]
        baseline_row = baseline_rows[baseline_id]
        comparison = compare_profiles(profiles[baseline_id], profiles[row["sample_id"]])
        comparisons.append(
            {
                "source": "benchmark",
                "campaign_id": "public-benchmark-v1",
                "baseline_sample_id": baseline_id,
                "variant_label": row["sample_id"],
                "axis": row["relation_type"],
                "language": baseline_row["language"],
                "source_class": baseline_row["source_class"],
                "cosine_similarity": float(comparison["cosine_similarity"]),
                "euclidean_distance": float(comparison["euclidean_distance"]),
                "manhattan_distance": float(comparison["manhattan_distance"]),
            }
        )
    return comparisons


def _repo_root_from_samples_csv(path: Path) -> Path:
    resolved = path.resolve()
    for parent in resolved.parents:
        if parent.name == "datasets":
            return parent.parent
    raise ValueError(f"Unable to infer repository root from benchmark samples CSV: {path}")


def _resolve_repo_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (repo_root / path).resolve()


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


def _axis_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_axis: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_axis[row["axis"]].append(row)
    summary = []
    for axis, axis_rows in sorted(by_axis.items()):
        cosine = [row["cosine_similarity"] for row in axis_rows]
        euclidean = [row["euclidean_distance"] for row in axis_rows]
        summary.append(
            {
                "axis": axis,
                "row_count": len(axis_rows),
                "group_count": len({row["campaign_id"] for row in axis_rows}),
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
    return {"reference_axis": "light_edit", "reference_count": len(reference), "comparisons": comparisons}


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


def _random_baseline_summary(benchmark_rows: list[dict[str, Any]], *, seed: int = 1729) -> dict[str, Any]:
    by_baseline: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in benchmark_rows:
        by_baseline[row["baseline_sample_id"]].append(row)
    pool = benchmark_rows[:]
    rng = random.Random(seed)
    sampled_rows = []
    for baseline_id, own_rows in sorted(by_baseline.items()):
        foreign_pool = [row for row in pool if row["baseline_sample_id"] != baseline_id]
        if not foreign_pool:
            continue
        for own_row in own_rows:
            sampled_rows.append(rng.choice(foreign_pool))
    cosine = [row["cosine_similarity"] for row in sampled_rows]
    euclidean = [row["euclidean_distance"] for row in sampled_rows]
    manhattan = [row["manhattan_distance"] for row in sampled_rows]
    return {
        "seed": seed,
        "pair_count": len(sampled_rows),
        "source_note": (
            "Random baseline uses seeded cross-baseline benchmark variant pairings rather than matched same-baseline perturbations."
            if sampled_rows
            else "Random baseline unavailable because the current benchmark fixture does not contain more than one baseline group."
        ),
        "cosine_similarity": _metric_summary(cosine),
        "euclidean_distance": _metric_summary(euclidean),
        "manhattan_distance": _metric_summary(manhattan),
    }


def _threshold_sensitivity(campaign_rows: list[dict[str, Any]], benchmark_rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "metric": "euclidean_distance",
        "grids": [
            {
                "name": grid["name"],
                "low_max": grid["low_max"],
                "moderate_max": grid["moderate_max"],
                "campaign_counts": _threshold_bucket_counts(campaign_rows, grid["low_max"], grid["moderate_max"]),
                "benchmark_counts": _threshold_bucket_counts(benchmark_rows, grid["low_max"], grid["moderate_max"]),
            }
            for grid in THRESHOLD_GRIDS
        ],
    }


def _threshold_bucket_counts(rows: list[dict[str, Any]], low_max: float, moderate_max: float) -> dict[str, int]:
    counts = {"low": 0, "moderate": 0, "larger": 0}
    for row in rows:
        value = float(row["euclidean_distance"])
        if value < low_max:
            counts["low"] += 1
        elif value < moderate_max:
            counts["moderate"] += 1
        else:
            counts["larger"] += 1
    return counts


def _benchmark_campaign_bridge(
    campaign_axis_summary: list[dict[str, Any]],
    benchmark_axis_summary: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    benchmark_map = {row["axis"]: row for row in benchmark_axis_summary}
    bridge = []
    for campaign_row in campaign_axis_summary:
        axis = campaign_row["axis"]
        if axis not in benchmark_map:
            continue
        benchmark_row = benchmark_map[axis]
        bridge.append(
            {
                "axis": axis,
                "campaign_row_count": campaign_row["row_count"],
                "benchmark_row_count": benchmark_row["row_count"],
                "campaign_mean_cosine_similarity": campaign_row["mean_cosine_similarity"],
                "benchmark_mean_cosine_similarity": benchmark_row["mean_cosine_similarity"],
                "cosine_similarity_delta": round(
                    benchmark_row["mean_cosine_similarity"] - campaign_row["mean_cosine_similarity"], 6
                ),
                "campaign_mean_euclidean_distance": campaign_row["mean_euclidean_distance"],
                "benchmark_mean_euclidean_distance": benchmark_row["mean_euclidean_distance"],
                "euclidean_distance_delta": round(
                    benchmark_row["mean_euclidean_distance"] - campaign_row["mean_euclidean_distance"], 6
                ),
            }
        )
    return bridge


def _counts_payload(
    campaign_rows: list[dict[str, Any]],
    benchmark_rows: list[dict[str, str]],
    campaign_axis_summary: list[dict[str, Any]],
    benchmark_axis_summary: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "snapshot_id": "statistical-validation-v1",
        "empirical_campaign_count": len({row["campaign_id"] for row in campaign_rows}),
        "empirical_comparison_row_count": len(campaign_rows),
        "benchmark_baseline_count": sum(1 for row in benchmark_rows if row["relation_type"] == "baseline"),
        "benchmark_variant_count": sum(1 for row in benchmark_rows if row["relation_type"] != "baseline"),
        "benchmark_language_count": len({row["language"] for row in benchmark_rows if row["relation_type"] == "baseline"}),
        "benchmark_source_class_count": len({row["source_class"] for row in benchmark_rows if row["relation_type"] == "baseline"}),
        "campaign_axis_count": len(campaign_axis_summary),
        "benchmark_axis_count": len(benchmark_axis_summary),
    }


def _manifest_payload(counts: dict[str, Any]) -> dict[str, Any]:
    return {
        "snapshot_id": "statistical-validation-v1",
        "status": "initial descriptive statistical validation layer",
        "empirical_campaign_count": counts["empirical_campaign_count"],
        "empirical_comparison_row_count": counts["empirical_comparison_row_count"],
        "benchmark_baseline_count": counts["benchmark_baseline_count"],
        "benchmark_variant_count": counts["benchmark_variant_count"],
        "guardrail": "These outputs provide initial descriptive validation summaries, bootstrap intervals, threshold-sensitivity summaries, and a seeded random baseline reference. They do not claim inferential certainty or publication-level completion.",
    }


def _write_axis_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "axis",
                "row_count",
                "group_count",
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
                    "group_count": row["group_count"],
                    "mean_cosine_similarity": row["mean_cosine_similarity"],
                    "mean_euclidean_distance": row["mean_euclidean_distance"],
                    "cosine_bootstrap_lower": row["cosine_bootstrap"]["lower"],
                    "cosine_bootstrap_upper": row["cosine_bootstrap"]["upper"],
                    "euclidean_bootstrap_lower": row["euclidean_bootstrap"]["lower"],
                    "euclidean_bootstrap_upper": row["euclidean_bootstrap"]["upper"],
                }
            )


def _write_bridge_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "axis",
                "campaign_row_count",
                "benchmark_row_count",
                "campaign_mean_cosine_similarity",
                "benchmark_mean_cosine_similarity",
                "cosine_similarity_delta",
                "campaign_mean_euclidean_distance",
                "benchmark_mean_euclidean_distance",
                "euclidean_distance_delta",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def _write_random_baseline_csv(path: Path, payload: dict[str, Any]) -> None:
    rows = [
        {"metric": "cosine_similarity", **payload["cosine_similarity"]},
        {"metric": "euclidean_distance", **payload["euclidean_distance"]},
        {"metric": "manhattan_distance", **payload["manhattan_distance"]},
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "count", "mean", "median", "min", "max"])
        writer.writeheader()
        writer.writerows(rows)


def _write_threshold_csv(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "grid",
                "low_max",
                "moderate_max",
                "campaign_low",
                "campaign_moderate",
                "campaign_larger",
                "benchmark_low",
                "benchmark_moderate",
                "benchmark_larger",
            ],
        )
        writer.writeheader()
        for row in payload["grids"]:
            writer.writerow(
                {
                    "grid": row["name"],
                    "low_max": row["low_max"],
                    "moderate_max": row["moderate_max"],
                    "campaign_low": row["campaign_counts"]["low"],
                    "campaign_moderate": row["campaign_counts"]["moderate"],
                    "campaign_larger": row["campaign_counts"]["larger"],
                    "benchmark_low": row["benchmark_counts"]["low"],
                    "benchmark_moderate": row["benchmark_counts"]["moderate"],
                    "benchmark_larger": row["benchmark_counts"]["larger"],
                }
            )


def _write_methods_summary(path: Path, counts: dict[str, Any]) -> None:
    lines = [
        "# Statistical Validation v1 Methods Summary",
        "",
        "This package aggregates campaign-level comparison rows and benchmark-subset comparison rows into an initial descriptive validation layer.",
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
        "- per-axis descriptive summaries for campaign rows and benchmark rows;",
        "- within-campaign and between-campaign variance summaries;",
        "- Hedges' g comparisons against the light-edit reference axis;",
        "- seeded cross-baseline random pairing reference from released benchmark variants;",
        "- threshold-sensitivity summaries around the current Euclidean interpretation convention;",
        "- benchmark-versus-campaign bridge summaries for overlapping perturbation axes.",
        "",
        "No statistical significance claims are made in this layer.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_results_summary(
    path: Path,
    counts: dict[str, Any],
    overall_summary: dict[str, Any],
    campaign_axis_summary: list[dict[str, Any]],
    benchmark_axis_summary: list[dict[str, Any]],
    variance_summary: dict[str, Any],
    effect_size_summary: dict[str, Any],
    random_baseline_summary: dict[str, Any],
    threshold_sensitivity: dict[str, Any],
    benchmark_campaign_bridge: list[dict[str, Any]],
) -> None:
    strongest = max(campaign_axis_summary, key=lambda row: row["mean_euclidean_distance"], default=None)
    mildest = min(campaign_axis_summary, key=lambda row: row["mean_euclidean_distance"], default=None)
    current_grid = next((row for row in threshold_sensitivity["grids"] if row["name"] == "current"), None)
    closest_bridge = min(benchmark_campaign_bridge, key=lambda row: abs(row["euclidean_distance_delta"]), default=None)
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
                f"- overlapping benchmark axes reviewed: `{len(benchmark_axis_summary)}`",
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
        ]
    )
    lines.extend(
        [
            "## Random baseline reference",
            "",
            f"- seeded cross-baseline random pairing count: `{random_baseline_summary['pair_count']}`",
            f"- random baseline mean Euclidean distance: `{random_baseline_summary['euclidean_distance']['mean']}`",
            "",
        ]
    )
    if current_grid:
        lines.extend(
            [
                "## Threshold sensitivity note",
                "",
                f"- current grid campaign counts: low=`{current_grid['campaign_counts']['low']}`, moderate=`{current_grid['campaign_counts']['moderate']}`, larger=`{current_grid['campaign_counts']['larger']}`",
                f"- current grid benchmark counts: low=`{current_grid['benchmark_counts']['low']}`, moderate=`{current_grid['benchmark_counts']['moderate']}`, larger=`{current_grid['benchmark_counts']['larger']}`",
                "",
            ]
        )
    if closest_bridge:
        lines.extend(
            [
                "## Benchmark-versus-campaign bridge",
                "",
                f"- closest Euclidean alignment across shared axes: `{closest_bridge['axis']}` with delta `{closest_bridge['euclidean_distance_delta']}`",
                "",
            ]
        )
    lines.extend(
        [
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
        "- the benchmark subset remains excerpt-based and currently covers three languages only;",
        "- the random baseline is a seeded cross-baseline reference rather than a full generative null model;",
        "- threshold sensitivity is reported descriptively and does not determine a universal decision boundary;",
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
        f"- shared campaign axes summarized: `{counts['campaign_axis_count']}`",
        f"- benchmark axes summarized: `{counts['benchmark_axis_count']}`",
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
