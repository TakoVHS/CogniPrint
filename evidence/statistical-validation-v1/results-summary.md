# Statistical Validation v1 Results Summary

The current validation layer summarizes `41` empirical comparison rows and `36` released benchmark variants.

## Overall metric summaries

- mean cosine similarity: `0.990429`
- mean Euclidean distance: `2.610789`
- mean Manhattan distance: `3.444352`

## Axis-level observed pattern

- largest mean Euclidean shift in current campaign rows: `expanded_version` at `4.681358`
- smallest mean Euclidean shift in current campaign rows: `minor_lexical_substitution` at `0.144192`
- overlapping benchmark axes reviewed: `6`

## Variance note

- between-campaign variance of mean Euclidean distance: `1.27235`
- light-edit reference rows available for effect-size comparison: `7`

## Random baseline reference

- seeded cross-baseline random pairing count: `36`
- random baseline mean Euclidean distance: `6.160437`

## Threshold sensitivity note

- current grid campaign counts: low=`12`, moderate=`13`, larger=`16`
- current grid benchmark counts: low=`7`, moderate=`13`, larger=`16`

## Benchmark-versus-campaign bridge

- closest Euclidean alignment across shared axes: `word_order_shift` with delta `1.744741`

These values should be read as descriptive stability tendencies and perturbation-effect summaries rather than definitive inferential results.
