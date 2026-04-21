# Paper Directory

This directory contains the manuscript layer for CogniPrint.

## Files

- `main.tex` — the current LaTeX manuscript scaffold.
- `README.md` — overview of the manuscript layer.
- `NOTES.md` — editorial notes and next writing tasks.

## Current status

The manuscript is an early research draft. It already contains:
- title, author, and ORCID block;
- abstract;
- introduction;
- formal setting;
- stability sections;
- limitations;
- empirical protocol;
- conclusion and open problems;
- appendix scaffold.

## Build notes

A minimal local build flow is expected to be:

```bash
cd paper
pdflatex main.tex
pdflatex main.tex
```

A BibTeX or biber stage can be added later if the reference layer is expanded.

## Editorial rule

No sentence in the manuscript should make a stronger claim than is supported by:
- a formal theorem with assumptions;
- a proof or proof sketch;
- a documented empirical result;
- or a clearly labelled open question.
