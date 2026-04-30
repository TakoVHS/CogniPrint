# Public Benchmark v1.1 Methods Summary

This file summarizes the released `v1.1` benchmark waves.

## Release method

The `v1.1` release extends the existing public benchmark layer with three small approved waves rather than a full benchmark jump.

Current release method:

- select public-domain source texts with stable source URLs;
- extract short baseline excerpts suitable for public release;
- create six controlled variants per baseline across the current perturbation axes;
- record every baseline and variant in `datasets/public-benchmark-v1.1/metadata/sample-plan-template.csv`;
- publish matching counts and summaries under `evidence/public-benchmark-v1.1/`.

## Current released waves

The released `v1.1` waves add:

- one German-language literary baseline;
- one Russian-language literary baseline;
- one English-language government baseline;
- one French-language literary baseline;
- one English-language political baseline;
- one Spanish-language literary baseline;
- six controlled variants for each baseline.

The released waves are intentionally small. Their purpose is to extend language and source-class coverage without destabilizing the meaning of the already released `public-benchmark-v1` subset.

The third wave was selected to improve source-domain balance rather than to add languages mechanically. It introduces:

- a second English non-literary baseline in political prose;
- a Spanish baseline with clean public provenance.
