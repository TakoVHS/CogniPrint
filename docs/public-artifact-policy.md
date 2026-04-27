# Public Artifact Policy

This policy defines how CogniPrint separates public review artifacts from local execution materials.

## Purpose

CogniPrint uses a local workspace for empirical runs, campaign generation, dataset scaffolds, reports, and colleague-facing drafts. Not every workspace file is intended to be a public artifact. This policy clarifies what should be published and what should remain local-only unless explicitly reviewed.

## Public artifact layer

The authoritative public empirical snapshot is maintained under:

```text
evidence/empirical-v1/
```

This snapshot may include:

- public counts;
- public methods summaries;
- public results summaries;
- public limitations summaries;
- public evidence tables;
- public provenance summaries;
- machine-readable manifests.

## Local execution layer

The `workspace/` directory is primarily an execution/output area. It may contain:

- raw local input texts;
- temporary run bundles;
- campaign outputs;
- dataset scaffolds;
- share-pack drafts;
- manuscript draft materials;
- local notes.

Some workspace files may be force-added when they are intentionally selected as public review material, but the default assumption is that raw or temporary workspace material is local-only.

## Publication rule

Raw local input texts should not be published in the public evidence snapshot unless they have been explicitly reviewed and cleared for release.

Public summaries should avoid exposing unnecessary raw local text. They should focus on counts, methods, results summaries, limitations, provenance boundaries, and review routes.

## Due diligence rule

For external review, point reviewers first to:

1. `evidence/empirical-v1/`
2. `docs/empirical-evidence-summary-v1.md`
3. `docs/evidence-package-index.md`
4. `docs/public-review-bundle.md`
5. `docs/colleague-review-checklist.md`

## Current status

The current public evidence status is:

- 5 controlled perturbation campaigns;
- 41 comparison rows;
- campaign-004 contribution of 1 controlled series and 11 comparison rows;
- working empirical evidence package supporting a follow-up manuscript.

## Interpretation guardrail

Do not present public artifacts as a publication-ready empirical paper. The current public artifact layer supports review and manuscript consolidation.
