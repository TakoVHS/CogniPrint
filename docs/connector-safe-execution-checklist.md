# Connector Safe Execution Checklist

This checklist is a guardrail for any external connector or agent run against the CogniPrint repositories.

## Current repository status

- `CogniPrint`: clean, `main...origin/main`
- `TakoVHS.github.io`: clean, `main...origin/main`
- public reviewer release already exists:
  - `v0.2.0-reviewer-20260430`
- reviewer bundle asset already exists:
  - `cogniprint_reviewer_20260430.tar.gz`

## Already completed

These items should be treated as already done unless a new pass has a narrow correction to make.

### Scientific and reviewer surface

- `docs/due-diligence-response.md`
- `paper/empirical-stability-v1.md`
- `evidence/empirical-v1/`
- `evidence/public-benchmark-v1/`
- `evidence/statistical-validation-v1/`
- `docs/current-state-summary.md`
- `docs/public-review-bundle.md`
- `docs/colleague-review-checklist.md`
- `docs/external-review-dispatch.md`
- `docs/reviewer-handoff-message.md`
- `docs/reviewer-feedback-intake.md`
- `docs/claims-review-questionnaire.md`
- reviewer release tag and release asset

### Validation and benchmark support

- exploratory validation helper:
  - `scripts/bootstrap_validation.py`
- feedback synthesis helper:
  - `scripts/synthesize_feedback.py`
- benchmark growth direction:
  - `docs/benchmark-expansion-plan.md`
- current exploratory validation snapshot:
  - `docs/validation-status.md`
  - `docs/validation-status.json`

### Website

- `/evidence/` exists
- `/review/` exists
- Evidence and Review appear in navigation on the main public pages
- sitemap includes `/evidence/` and `/review/`
- robots.txt points to sitemap

### Optional billing layer

The optional commercial layer already exists separately under:

- `apps/api/`
- `apps/web/`

It must remain optional and secondary to the research and evidence layers.

## Partially complete or outdated

These areas exist, but may need refinement rather than replacement.

### `docs/statistical-validation-plan.md`

This file exists, but it still describes the next step in older terms. The repository now already contains an implemented descriptive validation layer under `evidence/statistical-validation-v1/`, so the plan should be revised forward toward inferential `v1.2`, not rewritten as if validation has not started.

### `docs/public-benchmark-plan.md`

This file exists, but it still points to the older `v1` benchmark-growth framing. It should be updated carefully toward a `v1.1` expansion target without discarding the current released subset.

### `docs/public-artifact-policy.md`

This file exists and is mostly correct, but it should be tightened to state more explicitly that:

- `workspace/` is local/private by default;
- `evidence/` directories are the authoritative public layer;
- raw local texts are not published;
- new evidence layers require updated `manifest.json` and `counts.json`.

## Not yet completed

These are the real remaining tasks from the large connector prompt.

1. Create `docs/manuscript-readiness-checklist.md`
2. Update `docs/statistical-validation-plan.md` to an explicit `v1.2` forward plan
3. Update `docs/public-benchmark-plan.md` to the requested `v1.1` expansion framing
4. Strengthen `evidence/public-benchmark-v1/results-summary.md` so it does more than just restate counts
5. Create or update GitHub issues so they match the current plan exactly:
   - add an issue specifically for reviewing the public benchmark subset
   - keep benchmark expansion, manuscript, validation, and optional Stripe review separate
6. Optionally create a manuscript-readiness and external-review presentation layer after the scientific documents are stable

## Do not overwrite

An external connector should not blindly recreate or replace the following:

- `docs/due-diligence-response.md`
- `paper/empirical-stability-v1.md`
- `docs/current-state-summary.md`
- `docs/public-review-bundle.md`
- `docs/external-review-dispatch.md`
- `docs/reviewer-handoff-message.md`
- `docs/reviewer-feedback-intake.md`
- `docs/claims-review-questionnaire.md`
- `docs/validation-status.md`
- `docs/validation-status.json`
- `evidence/public-benchmark-v1/*`
- `evidence/statistical-validation-v1/*`
- website `/evidence/` and `/review/` pages unless only narrow wording or link fixes are needed

## Safe execution order

If the connector continues, the safe order is:

1. scientific docs first;
2. benchmark and validation plan refinement second;
3. manuscript-readiness checklist third;
4. GitHub issue alignment fourth;
5. website wording touch-ups fifth;
6. optional Stripe work only after the scientific and reviewer-facing tasks are stable.

## Guardrail

Do not let the optional Stripe or hosted-access layer displace the manuscript draft, benchmark subset, or validation layer as the primary project identity.

The correct scientific phrase remains:

> working empirical evidence package supporting a follow-up manuscript
