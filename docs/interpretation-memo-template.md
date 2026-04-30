# Interpretation Memo Template v1

Status:

- template only
- use this only if `docs/decisions/final-decision.json` resolves to `memo`

This template exists for the narrow path where reviewers judge the current descriptive layer still too sensitive to benchmark composition for an immediate new corpus increment.

## Title

`Interpretation Memo v1`

## Opening scope statement

State clearly that the memo:

- interprets the current empirical package only
- does not authorize stronger claims
- does not generalize beyond the present benchmark and campaign layers

## Required inputs

Use these project anchors:

- `evidence/empirical-v1/`
- `evidence/public-benchmark-v1.1/`
- `evidence/statistical-validation-v1/`
- `docs/validation-status.md`
- `docs/benchmark-shift-note-v1.1.md`
- `docs/benchmark-decision-memo-v1.1.md`

## Required sections

### 1. Current descriptive snapshot

Report:

- reference and comparison groups
- mean similarity values
- bootstrap interval
- Hedges' g
- Cliff's delta
- permutation p-value

### 2. Interpretation boundary

Explain that:

- the observed separation is descriptive
- the benchmark-composition layer still moves enough to constrain wording
- the memo is a scientific narrowing step, not a retreat from the evidence package

### 3. Why no new benchmark increment yet

Summarize reviewer-backed reasoning:

- benchmark sensitivity still matters materially
- additional corpus growth would be premature without a clearer interpretation layer

### 4. Explicit limitations

Keep these visible:

- small and still-evolving released benchmark
- no forensic or attribution conclusion
- no broad-domain generalization
- no completed-study claim

### 5. Next step

State one concrete next step only:

- either refine interpretation and reviewer discussion further
- or revisit a later benchmark increment once the scientific concerns are clearer

## Guardrail wording

Preferred phrases:

- observed pattern
- measured shift
- descriptive separation
- benchmark-composition sensitivity
- manuscript-facing interpretation note

Avoid:

- detector
- identifies authors
- completed study
- definitive attribution
- forensic determination
