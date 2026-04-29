.PHONY: bootstrap init-workspace test smoke validate-sources demo sample-run sample-compare sample-study sample-profile sample-corpus sample-perturb sample-dataset billing-test billing-smoke billing-run-api

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

validate-sources:
	$(PY) scripts/validate_sources.py

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

sample-perturb:
	$(CLI) perturb --name sample-perturbation-lab --baseline-file workspace/input/original.txt --light-file workspace/input/edited.txt --variant-folder workspace/input/variants

sample-dataset:
	$(CLI) dataset --name sample-dataset --description "Local CogniPrint dataset scaffold." --baseline-file workspace/input/original.txt --variant-file workspace/input/edited.txt

demo: sample-run sample-compare sample-study sample-profile

billing-test:
	$(PY) -m pytest -q apps/api/tests/test_api.py

billing-smoke:
	test -f .env.example
	test -f .env.billing.example
	test -f apps/api/.env.example
	test -f apps/web/.env.example
	$(PY) -m compileall -q apps/api
	$(PY) -c "from apps.api.app.main import app; print(sorted(route.path for route in app.routes if route.path.startswith('/api/billing')))"

billing-run-api:
	$(VENV)/bin/uvicorn apps.api.app.main:app --reload --port 8000
