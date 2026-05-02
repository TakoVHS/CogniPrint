#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    dashboard = root.parent / "TakoVHS.github.io" / "evidence" / "dashboard.html"
    if not dashboard.exists():
        print(f"Evidence dashboard check failed:\n- missing dashboard file: {dashboard}")
        return 1

    text = dashboard.read_text(encoding="utf-8")
    errors: list[str] = []

    require(errors, "Evidence Visibility Dashboard" in text, "dashboard title heading is missing")
    require(errors, ">5<" in text and "controlled perturbation campaigns" in text, "dashboard is missing empirical campaign count 5")
    require(errors, ">41<" in text and "comparison rows in the current package" in text, "dashboard is missing empirical comparison row count 41")
    require(errors, ">11<" in text and "campaign-004 comparison rows" in text, "dashboard is missing campaign-004 row count 11")
    require(errors, ">6<" in text and "released benchmark baselines" in text, "dashboard is missing benchmark baseline count 6")
    require(errors, ">36<" in text and "released benchmark variants" in text, "dashboard is missing benchmark variant count 36")
    require(errors, "validation v1.1" in text.casefold(), "dashboard is missing validation v1.1 wording")
    require(errors, "descriptive" in text.casefold(), "dashboard is missing descriptive framing")
    require(errors, "working empirical evidence package supporting a follow-up manuscript" in text, "dashboard is missing core research framing")
    require(errors, "/styles.css" in text, "dashboard is missing stylesheet link")
    require(errors, "https://github.com/TakoVHS/CogniPrint/tree/main/evidence/empirical-v1" in text, "dashboard is missing empirical snapshot link")
    require(errors, "https://github.com/TakoVHS/CogniPrint/tree/main/evidence/public-benchmark-v1" in text, "dashboard is missing public benchmark link")
    require(errors, "https://github.com/TakoVHS/CogniPrint/tree/main/evidence/statistical-validation-v1" in text, "dashboard is missing validation link")

    if errors:
        print("Evidence dashboard check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Evidence dashboard check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
