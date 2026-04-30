# External Review Dispatch

This document defines the tracked external-review dispatch for the current CogniPrint evidence package.

## Status phrase

Use this exact framing:

> working empirical evidence package supporting a follow-up manuscript

Do not describe the current package as a completed study, final result, or publication-ready empirical paper.

## Review packet

Use the following tracked files as the primary review packet:

1. `docs/empirical-evidence-summary-v1.md`
2. `docs/evidence-package-index.md`
3. `docs/current-state-summary.md`
4. `docs/public-review-bundle.md`
5. `docs/colleague-review-checklist.md`
6. `docs/manuscript-validation-v1.1-notes.md`
7. `paper/empirical-stability-v1.md`
8. `evidence/public-benchmark-v1/coverage-summary.md`
9. `evidence/statistical-validation-v1/results-summary.md`
10. `evidence/statistical-validation-v1/benchmark-campaign-bridge-summary.md`
11. `docs/benchmark-shift-note-v1.1.md`
12. `docs/benchmark-decision-memo-v1.1.md`

Use local workspace materials only as optional follow-up context during direct collaboration.

## Frozen reviewer release

For external review, prefer the frozen reviewer release rather than the moving `main` branch.

- GitHub release: `v0.2.0-reviewer-20260430`
- Release page: `https://github.com/TakoVHS/CogniPrint/releases/tag/v0.2.0-reviewer-20260430`
- Reviewer bundle asset: `https://github.com/TakoVHS/CogniPrint/releases/download/v0.2.0-reviewer-20260430/cogniprint_reviewer_20260430.tar.gz`

Use the tracked files above when discussing specific sections, but use the frozen release as the review anchor.

## What reviewers should evaluate

Ask reviewers to focus on:

- whether the empirical framing is narrow enough;
- whether the methods description is understandable and reproducible enough for manuscript work;
- whether the results section distinguishes descriptive evidence from stronger claims;
- whether the limitations section is explicit enough about corpus bounds;
- whether validation v1.1 improves interpretability;
- whether the benchmark-versus-campaign bridge is useful for discussing perturbation families;
- whether the benchmark shift now looks moderate enough for another benchmark increment;
- which next benchmark or corpus additions would most improve the manuscript.

## Suggested short dispatch message

Suggested wording for review outreach:

> I am sending a compact CogniPrint review packet anchored to the frozen reviewer release v0.2.0-reviewer-20260430. The current repository contains a working empirical evidence package supporting a follow-up manuscript. I am asking for feedback on framing, methods clarity, evidence-table usefulness, validation-layer usefulness, limitations, and whether the current benchmark shift looks moderate enough for another benchmark increment. The package is not being presented as a completed empirical study.

## Decision gate after review

After external review, the next technical decision should be explicit rather than automatic.

Questions to answer:

1. Did reviewers find the validation layer clarifying or distracting?
2. Did reviewers identify missing benchmark coverage that should come before any stronger inference work?
3. Is there enough support to implement a narrower inferential layer, or should effort return to corpus and benchmark expansion first?

## Guardrail

The presence of validation v1.1 does not by itself justify a stronger inferential programme. The next move should depend on review feedback and corpus readiness, not on tooling momentum alone.
