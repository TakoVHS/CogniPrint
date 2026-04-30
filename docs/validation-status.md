# Validation Status

This document records the current exploratory bootstrap validation snapshot based on the aggregate study export produced from `workspace/studies`.

## Current snapshot

- metric: `cosine_similarity`
- reference group: `light`
- comparison group: `strong`
- light count: `16`
- strong count: `39`

## Current numbers

- light mean cosine similarity: `0.999753`
- strong mean cosine similarity: `0.981189`
- mean difference (`light - strong`): `0.018564`
- 95% bootstrap CI for the mean difference: `[0.014595, 0.022486]`
- Hedges' g: `1.711265`
- Cliff's delta: `0.942308`
- permutation p-value: `0.0`

## Interpretation

On the current aggregate export, the exploratory bootstrap summary does show a non-zero separation between the derived `light` and `strong` perturbation tiers for cosine similarity.

This is useful descriptive evidence, but it is not yet a justification for stronger general claims. The current grouping is derived from existing `variant_label` and `interpretation` fields in the aggregate CSV, which makes this a practical internal validation pass rather than a final benchmark-grade inference layer.

## Guardrail

Treat this file as a local validation status note for the current reviewer cycle.

It supports the statement that the current package shows an observed perturbation effect on the present dataset.

It does **not** by itself justify:

- forensic or attribution framing;
- broad domain generalization;
- completed-study claims;
- stronger manuscript claims without benchmark expansion and further review.

## Relationship to benchmark expansion

This file should now be read together with:

- `docs/benchmark-shift-note-v1.1.md`
- `docs/benchmark-decision-memo-v1.1.md`

The benchmark-shift note compares the earlier `36`-variant validation state with the current `54`-variant state, and the benchmark-decision memo records the current judgment that the descriptive layer is still moving materially under benchmark composition changes.

## Reproduction

```bash
cd /home/vietcash/projects/CogniPrint
source .venv/bin/activate
make bootstrap-validation
```
