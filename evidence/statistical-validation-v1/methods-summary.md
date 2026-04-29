# Statistical Validation v1 Methods Summary

This package aggregates campaign-level comparison rows and benchmark-subset comparison rows into an initial descriptive validation layer.

## Inputs

- empirical campaigns reviewed: `5`
- empirical comparison rows reviewed: `41`
- public benchmark baselines reviewed: `6`
- public benchmark variants reviewed: `36`

## Implemented summaries

- bootstrap percentile intervals for mean metric values;
- per-axis descriptive summaries for campaign rows and benchmark rows;
- within-campaign and between-campaign variance summaries;
- Hedges' g comparisons against the light-edit reference axis;
- seeded cross-baseline random pairing reference from released benchmark variants;
- threshold-sensitivity summaries around the current Euclidean interpretation convention;
- benchmark-versus-campaign bridge summaries for overlapping perturbation axes.

No statistical significance claims are made in this layer.
