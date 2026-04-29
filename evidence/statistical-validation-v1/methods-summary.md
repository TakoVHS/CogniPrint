# Statistical Validation v1 Methods Summary

This package aggregates campaign-level comparison rows and benchmark-subset coverage rows into an initial descriptive validation layer.

## Inputs

- empirical campaigns reviewed: `5`
- empirical comparison rows reviewed: `41`
- public benchmark baselines reviewed: `6`
- public benchmark variants reviewed: `36`

## Implemented summaries

- bootstrap percentile intervals for mean metric values;
- per-axis descriptive summaries;
- within-campaign and between-campaign variance summaries;
- Hedges' g comparisons against the light-edit reference axis.

No statistical significance claims are made in this layer.
