# Empirical Stability of Compact Text Profiles Under Controlled Perturbations

## Abstract

This manuscript draft summarizes the current CogniPrint empirical evidence package. The current public evidence base contains `5` controlled perturbation campaigns and `41` comparison rows, with campaign-004 contributing `1` controlled series and `11` comparison rows. The present materials document observed patterns, measured shifts, profile differences, perturbation effects, and stability tendencies within a local, provenance-linked corpus. They support a follow-up manuscript but do not justify broader generalization beyond the current evidence package.

## Introduction

CogniPrint is being developed as a reproducible research workstation for compact statistical text profiling and controlled perturbation analysis. The current project state combines a mathematical profile framework, provenance-linked empirical workflows, and a public evidence snapshot intended for colleague review and manuscript consolidation.

## Research Question

How stable are compact text-profile signals under controlled perturbations applied to the same topical baseline within the current CogniPrint corpus?

## Methods

The current empirical workflow is organized as a set of controlled perturbation campaigns run locally in the CogniPrint workstation. Each campaign compares a baseline text against one or more controlled variants and records profile-level comparison outputs. The goal of this workflow is to produce a reproducible empirical evidence package for manuscript preparation, not to claim a complete study.

At the series level, the basic design is baseline versus light edit versus additional variants. In campaign `empirical-campaign-004`, the study manifest records one baseline sample and `11` comparison variants, for `12` total inputs in the run bundle. The variant set includes edited, punctuation-cleanup, lexical-substitution, sentence-split or merge, word-order, compressed, expanded, formalized, informalized, strong-rewrite, and translated or crosslingual conditions. This structure supports side-by-side inspection of measured profile differences under controlled perturbation choices.

Inputs are provenance-linked. The campaign manifest points to the campaign configuration file, the campaign notes directory, the perturbation directory, and the study directory. The study manifest records baseline and variant sample identifiers, SHA-256 hashes, source references, CLI arguments, run identifiers, environment details, and the project metadata block. The dataset scaffold for `empirical-campaign-004-dataset` records dataset directories, source-policy notes, the shared `SOURCES.md` reference, and the relation model connecting variants back to a baseline sample when available.

Campaign outputs are emitted in multiple manuscript-friendly formats. For campaign `empirical-campaign-004`, the current evidence layer includes `campaign-results.csv`, `campaign-results.json`, `campaign-summary.md`, `latex/campaign-summary-table.tex`, `manuscript-appendix.md`, report notes for the current series, and study-level `aggregated-results.csv`, `aggregated-results.json`, `study-manifest.json`, and `study-summary.md`. At the multi-campaign level, the repository also contains cross-campaign summaries and limitations notes under `workspace/reports/`.

The workflow is local and reproducible in the limited engineering sense that the repository retains the source files, run manifests, study manifests, campaign summaries, and validation scripts needed to rerun or audit the current materials on the same workstation setup. In the current repository state, provenance validation has passed. This supports colleague review of how each result was produced, while still requiring further corpus expansion before stronger empirical claims would be appropriate.

The manuscript should also distinguish between the empirical campaign layer and the benchmark-linked validation layer. The campaign layer is the direct source of the `5` campaigns and `41` comparison rows. The benchmark-linked validation layer is a secondary descriptive interpretation layer used to contextualize those campaign results against released public benchmark materials. It is not a separate inferential study, and it should not be read as if it independently establishes population-level conclusions.

## Current Empirical Base

The current evidence package contains:

- `5` controlled perturbation campaigns;
- `41` comparison rows;
- campaign-004 contribution of `1` controlled series and `11` comparison rows;
- public evidence snapshot under `evidence/empirical-v1/`.
- released public benchmark subset under `evidence/public-benchmark-v1/`;
- expanded public benchmark growth layer under `evidence/public-benchmark-v1.1/`;
- benchmark-linked descriptive statistical validation outputs under `evidence/statistical-validation-v1/`.

The public artifact policy excludes raw local-only inputs from the public snapshot.

## Results

The current empirical base contains `5` controlled perturbation campaigns and `41` comparison rows. These materials should be read as a working empirical evidence package supporting a follow-up manuscript. The present results describe observed patterns, measured shifts, profile differences, perturbation effects, and stability tendencies within the current local corpus. They do not establish statistical significance, and they should not be generalized beyond the current campaign set.

