# CogniPrint

**CogniPrint** is a mathematical research framework for constructing compact statistical profiles of text - called *cognitive fingerprints* - and studying the geometry of profile similarity in feature space.

The project is positioned as a reproducible research methodology. It is not presented as a commercial product or a definitive judgement system.

## Research Scope

CogniPrint investigates:

- empirical regularities in written language;
- compact feature vectors for text profiles;
- similarity and distance between statistical profiles;
- stability of profile structure under controlled perturbations;
- geometric interpretation of representation space.

## Important Disclaimer

CogniPrint provides statistical and heuristic analysis for research purposes only.

Its outputs are:
- metrics derived from text structure;
- a compact fingerprint vector;
- profile comparison signals for regularity patterns.

Its outputs are not:
- source guarantees;
- legal conclusions;
- guaranteed source classification;
- final judgments about a text.

## How to Cite

If you use CogniPrint in research, please cite the project using the metadata in `CITATION.cff`.

Canonical manuscript form:

> Adriashkin, R. (2026). *Cognitive Fingerprints: A Mathematical Framework for Statistical Profiling of Text*. CogniPrint Research Initiative. Preprint v0.1. arXiv submission pending.

Canonical metadata:

- **Author:** Adriashkin Roman
- **ORCID:** 0009-0009-6337-1806
- **Affiliation:** CogniPrint Research Initiative
- **Project site:** https://cogniprint.org
- **Repository:** https://github.com/TakoVHS/CogniPrint

A DOI is assigned to each release via Zenodo.

## Public Research Surface

The current public research surface consists of:

- the project website at `cogniprint.org`;
- the source repository `TakoVHS/CogniPrint`;
- the website repository `TakoVHS/TakoVHS.github.io`;
- manuscript source under `paper/`;
- citation metadata in `CITATION.cff`.

## Project Status

The current repository provides a local research workstation baseline with a command-line interface for repeatable text profile runs, comparison runs, and exportable run bundles.

## Getting Started

```bash
cd /home/vietcash/projects/CogniPrint
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
cogniprint init-workspace
cogniprint run --label inline-sample --text "This is a sample text for analysis."
```

You can also bootstrap the local WSL workstation with:

```bash
make bootstrap
source .venv/bin/activate
make init-workspace
```

## Local Workstation Commands

Inline text:

```bash
cogniprint run --label inline-note --text "CogniPrint studies compact statistical profiles of text."
```

Single file:

```bash
cogniprint run --label file-note --file workspace/input/sample.txt
```

Folder of text files:

```bash
cogniprint run --label folder-batch --folder workspace/input/
```

Comparison:

```bash
cogniprint compare \
  --label original-vs-edited \
  --baseline-file workspace/input/original.txt \
  --variant-file workspace/input/edited.txt \
  --metric cosine
```

One baseline against many variants:

```bash
cogniprint compare \
  --label one-to-many \
  --baseline-file workspace/input/original.txt \
  --variant-folder workspace/input/variants/
```

## Workspace Outputs

The local workspace convention is:

- `workspace/input/` for local input material
- `workspace/runs/` for per-run bundles
- `workspace/reports/` for copied markdown summaries
- `workspace/notes/` for researcher notes
- `workspace/exports/` for copied CSV exports
- `workspace/studies/` for aggregated study bundles

Every run writes:

- `manifest.json`
- `results.json`
- `summary.md`
- `comparisons.json` when multiple texts are present
- `export.csv`

## Study Mode

Use `study` for a named baseline-and-variants workflow:

```bash
cogniprint study \
  --name perturbation-series-001 \
  --baseline-file workspace/input/original.txt \
  --variant-file workspace/input/edited.txt \
  --variant-folder workspace/input/variants/
```

Each study writes:

- `study-manifest.json`
- `aggregated-results.json`
- `aggregated-results.csv`
- `study-summary.md`
- `manuscript-note.md`

## Profile, Corpus, Reports, and Experiments

Single profile JSON:

```bash
cogniprint profile --text "CogniPrint studies compact statistical profiles of text."
cogniprint profile --file workspace/input/original.txt --output workspace/exports/original-profile.json --save --label original
```

Corpus batch profiling:

```bash
cogniprint corpus --input-dir workspace/input --output-dir workspace/corpus/sample --pattern "*.txt"
```

Study reports:

```bash
cogniprint report --study-dir workspace/studies/<study-id> --format md --output workspace/reports/study-report.md
cogniprint report --study-dir workspace/studies/<study-id> --format pdf --output workspace/reports/study-report.pdf
```

YAML experiment:

```yaml
name: perturbation-series-001
baseline_file: workspace/input/original.txt
variant_files:
  - workspace/input/edited.txt
variant_folder: workspace/input/variants
output_dir: workspace/experiments
```

```bash
cogniprint experiment run --config workspace/notes/experiment.yml
```

Perturbation lab:

```bash
cogniprint perturb \
  --name perturbation-lab-001 \
  --baseline-file workspace/input/original.txt \
  --light-file workspace/input/edited.txt \
  --variant-folder workspace/input/variants/
```

Empirical notes and aggregate study report:

```bash
cogniprint notes --study-dir workspace/studies/<study-id> --output-dir workspace/reports/<study-id>
cogniprint report --study-dir workspace/studies --aggregate --output workspace/reports/aggregate-study-summary.md --csv-output workspace/exports/aggregate-study-summary.csv
```

Dataset scaffold:

```bash
cogniprint dataset \
  --name perturbation-dataset-001 \
  --description "Local dataset scaffold for controlled profile studies." \
  --baseline-file workspace/input/original.txt \
  --variant-file workspace/input/edited.txt
```

The scaffold records source references, SHA-256 hashes, and explicit baseline/variant relations in `metadata/`.

Empirical campaign:

```yaml
name: empirical-campaign-001
campaign_id: empirical-campaign-001
description: Multi-series perturbation campaign for empirical stability notes.
series:
  - name: empirical-series-001
    baseline_file: workspace/input/original.txt
    light_file: workspace/input/edited.txt
    variant_folder: workspace/input/variants
```

```bash
cogniprint campaign run --config workspace/notes/campaign.yml
cogniprint campaign summarize --campaign-dir workspace/campaigns/empirical-campaign-001
```

Convenience targets:

```bash
make test
make smoke
make demo
make sample-perturb
make sample-dataset
```

## GitHub Workflows

This repository uses Python-only GitHub Actions workflows. There is no Jekyll, GitHub Pages deploy, or website deployment logic in this repository.

- `CogniPrint CI` runs on push, pull request, and manual dispatch. It installs the package on Python 3.11, runs `make test`, verifies `compileall`, and runs `make smoke`.
- `CogniPrint Research Validation` is manual-only. It runs the local workstation smoke/demo/study flow and uploads generated workspace artifacts for review.
- `CogniPrint Nightly Research` can run on schedule or manually. It creates guarded sample inputs when needed, runs a study, generates markdown/PDF reports, and uploads workspace artifacts.

See `docs/local-validation-workstation.md` for the full local workflow.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
