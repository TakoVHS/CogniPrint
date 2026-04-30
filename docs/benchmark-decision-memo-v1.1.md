# Benchmark Decision Memo v1.1

This memo records the current scientific decision after comparing the `36`-variant and `54`-variant benchmark states.

## Decision question

Does the current benchmark shift look moderate enough to justify another benchmark increment immediately, or is the descriptive layer still moving too much under benchmark composition changes?

## Current answer

The current shift should still be treated as materially benchmark-sensitive.

That does not invalidate the descriptive layer. It means the layer is still responding noticeably to benchmark composition changes, so stronger inferential wording remains premature.

## Main observations

From `docs/benchmark-shift-note-v1.1.md`:

- pooled random-baseline mean Euclidean distance increased from `8.92545` to `9.375026`;
- closest bridge alignment improved from `1.413941` to `0.871914`;
- widest bridge gap increased from `11.973804` to `14.944827`.

These changes do not all point in one direction. They indicate a more credible benchmark mix, but they also show that descriptive reference behavior is still moving under benchmark expansion.

## Scientific interpretation

The current `54`-variant state is better than the `36`-variant state for review and manuscript support because it is less narrowly tied to literary material.

However, the current shift pattern is still too strong to justify:

- stronger inferential language;
- universal threshold framing;
- claims that benchmark composition is no longer materially affecting the validation layer.

## Decision

Choose the narrower path now:

1. keep the current validation layer descriptive;
2. use the benchmark-shift note as the main review anchor;
3. prepare a compact interpretation memo for reviewers and manuscript planning;
4. delay the next benchmark increment decision until review of the current shift note and validation summaries.

## What not to do next

Do not:

- strengthen inferential wording now;
- describe the current benchmark as stable enough for broad generalization;
- launch another benchmark increment just to increase counts without a clear domain-diversity rationale.

## What to do next

The next useful step is a narrower interpretation pass:

- compare benchmark-shift and bridge movement in reviewer-facing prose;
- ask whether reviewers judge the current movement as acceptable descriptive sensitivity or as a sign that benchmark growth should continue before stronger manuscript claims;
- only then choose between another benchmark increment and a more consolidated manuscript pass.

## Guardrail

This memo records a scientific decision under bounded evidence.

It does not claim proof, completed-study status, or benchmark-level finality.
