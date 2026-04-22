# CogniPrint Local Validation Workstation

This document describes the actual local research workstation implemented in this repository.

CogniPrint outputs are analytical signals for research use. They are not legal conclusions, source guarantees, or final judgments about a text.

## Install on WSL

Run these commands from the repository root:

```bash
cd /home/vietcash/projects/CogniPrint
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

Or use the bootstrap target:

```bash
cd /home/vietcash/projects/CogniPrint
make bootstrap
source .venv/bin/activate
```

## Workspace Structure

The workstation uses:

- `workspace/input/` for local input material
- `workspace/runs/` for per-run bundles
- `workspace/reports/` for copied markdown summaries
- `workspace/notes/` for researcher notes
- `workspace/exports/` for copied CSV exports
- `workspace/studies/` for named study bundles and aggregated outputs
- `workspace/profiles/` for saved profile JSON
- `workspace/corpus/` for batch profile outputs
- `workspace/experiments/` for YAML experiment outputs
- `workspace/perturbations/` for perturbation lab bundles
- `workspace/datasets/` for dataset scaffolds

Create or repair the structure with:

```bash
cogniprint init-workspace
```

## Run Commands

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

Multiple inputs in one run automatically produce comparison artifacts:

```bash
cogniprint run --label two-sample-check --file workspace/input/original.txt --file workspace/input/edited.txt
```

## Comparison Commands

Inline baseline and variant:

```bash
cogniprint compare \
  --label perturbation-check \
  --baseline-text "A concise research note about profile stability." \
  --variant-text "A revised research note about profile stability under controlled edits."
```

File baseline and file variant:

```bash
cogniprint compare \
  --label original-vs-edited \
  --baseline-file workspace/input/original.txt \
  --variant-file workspace/input/edited.txt \
  --metric cosine
```

One baseline against many folder variants:

```bash
cogniprint compare \
  --label one-to-many \
  --baseline-file workspace/input/original.txt \
  --variant-folder workspace/input/variants/
```

## Study Commands

Use study mode when a single baseline should be compared against controlled variants as one named experiment series.

Inline baseline and variants:

```bash
cogniprint study \
  --name perturbation-inline-study \
  --baseline-text "A concise research note about profile stability." \
  --variant-text "A lightly revised research note about profile stability." \
  --variant-text "A strongly revised research note about profile stability with added context."
```

File baseline and folder variants:

```bash
cogniprint study \
  --name perturbation-folder-study \
  --baseline-file workspace/input/original.txt \
  --variant-file workspace/input/edited.txt \
  --variant-folder workspace/input/variants/
```

## Generated Run Artifacts

Each run writes a bundle under `workspace/runs/<run-id>/`:

- `manifest.json` records timestamp, label, input mode, input references, CLI args, configuration, project identity, Python version, environment summary, and git commit when available.
- `results.json` records metrics, profile representation, fingerprint vector, and comparison signals.
- `summary.md` provides a human-readable research summary.
- `comparisons.json` appears when two or more texts are analyzed.
- `export.csv` provides a compact tabular export for notes and manuscript preparation.

The same markdown summary is copied to `workspace/reports/`, and the CSV export is copied to `workspace/exports/`.

## Study Artifacts

Each study writes a bundle under `workspace/studies/<study-id>/`:

- `study-manifest.json` records the study name, source run, input references, CLI args, and conservative notes.
- `aggregated-results.json` records baseline metrics, variant rows, comparison metrics, and perturbation effect notes.
- `aggregated-results.csv` provides a compact table for manuscript preparation.
- `study-summary.md` is a manuscript-friendly markdown summary.
- `manuscript-note.md` is a conservative note stub for drafting.

Study mode also creates a source comparison run under `workspace/runs/<study-id>-comparison/` so the underlying per-text bundle remains reproducible.

## Profile Command

Use `profile` when you need one machine-readable profile without a full run bundle.

```bash
cogniprint profile --text "CogniPrint studies compact statistical profiles of text."
cogniprint profile --file workspace/input/original.txt --output workspace/exports/original-profile.json
cogniprint profile --file workspace/input/original.txt --save --label original
```

Saved profiles go to `workspace/profiles/`. You can ask the command to compare against saved profiles with a conservative cosine threshold:

```bash
cogniprint profile --file workspace/input/original.txt --similar-threshold 0.98
```

## Corpus Command

Use `corpus` to batch profile a directory of local text files:

```bash
cogniprint corpus --input-dir workspace/input --output-dir workspace/corpus/sample --pattern "*.txt"
```

The command writes one `*.profile.json` artifact per matched input and a `corpus-manifest.json` with source references.

## Report Command

Use `report` to generate manuscript-friendly reports from existing study artifacts:

```bash
cogniprint report --study-dir workspace/studies/<study-id> --format md --output workspace/reports/study-report.md
cogniprint report --study-dir workspace/studies/<study-id> --format pdf --output workspace/reports/study-report.pdf
```

Markdown reports are intended for editing and manuscript notes. PDF reports are plain archival reports generated without extra rendering infrastructure.

## YAML Experiments

Minimal experiment configs are YAML mappings:

```yaml
name: perturbation-series-001
description: Controlled profile comparison for local theory validation.
baseline_file: workspace/input/original.txt
variant_files:
  - workspace/input/edited.txt
