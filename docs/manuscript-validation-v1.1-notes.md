# Manuscript Validation v1.1 Notes

This document summarizes the current validation-layer material that should be carried into the tracked manuscript route.

## Purpose

The current validation package under `evidence/statistical-validation-v1/` is not a separate empirical study. It is a manuscript-support layer that helps interpret the existing campaign evidence package more clearly.

The latest benchmark-growth pass should also be read together with `docs/benchmark-shift-note-v1.1.md`, which compares the smaller and larger benchmark states and records how the descriptive reference layer moves under a broader source mix.

## Current validation base

- empirical campaigns reviewed: `5`
- empirical comparison rows reviewed: `41`
- released benchmark baselines reviewed: `9`
- released benchmark variants reviewed: `54`
- overlapping bridge axes reviewed: `6`

## What validation v1.1 adds

The current layer contributes four concrete review aids:

1. repeatable multi-draw random-reference summaries;
2. threshold review across cosine, Euclidean, and Manhattan metric families;
3. richer benchmark-versus-campaign bridge summaries for overlapping perturbation axes;
4. manuscript-facing summaries that remain detached from raw local-only inputs.

## Current descriptive anchors

- empirical mean Euclidean distance: `2.610789`
- pooled random-reference mean Euclidean distance: `9.375026`
- random-reference draw-mean Euclidean interval: `8.991032` to `9.75524`
- closest current Euclidean bridge alignment: `formalized_style` with delta `0.871914`
- widest current Euclidean bridge gap: `sentence_split_merge` with delta `14.944827`

These values are useful for discussion of observed pattern and measured shift. They should not be promoted to inferential or decision-level claims.

## Manuscript use

The current manuscript should use these outputs in a bounded way:

- as descriptive contrast between within-campaign perturbation effects and cross-baseline mismatch;
- as a reminder that metric-family choice affects interpretation;
- as support for discussing which perturbation families look more or less corpus-bound;
- as evidence that the repository now contains a reviewable validation layer, not just campaign summaries.

The current manuscript route should also read these summaries together with:

- `docs/benchmark-shift-note-v1.1.md`
- `docs/benchmark-decision-memo-v1.1.md`

## What the manuscript should not claim

The current manuscript should not claim:

- inferential statistical completion;
- universal threshold validity;
- a full null-model implementation;
- benchmark-generalized behavior across heterogeneous corpora.

## Decision gate for stronger inference

The repository should only move from the current descriptive validation layer toward a stronger inferential layer after:

1. external review of the current manuscript framing;
2. review of whether the validation layer clarifies rather than obscures the evidence package;
3. a clearer public benchmark expansion decision;
4. a concrete plan for which inferential outputs are empirically justified by the available corpus.
