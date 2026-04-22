# Empirical Stability Paper Plan

This document records the working plan for the second CogniPrint manuscript line: an empirical paper focused on stability under controlled perturbations.

## Working title

**Empirical Stability of Cognitive Fingerprints Under Controlled Text Perturbations**

## Purpose

The paper should document observed profile shifts and stability tendencies across controlled edits of the same underlying text. It should remain within a cautious research framing and should not overclaim source attribution or forensic certainty.

## Canonical identity

- **Project:** CogniPrint
- **Author:** Adriashkin Roman
- **ORCID:** 0009-0009-6337-1806
- **Affiliation:** CogniPrint Research Initiative
- **Primary category target:** math.ST
- **Secondary category target:** cs.CL
- **Contact:** roman@cogniprint.org

## Central question

How stable are compact statistical text profiles under light, moderate, and stronger controlled perturbations of the same baseline text?

## Suggested structure

### 1. Introduction
- Motivation for empirical stability analysis.
- Relation to the CogniPrint mathematical framework.
- Scope limits: observed profile shifts are empirical signals, not definitive identity claims.

### 2. Experimental design
- Baseline text selection.
- Controlled perturbation types.
- Series construction rules.
- Metric families and comparison outputs.

### 3. Results
- Metric-level changes across perturbation severity.
- Stability tendencies across repeated series.
- Aggregate campaign observations.
- Representative tables and appendix summaries.

### 4. Interpretation limits
- Dependence on corpus and perturbation design.
- Absence of universal claims.
- Need for repeated validation.

### 5. Conclusion
- What can currently be said empirically.
- What remains open for future formalisation.

## Target artifacts from the workstation

The following artifacts are intended to feed the paper:

- `campaign-summary.md`
- `campaign-results.json`
- `campaign-results.csv`
- `manuscript-appendix.md`
- `empirical-note.md`
- `methods-note.md`
- `result-summary.md`
- LaTeX summary tables

## Safe wording policy

Preferred wording:
- observed pattern
- measured shift
- profile difference
- perturbation effect
- stability tendency
- empirical note

Avoid:
- proof
- certainty
- definitive attribution
- forensic determination
- confirmed identity

## Practical next step

Run three to five campaign-level perturbation studies on controlled text sets, then use the resulting notes and tables to assemble the first empirical draft.
