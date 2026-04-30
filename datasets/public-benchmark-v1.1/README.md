# Public Benchmark v1.1 Expansion Scaffold

This directory is the next expansion scaffold after the current released subset in `datasets/public-benchmark-v1/`.

The purpose of `public-benchmark-v1.1` is to prepare the next benchmark increment without mixing planning-only intake material into the already released `v1` subset.

## Intended scope

`public-benchmark-v1.1` should move the benchmark layer toward:

- `20` to `50` public baselines;
- `100` to `300` controlled variants;
- broader multilingual coverage;
- broader source-domain coverage;
- stricter release gating for provenance and reuse checks.

## Intended structure

- `raw/` for approved public baselines selected for the next increment;
- `variants/` for controlled variants released with those baselines;
- `metadata/` for intake, provenance, coverage targets, and release gating;
- `exports/` for benchmark-level descriptive exports.

## Guardrail

This directory is an expansion scaffold only. It does not yet claim a released benchmark increment or benchmark-analysis results.
