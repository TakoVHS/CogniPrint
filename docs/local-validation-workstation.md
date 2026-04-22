# Local Validation Workstation

This document defines the next practical phase for CogniPrint: a local research workstation for theory validation, evidence gathering, and repeatable experiment runs on a personal computer.

## Goal

Create a local operating mode in which CogniPrint can be used as a private research workstation for:

- testing theoretical assumptions on controlled text samples;
- generating reproducible profile outputs;
- comparing perturbation variants of the same text;
- saving experiment inputs and outputs;
- exporting evidence materials for later writing and publication.

## Intended outcome

The workstation should allow the researcher to:

1. load one or more text samples locally;
2. run the same analysis pipeline repeatedly;
3. compare baseline and perturbed variants;
4. save results into structured artifacts;
5. assemble materials for manuscripts, notes, and future dataset releases.

## Target local capabilities

### 1. Local analysis mode

A simple local mode should exist for running CogniPrint against files or pasted text without any external platform dependency.

Minimum inputs:
- single text file;
- folder of text files;
- manual text input.

Minimum outputs:
- fingerprint/profile vector;
- metrics summary;
- comparison output for multiple samples;
- timestamped run record.

### 2. Evidence bundle generation

Each local run should be able to produce a saved evidence bundle containing:

- original input text or an internal reference to it;
- experiment metadata;
- output metrics;
- profile representation;
- optional comparison notes;
- exportable markdown or JSON summary.

### 3. Controlled perturbation workflow

The workstation should support comparing:

- original text;
- lightly edited text;
- strongly edited text;
- multilingual or translated variants when relevant.

This is intended for theory checking and perturbation analysis, not for forensic certainty claims.

### 4. Research material archive

The local workstation should maintain a clean directory structure for preserving research materials:

- `workspace/input/`
- `workspace/runs/`
- `workspace/reports/`
- `workspace/notes/`
- `workspace/exports/`

## Suggested implementation phases

### Phase A — reliable local baseline

- local CLI entrypoint;
- deterministic run output folder;
- experiment manifest per run;
- markdown summary export.

### Phase B — comparison mode

- pairwise comparison of two texts;
- folder-based batch comparison;
- perturbation experiment table.

### Phase C — evidence materials

- machine-readable JSON export;
- human-readable markdown report;
- optional CSV summary for repeated experiments.

### Phase D — researcher convenience layer

- local desktop-friendly launcher or script;
- simple preset commands;
- optional notebook or lightweight local UI.

## Rule of interpretation

The workstation is for research validation, evidence collection, and manuscript preparation.
It must remain aligned with the CogniPrint disclaimer: outputs are analytical signals, not definitive legal or forensic conclusions.
