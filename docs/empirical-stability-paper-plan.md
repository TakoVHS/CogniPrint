# Empirical Stability Paper Plan

This document records the working plan for the second CogniPrint manuscript line: an empirical paper focused on stability under controlled perturbations.

## Working Title

**Empirical Stability of Cognitive Fingerprints Under Controlled Text Perturbations**

## Purpose

The paper should document observed profile shifts and stability tendencies across controlled edits of the same underlying text. It should remain within a cautious research framing and should not overclaim source attribution.

## Canonical Identity

- **Project:** CogniPrint
- **Author:** Adriashkin Roman
- **ORCID:** 0009-0009-6337-1806
- **Affiliation:** CogniPrint Research Initiative
- **Primary category target:** math.ST
- **Secondary category target:** cs.CL
- **Contact:** roman@cogniprint.org

## Central Question

How stable are compact statistical text profiles under light, moderate, and stronger controlled perturbations of the same baseline text?

## Suggested Structure

### 1. Introduction

- Motivation for empirical stability analysis.
- Relation to the CogniPrint mathematical framework.
- Scope limits: observed profile shifts are empirical signals, not final identity claims.

### 2. Experimental Design

- Baseline text selection.
- Controlled perturbation types.
- Series construction rules.
- Metric families and comparison outputs.

### 3. Results

- Metric-level changes across perturbation severity.
- Stability tendencies across repeated series.
- Aggregate campaign observations.
- Representative tables and appendix summaries.

### 4. Interpretation Limits

- Dependence on corpus and perturbation design.
- Absence of universal claims.
- Need for repeated validation.

### 5. Conclusion

- What can currently be said empirically.
- What remains open for future formalisation.

## Target Artifacts From The Workstation

- `campaign-summary.md`
- `campaign-results.json`
- `campaign-results.csv`
- `manuscript-appendix.md`
- `empirical-note.md`
- `methods-note.md`
- `result-summary.md`
- LaTeX summary tables
- `workspace/reports/multi-campaign-summary.md`
- `workspace/reports/paper-2/`

## Drafting Command

```bash
cogniprint campaign paper2 \
  --campaign-root workspace/campaigns \
  --output-dir workspace/reports/paper-2
```

## Safe Wording Policy

Preferred wording:

- observed pattern
- measured shift
- profile difference
- perturbation effect
- stability tendency
- empirical note

Avoid stronger claims that imply source guarantees, legal conclusions, or final classification.

## Practical Next Step

Run three to five campaign-level perturbation studies on controlled text sets, then use the resulting notes and tables to assemble the first empirical draft.