Campaign-level summaries show repeated metric movement under controlled edits rather than a single uniform response. Across the current campaign body, campaign means range from cosine signals near `0.973802` to `0.998703`, while mean Euclidean metrics range from `1.601293` to `4.127904`. Within this evidence package, these values are best treated as descriptive indicators of how strongly profile geometry changed under the specific perturbations used in each campaign.

Campaign `empirical-campaign-004` contributes one controlled perturbation series with `11` comparison rows. In that series, light variants such as `edited.txt`, `02_minor_lexical_substitution.txt`, and `09_strong_rewrite_same_claim.txt` showed low perturbation effect signals in the current profile configuration, with Euclidean metrics of `0.321467`, `0.272972`, and `0.225101` respectively. Several structural or compression-related variants showed larger measured shifts, including `01_punctuation_cleanup.txt` at `5.1`, `03_sentence_split_merge.txt` at `5.829847`, `05_compressed_version.txt` at `6.023463`, and `06_expanded_version.txt` at `7.222145`. Other variants, including `04_word_order_shift.txt`, `07_formalized_style.txt`, `08_informalized_style.txt`, and `10_translated_or_crosslingual.txt`, fell into a moderate perturbation range in this profile configuration.

Taken together, these results support a narrow descriptive claim: within the current local evidence package, some controlled edits produce small profile differences while others produce larger measured shifts. The direction and size of the effect depend on the particular variant design, the baseline text, and the metric configuration used in the run bundle. At this stage, the results are most useful as colleague-reviewable empirical materials for a follow-up manuscript rather than as broad claims about text populations.

## Benchmark Growth Layer v1.1

The manuscript should distinguish between the smaller released benchmark subset and the later growth layer used to improve interpretation of the validation frame.

The currently released subset under `evidence/public-benchmark-v1/` records `6` baselines and `36` controlled variants. The broader interpretive layer under `evidence/public-benchmark-v1.1/` records `9` baselines, `54` controlled variants, `5` benchmark languages, and `3` released source classes. This expanded layer should still be treated as small and still requires further growth, but it gives the current manuscript a broader descriptive contrast than the smaller subset alone.

The main manuscript value of this benchmark growth layer is not benchmark finality. Its value is that it improves the descriptive reading of how campaign-level perturbation effects sit against a somewhat broader public reference mix.

## Validation Layer v1.1

The current validation layer should be read as a bridge between campaign-level evidence and a broader benchmark programme. In its current v1.1 state it contributes four practical elements:

- repeatable multi-draw cross-baseline random reference distributions from the released benchmark subset;
- threshold-sensitivity summaries across several metric families rather than a single Euclidean convention;
- richer benchmark-versus-campaign bridge rows for overlapping perturbation axes;
- benchmark-linked validation summaries that can be cited in manuscript drafting without exposing local-only raw inputs.

This v1.1 layer improves interpretability but does not remove the descriptive and corpus-bound character of the current evidence package.

Methodologically, the benchmark-linked validation layer is best understood as a contextual comparison surface. It provides reference distributions, bridge rows, and threshold-oriented descriptive summaries that help the manuscript explain observed campaign behavior more clearly. It does not supply a preregistered inferential design, a stable benchmark-wide null model, or a corpus-generalized decision rule.

In the current package, the random-reference layer reports `64` draws with `54` cross-baseline pairs per draw. The pooled random-reference mean Euclidean distance is `9.375026`, while the draw-mean Euclidean reference interval spans `8.991032` to `9.75524`. The current empirical campaign mean Euclidean distance remains lower at `2.610789`. This remains a useful descriptive contrast for the manuscript because it helps show that the campaign package is not behaving like indiscriminate cross-baseline mismatch in the broader released benchmark-growth layer.

The current threshold layer also helps structure interpretation. Under the current Euclidean grid, the campaign package yields low=`12`, moderate=`13`, larger=`16`, while the benchmark subset yields low=`7`, moderate=`13`, larger=`16`. Under the current cosine grid, the campaign package yields low=`24`, moderate=`5`, larger=`12`, while the benchmark subset yields low=`23`, moderate=`9`, larger=`4`. The manuscript should use these outputs as framing aids rather than as basis for a fixed decision boundary.

