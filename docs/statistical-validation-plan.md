# Statistical Validation Plan

## Current limitation

The existing empirical evidence package is descriptive and campaign-level. It provides observed patterns, measured shifts, and profile differences across controlled perturbation campaigns, but it does not yet provide a stronger inferential validation layer.

## Proposed validation layer

The next statistical validation step should include:

- effect-size summaries;
- bootstrap confidence intervals;
- within-campaign variance;
- between-campaign variance;
- random perturbation baseline;
- stability threshold sensitivity;
- ablation by perturbation type.

## Planned implementation targets

These components should be implemented later, not claimed now:

- `src/cogniprint/stats/bootstrap.py`
- `src/cogniprint/stats/effect_size.py`
- `src/cogniprint/stats/confidence_intervals.py`

## Planned output package

Statistical validation outputs should be written under:

- `evidence/statistical-validation-v1/`

## Guardrail

Do not add significance claims, interval claims, or stronger validation language before the statistical layer is actually implemented and verified.
