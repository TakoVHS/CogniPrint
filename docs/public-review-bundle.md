# Public Review Bundle

This document defines the compact public review bundle for the current CogniPrint empirical evidence package.

## Status

CogniPrint currently has a working empirical evidence package supporting a follow-up manuscript.

This bundle is intended for colleague review and manuscript planning. It should not be presented as a settled publication-level empirical paper.

## Core review files

Use the following files for a compact review package:

1. `docs/empirical-evidence-summary-v1.md`
2. `docs/evidence-package-index.md`
3. `docs/current-state-summary.md`
4. `docs/colleague-review-checklist.md`
5. `docs/manuscript-validation-v1.1-notes.md`
6. `docs/external-review-dispatch.md`
7. `docs/reviewer-handoff-message.md`
8. `docs/reviewer-feedback-intake.md`
9. `docs/claims-review-questionnaire.md`
10. `docs/claims-matrix.md`
11. `docs/benchmark-protocol.md`
12. `docs/public-benchmark-plan.md`
13. `docs/statistical-validation-plan.md`
14. `docs/manuscript-readiness-checklist.md`
15. `docs/validation-status.md`
16. `docs/benchmark-shift-note-v1.1.md`
17. `docs/benchmark-decision-memo-v1.1.md`
18. `paper/empirical-stability-v1.md`
19. `evidence/empirical-v1/README.md`
20. `evidence/public-benchmark-v1/coverage-summary.md`
21. `evidence/statistical-validation-v1/results-summary.md`
22. `evidence/statistical-validation-v1/benchmark-campaign-bridge-summary.md`
23. `evidence/statistical-validation-v1/limitations-summary.md`
24. `docs/public-vs-local-materials.md`

## Current empirical base

The current package summarizes:

- 5 controlled perturbation campaigns;
- 41 comparison rows;
- campaign-004 contribution of 1 series and 11 comparison rows;
- provenance-linked inputs;
- dataset scaffolds;
- multi-campaign summaries;
- manuscript-oriented drafting outputs.

## Review request

Ask colleagues to evaluate:

- whether the empirical framing is clear;
- whether the Methods section is reproducible enough;
- whether the Results section is appropriately bounded;
- whether the Limitations section is explicit enough;
- whether validation v1.1 improves interpretability or adds unnecessary complexity;
- whether the benchmark-versus-campaign bridge is useful for manuscript discussion of perturbation families;
- whether the benchmark-shift note shows moderate stabilization or continued benchmark sensitivity;
- whether the benchmark-decision memo makes the next-step logic clearer;
- which additional corpora or campaign types would make the follow-up manuscript stronger.

## Canonical decision intake

Use the canonical GitHub decision issue for the narrow benchmark-increment gate:

- `https://github.com/TakoVHS/CogniPrint/issues/16`

Preferred reviewer reply format:

```text
Decision: Increment
Reasoning: <1-2 short paragraphs>
```

or

```text
Decision: Memo
Reasoning: <1-2 short paragraphs>
```

or

```text
Decision: Abstain
Reasoning: <1-2 short paragraphs>
```

## Review-loop decision gate

After the external review pass, decide explicitly between these paths:

1. keep focus on corpus and benchmark expansion if reviewers judge the current validation layer too thin for stronger inference;
2. keep the current descriptive validation layer but tighten manuscript framing if reviewers judge the layer useful but still corpus-bound;
3. implement a narrower inferential layer only if review feedback and corpus readiness both support that move.

## Guardrail

Use the phrase:

> working empirical evidence package supporting a follow-up manuscript

Do not present the current package as a settled empirical paper.

## Reviewer release pattern

Use the reviewer tag pattern:

`v0.2.0-reviewer-YYYYMMDD`

The reviewer bundle should be reproducible with:

```bash
make reviewer-bundle
```

The tracked reviewer release is built from public evidence layers and tracked docs, not from local-only `workspace/` drafting files.