The benchmark-versus-campaign bridge shows that overlap is not uniform across perturbation families. Among the shared axes, the closest current Euclidean alignment is `formalized_style` with delta `0.871914`, while the widest current gap is `sentence_split_merge` with delta `14.944827`. This strengthens the discussion section because it lets the manuscript differentiate between perturbation families that appear to travel more smoothly from the broader benchmark-growth layer into the local campaign layer and those that still look strongly corpus-bound.

The bridge should still be read cautiously. The combined benchmark-plus-validation layer now supports clearer reviewer-facing descriptive analysis than the smaller benchmark state did, but benchmark composition still moves the reference behavior materially enough to matter for interpretation.

## Limitations

The current empirical materials remain limited in scope. The repository now contains a working empirical evidence package with `5` campaigns and `41` comparison rows, but this is still a small corpus with a narrow experimental base.

The completed texts are self-authored or otherwise local research materials. That makes the current package useful for controlled internal comparison, but it constrains external generalization. Observed patterns and measured shifts should therefore be interpreted as corpus-bound results from the present evidence layer rather than as claims about a broader population of texts.

The perturbation campaigns are designed around controlled edits to selected baseline samples. This is useful for studying profile differences and perturbation effects, but the resulting measurements still depend on text length, wording choices, edit structure, and the particular feature configuration used in the run bundle. The current repository does not provide a basis for inferential statistical claims, and it does not justify claims of uniform behavior across heterogeneous corpora.

The current package should also be bounded by purpose. It is not an authorship attribution workflow, not a source-verification workflow, and not a forensic or legal instrument. The outputs are analytical signals attached to specific local runs, not conclusions about identity or source.

The current validation layer does not remove these limitations. The random-reference summaries remain cross-baseline references rather than a full null model. The threshold outputs remain descriptive and metric-dependent. The benchmark-versus-campaign bridge remains constrained by a still-small benchmark-growth layer with limited source classes and languages. These layers improve review quality, but they do not justify stronger population-level or decision-level claims.

An additional limitation is benchmark-composition sensitivity. The current benchmark-growth pass improved the descriptive frame, but it also changed the reference behavior enough to matter for interpretation. This means that the manuscript can responsibly discuss benchmark-linked descriptive contrast, yet it still has to state that the current reading depends materially on the released benchmark mix rather than on a benchmark state that can already be treated as settled.

## Discussion

At the current stage, the main value of the evidence package is organizational and descriptive. The repository now supports a coherent path from provenance-linked local inputs to campaign summaries, evidence tables, manuscript-ready sections, and compact colleague-review materials. This makes it possible to ask more disciplined questions about framing and method before expanding the corpus further.

The current evidence package is strong enough to support a follow-up manuscript draft, but not strong enough to justify broad population claims. The current decision gate now supports a bounded provenance-clean benchmark increment, which is a more useful immediate next step than additional infrastructure work. That increment should be treated as evidence-growth work for manuscript support, not as a basis for stronger public claims.

The review loop should still explicitly cover the validation layer. Colleagues should be asked whether the random-reference description is understandable, whether the cross-metric threshold summaries clarify or confuse the evidence package, and whether the benchmark-versus-campaign bridge improves the manuscript's interpretation of perturbation families while the benchmark layer continues to expand under bounded guardrails.

## Future Work

- lock and execute a provenance-clean `wave-005` benchmark increment under the current pre-registration guardrails;
- expand the released public benchmark corpus with broader source classes and language coverage;
- strengthen the current descriptive validation layer into a broader inferential program only where the corpus justifies it;
- expand campaign diversity and corpus heterogeneity;
- incorporate colleague review feedback into the next manuscript iteration.

## Evidence Snapshot Reference

See `evidence/empirical-v1/` for the current public evidence snapshot.

## Suggested Appendix

- public methods summary;
- public results summary;
- public limitations summary;
- evidence table;
- provenance summary;
- benchmark-versus-campaign bridge summary;
- validation v1.1 notes;
- benchmark-validation interpretation note.

## Review Status

This document is a manuscript draft supporting a follow-up manuscript. It is intended for technical review and refinement, not as a publication-ready empirical paper.