variant_folder: workspace/input/variants
output_dir: workspace/experiments
```

Run the experiment with:

```bash
cogniprint experiment run --config workspace/notes/experiment.yml
```

The runner creates a normal study under `workspace/studies/` and copies the study bundle into `workspace/experiments/<experiment-name>/study/`.

## Perturbation Lab

Use `perturb` when you want a baseline, light variant, strong variant, and candidate variants to be treated as one stability-oriented lab bundle:

```bash
cogniprint perturb \
  --name perturbation-lab-001 \
  --baseline-file workspace/input/original.txt \
  --light-file workspace/input/edited.txt \
  --strong-file workspace/input/variants/strongly-edited.txt \
  --variant-folder workspace/input/variants/
```

Outputs are written under `workspace/perturbations/<perturbation-id>/`:

- `perturbation-manifest.json`
- `perturbation-results.json`
- `perturbation-summary.csv`
- `stability-summary.md`
- `study/` copy of the underlying study bundle

Interpret the output as profile shifts, observed changes, perturbation effects, and stability patterns.

## Empirical Notes

Use `notes` to turn completed study artifacts into manuscript-oriented internal notes:

```bash
cogniprint notes --study-dir workspace/studies/<study-id> --output-dir workspace/reports/<study-id>
```

The command writes:

- `empirical-note.md`
- `methods-note.md`
- `result-summary.md`

## Dataset Scaffold

Use `dataset` to create a clean future-release scaffold:

```bash
cogniprint dataset \
  --name perturbation-dataset-001 \
  --description "Local dataset scaffold for controlled profile studies." \
  --baseline-file workspace/input/original.txt \
  --variant-file workspace/input/edited.txt
```

Outputs are written under `workspace/datasets/<dataset-name>/`:

- `dataset-manifest.json`
- `README.md`
- `raw/`
- `variants/`
- `metadata/samples.csv`
- `metadata/variants.csv`
- `exports/`

## Aggregate Study Reports

Use aggregate reporting to compare repeated study outputs:

```bash
cogniprint report \
  --study-dir workspace/studies \
  --aggregate \
  --output workspace/reports/aggregate-study-summary.md \
  --csv-output workspace/exports/aggregate-study-summary.csv
```

This produces a markdown table and optional CSV across all study bundles found in the study root.

## Reproducible Run IDs

By default, run directories include a UTC timestamp and a content/configuration hash. For exact scripted paths, pass `--run-id`:

```bash
cogniprint run --run-id experiment-001 --text "Controlled sample text."
```

The command fails rather than overwriting an existing run directory.

## Make Targets

```bash
make bootstrap
make test
make smoke
make demo
make sample-study
make sample-profile
make sample-corpus
make sample-perturb
make sample-dataset
```

`make smoke` runs deterministic local checks without requiring credentials. `make demo` creates example run, compare, and study bundles.

## GitHub Workflows

`CogniPrint CI` runs on push, pull request, and manual dispatch. It installs the package on Python 3.11, runs tests, compiles `src` and `tests`, and runs the smoke target.

`CogniPrint Research Validation` is manual-only through `workflow_dispatch`. It runs workstation validation commands and uploads generated `workspace/runs`, `workspace/studies`, `workspace/reports`, and `workspace/exports` artifacts for review.

`CogniPrint Nightly Research` supports manual dispatch and a guarded nightly schedule. It creates sample inputs only when missing, runs a study, generates markdown/PDF reports, and uploads workspace artifacts.

There is no Jekyll, GitHub Pages deploy, or website deployment logic in this repository.

## Research Use

Use generated bundles for:

- theory validation notes
- baseline and perturbation comparisons
- manuscript tables and descriptive summaries
- future dataset preparation

Interpret the outputs as profile, metric, comparison, observed change, and perturbation effect signals that require context and repeated validation.

Avoid turning a single run into an over-strong claim. The recommended workflow is:

1. Keep original input files under `workspace/input/`.
2. Put controlled edits under `workspace/input/variants/`.
3. Run `cogniprint study`.
4. Review `study-summary.md` and `aggregated-results.csv`.
5. Copy conservative observations into `workspace/notes/` or manuscript drafts.
