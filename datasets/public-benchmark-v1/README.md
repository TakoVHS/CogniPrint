# Public Benchmark v1 Scaffold

This directory is the repository location for the first public CogniPrint benchmark corpus.

It now contains a small released subset built from public baseline excerpts and locally derived controlled variants.

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
- `metadata/samples.csv`
- `metadata/release-criteria.md`

The current released subset includes:

- `5` released baseline excerpts;
- `10` released controlled variants;
- `2` released languages (`en`, `es`);
- literary, political, and government prose source classes.

This subset is suitable for public benchmark assembly work and early external review. It does not claim benchmark analysis results or statistical validation yet.
