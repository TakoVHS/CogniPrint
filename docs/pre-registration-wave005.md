# Pre-registration for wave-005

Status:

- draft template only
- do not lock or rely on this document until `docs/decisions/final-decision.json` resolves to `increment`

This file is a structured draft for a possible `wave-005` benchmark expansion. It exists so the project can move quickly once a reviewer-backed increment decision is recorded, but it is not yet an active pre-registration.

## Decision gate

Current rule:

- `wave-005` may proceed only if the current decision file resolves to `increment`
- before any new corpus download or benchmark loading, run:

```bash
cd /home/vietcash/projects/CogniPrint
source .venv/bin/activate
python scripts/preregister_wave005.py
python scripts/check_prereg_compliance.py
```

## Registration metadata

- registration date: `YYYY-MM-DD`
- git commit before any data loading: `TO_FILL`
- decision file: `docs/decisions/final-decision.json`
- locked hash file: `validation/wave005_prereg_hash.txt`
- lock metadata file: `validation/wave005_prereg_lock.json`

## Hypotheses

Primary descriptive hypothesis:

1. the mean cosine shift between the derived `light` and `strong` perturbation tiers remains non-zero after benchmark expansion under the fixed wave-005 analysis plan

Secondary descriptive hypothesis:

2. benchmark expansion improves reference stability enough to reduce composition-driven movement in the benchmark bridge and random-baseline summaries relative to the earlier v1.1 states

Non-claim:

- this wave does not by itself justify forensic, attribution, or broad-domain generalization claims

## Primary metrics

Only these metrics should be treated as primary unless an explicit appendix note justifies a deviation:

- cosine similarity mean difference between `light` and `strong`
- 95% bootstrap interval for the mean difference
- Hedges' g
- Cliff's delta
- permutation p-value

## Benchmark-growth objective

Target direction:

- expand beyond the current `public-benchmark-v1.1` released state
- prefer provenance-clean public sources
- prioritize source-domain balance over language-count growth for its own sake

Minimum requirements before treating the wave as complete:

- explicit provenance for each new baseline
- no private, paywalled, or unclear-license inputs
- benchmark metadata updated in both `datasets/public-benchmark-v1.1/metadata/` and `evidence/public-benchmark-v1.1/`

## Inclusion and exclusion rules

Include only:

- public-domain or otherwise permissively reusable texts
- sources with stable provenance notes
- texts long enough for the existing CogniPrint profile workflow

Exclude:

- private texts
- unclear-license materials
- paywalled news sources
- sources with unresolved provenance ambiguity

## Analysis lock

The wave-005 path should keep using the existing descriptive validation workflow and should not silently introduce a new inferential framing layer.

Locked workflow:

1. update benchmark metadata and released counts
2. rerun the benchmark-aware descriptive validation
3. compare the new bridge/random-baseline behavior against the prior released state
4. record changes in tracked evidence and reviewer-facing notes

## Integrity confirmation

Before locking this file, confirm:

- no new corpus data have been loaded for wave-005
- no wave-005 results files have been generated
- the decision file already resolves to `increment`

## Investigator sign-off

- principal investigator: `Adriashkin Roman`
- sign-off date: `YYYY-MM-DD`
- signature note: `TO_FILL`
