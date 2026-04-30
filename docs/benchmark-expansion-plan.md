# Benchmark Expansion Plan

This document defines the next benchmark-growth pass after reviewer release `v0.2.0-reviewer-20260430`.

## Goal

Increase the empirical base from the current small public benchmark subset toward a stronger comparative corpus with 200+ comparison rows and multiple source domains.

## Current constraint

The present public benchmark layer is useful for review and manuscript planning, but it is not yet broad enough to support stronger inferential claims on its own.

## Candidate public or permissively licensed sources

- [ ] PAN authorship and style benchmark materials, subject to license review and attribution clarity.
- [ ] Public-domain literary prose from Project Gutenberg, sampled conservatively by author and text length.
- [ ] Public-domain political or government prose with clean provenance.
- [ ] Small manually authored benchmark samples created specifically for perturbation studies.

## Protocol

1. Select only sources with clear provenance and public reuse conditions.
2. Generate baseline entries plus controlled light and strong perturbation variants.
3. Preserve baseline-versus-variant relations in the benchmark metadata layer.
4. Compare within-source perturbation shifts against cross-source reference behavior.
5. Re-run exploratory and release-level validation summaries after each benchmark expansion pass.

## Sample-size target

- at least 100 comparison pairs for the next headline slice;
- at least 3 campaign families or perturbation families represented in that slice;
- at least 3 source domains before any stronger generalization framing.

## Required implementation tasks

1. [ ] Add source-ingest helpers for approved public datasets.
2. [ ] Extend benchmark metadata registries with clearer domain and source-family fields.
3. [ ] Add campaign runs for new public benchmark families.
4. [ ] Recompute bootstrap and effect-size summaries after each benchmark expansion increment.
5. [ ] Revisit claims wording only after the expanded benchmark layer exists.

## Expected result

- a stronger benchmark-backed reviewer release;
- a broader validation appendix for manuscript work;
- clearer grounds for deciding whether inferential validation should be expanded or still deferred.

## Guardrail

Benchmark growth is for stronger empirical support, not for stronger claims by default. Any change in wording should follow evidence growth, not lead it.
