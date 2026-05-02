#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def expect_equal(errors: list[str], actual: object, expected: object, label: str) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    checks = load_json(root / "docs/evidence-visibility-checks.json")
    empirical = load_json(root / "evidence/empirical-v1/counts.json")
    benchmark = load_json(root / "evidence/public-benchmark-v1/counts.json")
    validation = load_json(root / "evidence/statistical-validation-v1/counts.json")

    errors: list[str] = []

    evidence_snapshot = checks.get("evidence_snapshot", {})
    benchmark_subset = checks.get("benchmark_subset", {})
    validation_v1_1 = checks.get("validation_v1_1", {})

    if not isinstance(evidence_snapshot, dict):
        errors.append("docs/evidence-visibility-checks.json: evidence_snapshot must be an object")
    if not isinstance(benchmark_subset, dict):
        errors.append("docs/evidence-visibility-checks.json: benchmark_subset must be an object")
    if not isinstance(validation_v1_1, dict):
        errors.append("docs/evidence-visibility-checks.json: validation_v1_1 must be an object")

    if errors:
        print("Evidence visibility check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    expect_equal(errors, evidence_snapshot.get("campaigns"), empirical.get("campaign_count"), "campaign count")
    expect_equal(errors, evidence_snapshot.get("comparison_rows"), empirical.get("comparison_row_count"), "comparison row count")
    expect_equal(
        errors,
        evidence_snapshot.get("campaign_004_rows"),
        empirical.get("campaign_004", {}).get("comparison_row_count") if isinstance(empirical.get("campaign_004"), dict) else None,
        "campaign-004 row count",
    )

    expect_equal(errors, benchmark_subset.get("released_baselines"), benchmark.get("released_samples"), "released benchmark baselines")
    expect_equal(errors, benchmark_subset.get("released_variants"), benchmark.get("released_variants"), "released benchmark variants")
    expect_equal(errors, benchmark_subset.get("released_languages"), benchmark.get("released_languages"), "released benchmark languages")
    expect_equal(errors, benchmark_subset.get("released_source_classes"), benchmark.get("released_source_classes"), "released benchmark source classes")

    expect_equal(errors, validation_v1_1.get("snapshot_id"), validation.get("snapshot_id"), "validation snapshot id")
    expect_equal(errors, validation_v1_1.get("benchmark_baselines"), validation.get("benchmark_baseline_count"), "validation benchmark baselines")
    expect_equal(errors, validation_v1_1.get("benchmark_variants"), validation.get("benchmark_variant_count"), "validation benchmark variants")
    expect_equal(errors, validation_v1_1.get("benchmark_languages"), validation.get("benchmark_language_count"), "validation benchmark languages")
    expect_equal(errors, validation_v1_1.get("benchmark_source_classes"), validation.get("benchmark_source_class_count"), "validation benchmark source classes")
    expect_equal(errors, validation_v1_1.get("shared_bridge_axes"), validation.get("shared_bridge_axis_count"), "shared bridge axes")
    expect_equal(errors, validation_v1_1.get("framing"), "descriptive", "validation framing")

    guardrail = str(checks.get("guardrail", ""))
    if "descriptive" not in guardrail or "stronger attribution claim" not in guardrail:
        errors.append("guardrail text is missing expected descriptive/non-upgrade phrasing")

    if errors:
        print("Evidence visibility check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Evidence visibility check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
