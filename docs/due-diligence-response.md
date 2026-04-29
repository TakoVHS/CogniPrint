# Due Diligence Response

## Short status answer

CogniPrint is not presented as a completed empirical study. It is currently a working empirical evidence package supporting a follow-up manuscript.

## What the reviewer was correct about

The earlier repository state was organized but still closer to a framework and workstation scaffold than to an auditable empirical evidence package. Public-facing evidence materials, concise counts, and due-diligence-oriented summaries were not yet assembled clearly enough for external review.

## What has changed after the feedback

The repository now contains a public empirical evidence snapshot, a released public benchmark subset, colleague-facing review materials, an expanded descriptive statistical validation layer, a manuscript-drafting layer, and clearer public framing about the scope and limits of the current corpus.

## What is now public and auditable

The following materials are now available for review:

- `evidence/empirical-v1/`
- `docs/empirical-evidence-summary-v1.md`
- `docs/evidence-package-index.md`
- `docs/public-review-bundle.md`
- `docs/colleague-review-checklist.md`
- `docs/current-state-summary.md`
- `evidence/public-benchmark-v1/`
- `evidence/statistical-validation-v1/`
- website routes `/evidence/` and `/review/`

## What the public evidence snapshot contains

The public snapshot under `evidence/empirical-v1/` includes:

- `manifest.json`
- `counts.json`
- methods summary
- results summary
- limitations summary
- evidence table
- provenance summary

These files provide a stable public summary of the current empirical base without exposing raw local-only input texts.

The repository also now exposes a released benchmark subset under `evidence/public-benchmark-v1/` and a descriptive validation layer under `evidence/statistical-validation-v1/`. That validation layer now includes repeatable random-reference summaries, threshold review across multiple metric families, and benchmark-versus-campaign bridge artifacts. These layers remain bounded and should be read as validation-oriented evidence rather than as a finished benchmark program.

## What is still not finished

- The current empirical base remains small and corpus-bound.
- The statistical layer remains descriptive rather than inferential.
- The public benchmark corpus is still small and excerpt-based.
- External review and benchmark-oriented validation are still future steps.

## What would be required for the next maturity level

- a public benchmark corpus with clear licensing and provenance;
- statistical validation outputs beyond descriptive campaign summaries;
- broader corpus diversity and stronger comparison baselines;
- additional external review before broader manuscript claims.

## Where to look first

1. `README.md`
2. `evidence/empirical-v1/README.md`
3. `evidence/empirical-v1/manifest.json`
4. `evidence/empirical-v1/counts.json`
5. `docs/empirical-evidence-summary-v1.md`
6. website `/evidence/`
7. website `/review/`

## What should not be claimed

Do not describe the current repository state as:

- a completed empirical study;
- a publication-ready empirical paper;
- a general-purpose source decision system;
- a basis for broad population-level generalization.
