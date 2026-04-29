# Public Benchmark Candidate Selection Notes

This note records the first verified candidate-source layer for `public-benchmark-v1`.

## Current status

The benchmark corpus is not assembled yet. The files in this directory describe candidate public sources only.

## Candidate-source principles

- prefer sources with stable public URLs;
- prefer clear public-domain or otherwise permissive reuse status;
- record acquisition date at the time of intake;
- do not copy raw source text into the benchmark until license and provenance checks are complete;
- keep multilingual coverage explicit rather than assumed.

## Current candidate classes represented

- English literary prose
- English political prose
- Spanish literary prose
- French literary prose
- U.S. government prose

## Next benchmark step

The next step is to choose a small first release subset from this candidate pool, create baseline and controlled variant relations, and then populate:

- `raw/`
- `variants/`
- benchmark-level metadata manifests

Only after that should `evidence/public-benchmark-v1/` move from scaffold status toward a real public benchmark snapshot.
