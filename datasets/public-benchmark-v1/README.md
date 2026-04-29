# Public Benchmark v1 Scaffold

This directory is the planned repository location for the first public CogniPrint benchmark corpus.

It is currently a scaffold only. It does not yet contain released benchmark samples.

## Intended scope

The first benchmark package is planned to include:

- public-domain texts;
- permissively licensed texts;
- small manually authored benchmark samples;
- multilingual samples when provenance and license status are clear.

## Intended structure

- `raw/` for public baseline texts approved for release;
- `variants/` for controlled public variants linked to baselines;
- `metadata/` for provenance, license, source URL, and acquisition-date records;
- `exports/` for benchmark-level public exports and summaries.

## Guardrail

Do not treat this directory as a released benchmark corpus yet. It is a planning scaffold for the next empirical maturity step.

## Current intake status

The repository now includes a candidate-source intake file under:

- `metadata/candidate-sources.csv`

These rows identify verified public candidate sources for the first benchmark pass. They do not mean benchmark samples have already been released into `raw/` or `variants/`.
