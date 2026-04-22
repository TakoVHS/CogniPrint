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
- a heuristic assessment of regularity patterns.

Its outputs are not:
- definitive authorship proof;
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

The current release provides a research baseline with core analysis capabilities and a command-line interface.

## Getting Started

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/quick_test.py "This is a sample text for analysis."
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.
