# Campaign 003 Input Set

This directory is reserved for a genuinely separate empirical input set for `empirical-campaign-003`.

## Intended structure

- `original.txt`
- `edited.txt`
- `variants/`

## Rule

The campaign-003 corpus should not be a duplicate of the earlier micro-series. It should use a separate baseline and controlled variants derived from that baseline.

## Recommended steps

1. Place a new baseline text in `original.txt`.
2. Place a light edit of that same baseline in `edited.txt`.
3. Add 5 to 10 controlled variants under `variants/`.
4. Record source provenance in `workspace/input/SOURCES.md`.
5. Run `make validate-sources` before creating the next campaign config.

## Safe interpretation note

The resulting campaign should be described in terms of observed profile changes, perturbation effects, and stability tendencies. Avoid stronger language implying source finality or universal conclusions.
