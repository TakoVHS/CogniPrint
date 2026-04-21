# CogniPrint

**CogniPrint** is a mathematical research framework for constructing compact statistical profiles of text — called *cognitive fingerprints* — and studying the geometry of profile similarity in feature space.

The project is positioned as a reproducible research methodology. It is not presented as a commercial product or a definitive source classifier.

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

## Citation

If you use CogniPrint in your research, please cite it using the metadata in `CITATION.cff`. A DOI is assigned to each release via Zenodo.

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
