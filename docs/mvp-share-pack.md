# CogniPrint MVP Share Pack

This document defines the current minimum viable research package that can be shown to scientific colleagues.

## Current MVP Status

CogniPrint currently provides a working local research workstation with:

- repeatable profile generation;
- text-to-text comparison;
- named study workflows;
- perturbation lab workflows;
- dataset scaffolds;
- campaign-level summaries;
- markdown, CSV, JSON, LaTeX, and PDF-oriented outputs.

The MVP should be presented as a reproducible research workstation for compact statistical text profiles and empirical perturbation studies.

## What To Show Colleagues

A concise colleague-facing package should include:

1. `README.md` from the generated share pack.
2. `project-summary.md`.
3. `campaign-summary.md`.
4. `manuscript-appendix.md`.
5. `latex-summary-table.tex`.
6. one `empirical-note.md` from a series.
7. one dataset scaffold manifest when available.
8. `interpretation-note.md`.

## Suggested Demonstration Sequence

1. Show the baseline input and controlled variants.
2. Run or inspect a campaign config.
3. Show campaign summary outputs.
4. Show manuscript appendix text.
5. Show the LaTeX table as evidence of export readiness.
6. Show the dataset scaffold manifest for future publication preparation.

## Recommended Framing

- reproducible research workstation
- compact statistical text profiles
- controlled perturbation campaigns
- profile shifts and metric shifts
- stability tendencies observed across campaign rows
- campaign-level evidence

## Do Not Send As Claims

- source guarantees
- legal conclusions
- final classification claims
- final judgments about a text

## Command

```bash
cogniprint campaign share-pack \
  --campaign-dir workspace/campaigns/empirical-campaign-001 \
  --dataset-dir workspace/datasets/final-v5-dataset \
  --output-dir workspace/share/colleague-pack-001
```

## Practical Sharing Rule

When sharing with colleagues, prefer a small curated output set over the entire workspace tree.
