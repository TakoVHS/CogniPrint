# Benchmark Protocol

## Objective

Measure how CogniPrint profile distances behave under controlled perturbations and compare campaign-linked evidence with a released public benchmark subset.

## Current material

- internal controlled perturbation campaigns 001-005
- released benchmark subset under `datasets/public-benchmark-v1/`
- public benchmark evidence under `evidence/public-benchmark-v1/`
- descriptive validation outputs under `evidence/statistical-validation-v1/`

## Metrics

- cosine similarity
- Euclidean distance
- Manhattan distance
- bootstrap intervals and effect-size summaries already surfaced in the descriptive validation layer

## Procedure

1. Compare baseline texts with controlled variants inside each campaign family.
2. Compare benchmark baselines with controlled public variants.
3. Aggregate observed profile differences by perturbation axis.
4. Use the benchmark-versus-campaign bridge to interpret which axes appear more or less corpus-bound.

## Sample-size growth target

- grow beyond the current 41 campaign comparison rows for stronger inferential slices;
- expand benchmark coverage across additional source classes and languages;
- add enough independent comparisons for leave-one-campaign-out and stronger sensitivity reporting.

## Expected outputs

- reviewer-facing benchmark summaries
- bridge summaries between benchmark axes and campaign axes
- stronger inferential validation only after the current descriptive layer has been externally reviewed

## Guardrail

The current benchmark subset is a released public benchmark layer, but it is not yet the same thing as a full benchmark validation programme.
