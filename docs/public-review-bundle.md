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
7. `paper/empirical-stability-v1.md`
8. `evidence/statistical-validation-v1/results-summary.md`
9. `evidence/statistical-validation-v1/benchmark-campaign-bridge-summary.md`
10. `workspace/reports/paper-2/clean-methods-section.md`
11. `workspace/reports/paper-2/clean-results-section.md`
12. `workspace/reports/paper-2/clean-limitations-section.md`
13. `workspace/reports/paper-2/evidence-table.md`
14. `workspace/reports/paper-2/follow-up-manuscript-draft.md`
15. `workspace/share/colleague-pack-004/one-page-summary.md`
16. `workspace/share/colleague-pack-004/email-to-colleagues.md`
17. `workspace/share/colleague-pack-004/review-request-message.md`

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
- which additional corpora or campaign types would make the follow-up manuscript stronger.

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
