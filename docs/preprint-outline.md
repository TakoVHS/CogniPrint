# Preprint Outline

## Working title

**Cognitive Fingerprints: A Mathematical Framework for Statistical Profiling of Text**

## Positioning

This preprint should present CogniPrint as a mathematical research framework. It should avoid product-style framing and avoid claims that exceed the evidence provided by the experiments.

## Proposed structure

### 1. Introduction
- problem statement in mathematical and empirical terms;
- motivation for compact statistical profiles of text;
- summary of contributions;
- scope and limitations.

### 2. Related mathematical context
- finite-dimensional feature representations;
- empirical profile comparison;
- perturbation stability of summary statistics;
- geometric analysis in feature space.

### 3. Formal setting
- text space and notation;
- feature map definition;
- cognitive fingerprint definition;
- profile similarity and distance definitions.

### 4. Stability analysis
- perturbation model;
- assumptions on feature coordinates;
- propositions and proof sketches from `docs/math.md`;
- discussion of admissible regimes and limitations.

### 5. Empirical protocol
- corpus construction principles;
- preprocessing assumptions;
- feature extraction protocol;
- evaluation of profile variation and profile similarity.

### 6. Results
- descriptive statistics;
- profile-space geometry;
- perturbation experiments;
- sensitivity and robustness analysis.

### 7. Discussion
- interpretation of the findings;
- limits of the current methodology;
- open mathematical questions.

### 8. Conclusion
- summary of the mathematical contribution;
- future directions for formal and empirical refinement.

## Required language rules

Use:
- cognitive fingerprint
- mathematical profile
- statistical signature
- feature space
- profile similarity
- heuristic assessment

Avoid:
- source finality
- automated source judgement
- investigative finality
- legal conclusions
- guaranteed classification
- vendor-specific infrastructure names

## Minimum evidence rule

No claim should be included in the preprint unless it is supported by:
- a formal statement with assumptions;
- a proof or proof sketch;
- or a clearly described empirical result.

## Immediate next writing step

Draft the introduction and formal setting first, then derive the stability section from `docs/math.md`.
