# Public Benchmark Plan v1.1

This document defines the next benchmark expansion step after the current released subset in `evidence/public-benchmark-v1/`.

## Why a public benchmark is needed

The current empirical package is useful for manuscript planning and colleague review, but it remains small and corpus-bound. A larger public benchmark is needed so that the next validation layer can be audited on openly reviewable materials with clear provenance and licensing.

## Current baseline

The repository already contains a small released benchmark subset:

- `9` public baselines in the current `v1.1` growth layer;
- `54` controlled variants in the current `v1.1` growth layer;
- `5` released languages across the current `v1.1` growth layer;
- `3` released source classes;
- `6` perturbation axes.

This is a legitimate benchmark-growth layer, but it is still too small to support stronger benchmark-level generalization.

## Minimum viable benchmark v1.1

The next benchmark increment should target:

- `20` to `50` public baselines;
- `100` to `300` controlled variants;
- multilingual coverage such as `EN/RU/VI` or `EN/RU/DE/FR`;
- explicit provenance, license, and source-family notes for each released baseline.

## Candidate corpus classes

- public-domain texts;
- permissively licensed texts;
- small manually authored benchmark samples;
- multilingual samples with clear provenance;
- public abstracts only when both attribution and reuse conditions are explicit.

## Excluded sources

Do not include:

- paywalled or unclear-license news content;
- private messages;
- private workspace inputs;
- raw sensitive texts;
- corpora with unclear redistribution status.

## Directory plan

The next increment should be structured under:

- `datasets/public-benchmark-v1.1/`
- `evidence/public-benchmark-v1.1/`

The current `v1` subset should remain available as the already released small benchmark layer.

## Required metadata

Each released baseline in `v1.1` should include:

- stable sample identifier;
- source title;
- source URL;
- license or reuse note;
- acquisition date;
- source domain or source-family field;
- language field;
- relation mapping to controlled variants.

## Validation outputs expected from v1.1

The next benchmark evidence layer should include:

- `manifest.json`
- `counts.json`
- methods summary
- results summary
- limitations summary
- evidence table
- provenance summary

It should also be suitable for re-running the existing descriptive validation layer with broader coverage.

## Relationship to validation

Benchmark expansion is not a cosmetic step. It is the main condition for deciding whether stronger inferential validation is justified.

The sequence should be:

1. expand public benchmark coverage;
2. recompute descriptive validation outputs;
3. evaluate divergence and stability across more source families;
4. only then consider stronger inferential wording.

## Guardrail

This plan does not claim that the benchmark is already complete.

It defines the next benchmark maturity target while preserving the existing released subset as a valid but limited public layer.
