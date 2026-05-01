# Evidence Visibility Layer

The evidence visibility layer is a small TypeScript generator that reads the current public scientific artifacts and materializes a compact visibility summary for review-facing use.

## Purpose

This layer exists to make the current public scientific state easier to inspect without changing the underlying research claims.

It is limited to:

- `evidence/empirical-v1/`
- `evidence/public-benchmark-v1/`
- `evidence/statistical-validation-v1/`

## Outputs

The generator writes:

- `docs/evidence-visibility-checks.json`
- `../TakoVHS.github.io/evidence/dashboard.html`

## Guardrail

The visibility layer is descriptive and review-oriented. It does not turn the current package into:

- a completed empirical study;
- a forensic determination workflow;
- a source-finality or attribution decision system.

## Current visible values

The current generated layer is expected to surface:

- 5 campaigns;
- 41 comparison rows;
- campaign-004 with 11 comparison rows;
- public benchmark subset v1 with 6 baselines and 36 variants;
- validation v1.1 as descriptive.
