# Scientific Control Status - 2026-05-01

This note records the current controlled state of the scientific layer after the latest validation and decision-gate checks.

## Current state

CogniPrint remains a working empirical evidence package supporting a follow-up manuscript.

The scientific and reviewer-facing layers are present and validated:

- `docs/due-diligence-response.md`
- `paper/empirical-stability-v1.md`
- `evidence/empirical-v1/`
- `evidence/public-benchmark-v1/`
- `evidence/public-benchmark-v1.1/`
- `evidence/statistical-validation-v1/`
- `docs/statistical-validation-plan.md`
- `docs/public-benchmark-plan.md`
- `docs/manuscript-readiness-checklist.md`
- `docs/public-artifact-policy.md`

## Validation status

The following checks passed on 2026-05-01:

- `make validate-sources`
- `python -m compileall -q src tests scripts`
- `make test`
- `make smoke`
- `python scripts/check_claims_drift.py`
- `make reviewer-release-check`

## Decision-gate status

The canonical intake issue is:

- `https://github.com/TakoVHS/CogniPrint/issues/16`

Current status:

- issue exists
- sync from GitHub comments works
- template comments are ignored correctly
- no real reviewer decision comment has been recorded yet
- `docs/decisions/final-decision.json` therefore remains `pending`

## Guardrail

The next scientific branch must still be chosen by real reviewer input:

- `increment`
- `memo`
- or `ambiguous`

No new benchmark wave should start until that gate resolves.

## Out-of-scope parallel changes

There are local billing-related working-tree changes outside the scientific scope of this note. They were not included in the scientific control pass.
