# Public Benchmark v1 Release Criteria

The first public benchmark subset is intentionally small and conservative.

## Release criteria

- the source must have a stable public URL;
- the source class and reuse status must be documented in metadata;
- the released text should be a short excerpt rather than a full imported work;
- each baseline must have at least one controlled variant with a named perturbation axis;
- each released file must map cleanly to a row in `samples.csv`;
- no private or local-only research text may appear in this benchmark subset.

## Current first-release profile

The current release subset is limited to:

- English-language, Spanish-language, and French-language baseline excerpts;
- public-domain literary prose;
- public-domain political prose;
- public-domain government prose;
- six controlled perturbation axes:
  - punctuation cleanup;
  - controlled compression;
  - sentence split and merge;
  - word-order shift;
  - formalized style;
  - informalized style.

## Guardrail

This release criteria note documents what is included in the first subset. It does not claim that benchmark analyses or statistical validation have already been completed.
