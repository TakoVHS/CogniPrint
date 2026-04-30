# Statistical Validation Plan v1.2

This document describes the next validation step after the currently implemented descriptive layer in `evidence/statistical-validation-v1/`.

## Current position

CogniPrint already contains a descriptive statistical validation layer (`v1.1`) with:

- campaign-level summary metrics;
- bootstrap mean intervals for selected metrics;
- effect-size summaries;
- variance summaries;
- random-reference summaries;
- threshold-sensitivity outputs;
- benchmark-versus-campaign bridge artifacts.

These outputs improve interpretability, but they do not yet amount to a broader inferential validation layer.

## Current limitation

The present validation layer is still:

- corpus-bound;
- benchmark-limited;
- descriptive in its main framing;
- dependent on a small released benchmark subset;
- not strong enough for broader generalization claims.

The next step should therefore be framed as `v1.2`, not as a first validation pass.

## v1.2 objective

Move from descriptive validation summaries toward a narrower inferential layer that remains explicitly bounded by corpus size, benchmark coverage, and perturbation-family structure.

## Proposed v1.2 components

### Effect-size summaries

Extend effect-size reporting so that campaign families, benchmark families, and shared perturbation axes can be compared more systematically.

Targets:

- axis-level effect-size summaries;
- campaign-family effect-size summaries;
- benchmark-family effect-size summaries;
- explicit distinction between exploratory and manuscript-citable effect-size outputs.

### Bootstrap confidence intervals

The current bootstrap outputs should be extended from simple mean summaries toward more explicit interval reporting for:

- campaign-level metric summaries;
- axis-level summaries;
- benchmark-versus-campaign deltas;
- stability-band summaries where sample counts permit.

The purpose is interval estimation, not proof language.

### Variance decomposition

Extend current within/between summaries toward a clearer decomposition of:

- within-campaign variance;
- between-campaign variance;
- within-axis variance;
- between-axis variance;
- benchmark-side variance versus campaign-side variance.

This is intended to clarify which parts of the current signal are stable and which remain strongly corpus-bound.

### Random or null reference baseline

The current random-reference layer should be strengthened into a more explicit null-style reference family.

Targets:

- repeatable multi-draw random-reference distributions;
- clearer distinction between cross-baseline mismatch and controlled perturbation shift;
- optional null summaries for shared-axis comparisons where benchmark coverage permits.

This remains a reference baseline, not a claim of decision calibration.

### Axis-wise stability bands

Build axis-wise summaries that show whether a perturbation family tends to remain in a narrow low/moderate/larger band or whether it varies strongly across corpora and campaigns.

These bands should be reported as descriptive stability ranges, not as universal thresholds.

### Metric sensitivity

Extend current threshold outputs toward a clearer metric-sensitivity layer across:

- cosine similarity;
- Euclidean distance;
- Manhattan distance;
- any additional metric family added later under the same conservative rules.

The goal is to document how much the interpretation depends on the metric family.

### Benchmark-versus-campaign divergence

The current bridge artifacts should evolve into a more explicit divergence layer.

Targets:

- shared-axis delta summaries;
- ranking of closest and widest benchmark-versus-campaign gaps;
- stable versus unstable axis notes;
- manuscript-facing wording that keeps these outputs descriptive unless benchmark scale improves.

## Proposed implementation direction

The current repository already contains the main descriptive validation code path. The `v1.2` pass should extend that code rather than introduce a parallel competing pipeline.

Primary implementation surface:

- `src/cogniprint/stats/bootstrap.py`
- `src/cogniprint/stats/effect_size.py`
- `src/cogniprint/stats/confidence_intervals.py`
- `src/cogniprint/stats/validation.py`
- `scripts/generate_statistical_validation.py`

## Planned output package

The next validation release should continue to publish into:

- `evidence/statistical-validation-v1/`

If the schema or maturity level changes materially, introduce a clearly versioned sublayer rather than overwriting the meaning of the current files without explanation.

## Dependency on benchmark growth

`v1.2` depends on benchmark growth. It should not be treated as purely a code task.

Before stronger inferential framing is attempted, the public benchmark layer should move beyond the current small released subset toward:

- more baselines;
- more controlled variants;
- more source domains;
- more explicit multilingual coverage.

## Guardrail

Do not use `v1.2` work to justify:

- proof claims;
- certainty claims;
- forensic framing;
- completed-study wording;
- general-purpose attribution or source-finality claims.

The correct posture remains:

> working empirical evidence package supporting a follow-up manuscript
