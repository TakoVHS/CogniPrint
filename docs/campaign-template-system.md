# Campaign Template System

This document records the recommended template layer for repeatable empirical campaigns in CogniPrint.

## Purpose

Campaign templates exist to reduce manual YAML writing and make repeated perturbation studies easier to run consistently.

## Template location

Templates are stored under:

- `workspace/notes/templates/`

Recommended starter templates:

- `single-baseline-perturbation.yml`
- `multi-series-perturbation-campaign.yml`
- `multilingual-comparison-campaign.yml`

## Template usage

1. Copy the template into `workspace/notes/`.
2. Rename it for the active campaign.
3. Replace sample input paths with your real local inputs.
4. Run `cogniprint campaign run --config <file>`.
5. Run `cogniprint campaign summarize --campaign-dir <campaign-dir>`.

## Safe interpretation rule

Campaign outputs should be described in terms of:

- observed patterns;
- measured shifts;
- profile differences;
- perturbation effects;
- stability tendencies.

Avoid stronger language implying certainty or definitive attribution.
