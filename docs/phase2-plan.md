# Phase 2 — Server-Side Research Extension for CogniPrint

**Status:** Internal implementation proposal.

This document describes a planned local extension for larger-scale experimentation with the **CogniPrint cognitive fingerprint methodology**. The goal is to support reproducible experiments, batch analysis, storage of computed profiles, and programmatic access for research workflows.

## Core rule

All public-facing materials must use only CogniPrint-safe language.

### Allowed public terms
- CogniPrint
- cognitive fingerprint
- mathematical profile
- statistical signature
- feature space
- profile similarity
- heuristic assessment
- research analysis
- empirical regularities
- reproducible computation

### Public language to avoid
- source finality
- automated source judgement
- investigative finality
- legal conclusions
- guaranteed classification
- third-party infrastructure brand names in public copy

## Purpose of Phase 2

Phase 2 is intended to extend the research baseline with:

- a programmatic HTTP interface for experiments;
- asynchronous execution for analysis jobs;
- persistent analytical storage for computed profiles;
- reproducible local orchestration for research workflows.

This is an internal engineering plan, not a public marketing statement.

## Research disclaimer

CogniPrint is a mathematical and computational research methodology.

Its outputs are:
- statistical summaries;
- heuristic assessments;
- profile comparison signals.

Its outputs are not:
- source guarantees;
- legal conclusions;
- guaranteed source classification;
- final judgments about a text.

Any interpretation must remain within the frame of research and experimentation.

## Planned architectural components

Public documentation should describe the system only in generic technical language.

| Internal role | Public description |
|---|---|
| analytical storage | persistent storage for cognitive fingerprint records |
| task queue | asynchronous execution layer |
| HTTP interface | programmatic research API |
| container orchestration | reproducible local runtime |
| configuration layer | centralised environment settings |

## Planned repository additions

The following files are planned for the implementation phase:

- `.env.example` — local research configuration template
- `docker-compose.yml` — local orchestration
- `Dockerfile` — service build instructions
- `src/cogniprint/config.py` — configuration loader
- `src/cogniprint/db/storage.py` — analytical storage client
- `src/cogniprint/tasks/__init__.py` — task layer initialisation
- `src/cogniprint/tasks/analysis_tasks.py` — asynchronous analysis execution
- `src/cogniprint/main.py` — HTTP entry point
- `scripts/init_storage.py` — initial storage setup
- `Makefile` — convenience commands for local research runs

## Public API vocabulary rules

If Phase 2 introduces an HTTP interface, the external vocabulary must remain brand-safe.

### Preferred response fields
- `metrics`
- `fingerprint_vector`
- `heuristic_assessment`
- `score`
- `matches`
- `profile_similarity`

### Avoid
- `source_guarantee`
- `source_judgement`
- `investigative_score`
- `finality_result`

## Example research workflow

```bash
# start local research services
docker-compose up -d

# initialise analytical storage
python scripts/init_storage.py

# send a text for analysis
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Example research text.", "author_id": "exp_01"}'

# query similar cognitive profiles
curl "http://localhost:8000/similar?text=Another%20text&threshold=0.05"
```

This workflow is described for internal implementation planning only.

## Scientific positioning

CogniPrint should be presented as a research programme focused on:

- compact statistical representations of text;
- feature-vector construction;
- empirical regularity analysis;
- similarity in profile space;
- reproducible mathematical experiments.

Preferred framing:

> We study compact statistical representations of text and the geometry of profile similarity.

Avoid product-like or accusatory framing.

## Alignment with citation and visibility

Phase 2 must preserve the project’s scholarly direction:

- `CITATION.cff`
- `.zenodo.json`
- versioned releases
- preprint-ready notes
- mathematically precise terminology

The long-term objective is not sensational product language, but recognised mathematical authorship, citation, DOI visibility, and research legitimacy.

## Public communication rule

When discussing infrastructure outside internal engineering notes:

- describe capabilities generically;
- avoid naming third-party infrastructure products;
- avoid claims that imply legal, investigative, or over-strong classification;
- keep all statements compatible with a research methodology framing.

## Next implementation steps

1. Approve this language standard.
2. Implement Phase 2 files using internal engineering names where needed.
3. Keep public strings and documentation fully vendor-neutral.
4. Validate the extension locally with research-oriented test inputs.
5. Publish only the research-safe framing externally.

## One-sentence positioning

**CogniPrint is a mathematical research framework for cognitive fingerprint analysis, profile comparison, and reproducible study of statistical regularities in text.**
