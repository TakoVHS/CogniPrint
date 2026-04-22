.PHONY: bootstrap init-workspace test smoke demo sample-run sample-compare sample-study sample-profile sample-corpus

PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
CLI := $(VENV)/bin/cogniprint

bootstrap:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .

init-workspace:
	$(CLI) init-workspace

test:
	$(PY) -m unittest discover -s tests -p "test_*.py"

smoke:
	$(CLI) init-workspace
	$(CLI) profile --text "CogniPrint smoke profile for local workstation verification." --output workspace/exports/smoke-profile.json
	$(CLI) run --label smoke-inline --text "CogniPrint smoke run for local workstation verification."
	$(CLI) compare --label smoke-compare --baseline-text "A compact baseline note for profile comparison." --variant-text "A revised baseline note for profile comparison with added context."

sample-run:
	$(CLI) run --label sample-inline --text "CogniPrint studies compact statistical profiles of text for reproducible research notes."

sample-compare:
	$(CLI) compare --label sample-comparison --baseline-text "A concise research note about profile stability." --variant-text "A revised and expanded research note about profile stability under controlled edits."

sample-study:
	$(CLI) study --name sample-perturbation-study --baseline-text "A concise research note about profile stability." --variant-text "A lightly revised research note about profile stability." --variant-text "A strongly revised research note about profile stability with changed structure and added detail."

sample-profile:
	$(CLI) profile --text "CogniPrint studies compact statistical profiles of text." --save --label sample-profile

sample-corpus:
	$(CLI) corpus --input-dir workspace/input --output-dir workspace/corpus --pattern "*.txt"

demo: sample-run sample-compare sample-study sample-profile
