# Benchmark Shift Note v1.1

This note compares the descriptive validation layer before and after the larger `wave-004` benchmark expansion.

## Compared states

### Earlier state

- `6` benchmark baselines
- `36` benchmark variants
- `5` benchmark languages
- `3` benchmark source classes

### Current state

- `9` benchmark baselines
- `54` benchmark variants
- `5` benchmark languages
- `3` benchmark source classes

The main difference is not language count. The larger state improves source-domain balance by adding three non-literary baselines in one pass.

## Key descriptive shifts

### Random baseline reference

Earlier `36`-variant state:

- pooled random-baseline mean Euclidean distance: `8.92545`
- draw-mean Euclidean reference interval: `8.549851` to `9.296735`

Current `54`-variant state:

- pooled random-baseline mean Euclidean distance: `9.375026`
- draw-mean Euclidean reference interval: `8.991032` to `9.75524`

Observed shift:

- random-baseline mean Euclidean distance increased by `0.449576`

Interpretation:

The expanded benchmark produces a slightly more separated cross-baseline reference distribution. That is compatible with a broader source mix rather than with tighter within-baseline stability by itself.

### Benchmark-versus-campaign bridge

Earlier `36`-variant state:

- closest Euclidean alignment: `formalized_style`, delta `1.413941`
- widest Euclidean gap: `sentence_split_merge`, delta `11.973804`

Current `54`-variant state:

- closest Euclidean alignment: `formalized_style`, delta `0.871914`
- widest Euclidean gap: `sentence_split_merge`, delta `14.944827`

Observed shift:

- closest bridge alignment improved by `0.542027`
- widest bridge gap increased by `2.971023`

Interpretation:

The bridge does not move in one direction only. One overlapping axis aligns more closely under the broader benchmark mix, while another axis diverges more strongly. This is a mixed stabilization signal, not a simple monotonic improvement.

## Scientific reading

The larger benchmark layer is more credible than the smaller one for descriptive reruns because it is less narrowly dominated by literary material.

At the same time, the current shifts do not justify stronger inferential wording. They show that benchmark composition still matters materially for the descriptive reference layer.

## Decision gate

Current recommendation:

1. do not strengthen inferential language yet;
2. prefer one more provenance-clean benchmark increment with domain-diversity value;
3. rerun the descriptive layer again and check whether the bridge and random-baseline summaries stabilize more moderately.

## Guardrail

This note records descriptive shifts between two benchmark states.

It does not claim proof, completed-study status, or broad domain generalization.
