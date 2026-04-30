# PROGRESS

## 2026-04-27 — Empirical Evidence Snapshot v1

Completed:
- consolidated the current empirical base into a public evidence snapshot under `evidence/empirical-v1/`;
- recorded the current evidence counts:
  - 5 controlled perturbation campaigns;
  - 41 comparison rows;
  - campaign-004 contribution of 1 controlled series and 11 comparison rows;
- added machine-readable public evidence metadata:
  - `evidence/empirical-v1/manifest.json`;
  - `evidence/empirical-v1/counts.json`;
- added public summary artifacts:
  - `evidence/empirical-v1/methods-summary.md`;
  - `evidence/empirical-v1/results-summary.md`;
  - `evidence/empirical-v1/limitations-summary.md`;
  - `evidence/empirical-v1/evidence-table.md`;
  - `evidence/empirical-v1/provenance-summary.md`;
- added public artifact policy in `docs/public-artifact-policy.md`;
- updated `README.md` to surface the current empirical evidence package;
- maintained the project framing as a working empirical evidence package supporting a follow-up manuscript.

Current status:
- CogniPrint is no longer only a scaffold or framework outline;
- it now has a public empirical evidence snapshot for due diligence and colleague review;
- it is still not presented as a publication-ready empirical paper.

Next:
- expose the evidence snapshot from the public website;
- continue manuscript consolidation from the clean Methods, Results, Limitations, and evidence table;
- obtain external review on the evidence package and manuscript draft.

## 2026-04-29 — Public Benchmark Scaffold v1

Completed:
- added `docs/due-diligence-response.md` for technical reviewers;
- added `docs/public-benchmark-plan.md` to define the next empirical maturity step;
- added `docs/statistical-validation-plan.md` to separate current descriptive evidence from later validation work;
- added `paper/empirical-stability-v1.md` as a manuscript draft scaffold for the follow-up paper;
- added `datasets/public-benchmark-v1/` as a public benchmark scaffold with metadata templates;
- added `evidence/public-benchmark-v1/` as a zero-count public benchmark evidence scaffold;
- added a first verified candidate-source intake layer in `datasets/public-benchmark-v1/metadata/candidate-sources.csv`.
- released a first small public benchmark subset:
  - `6` baseline excerpts;
  - `36` controlled variants;
  - `3` released languages;
  - literary, political, and government prose source classes;
- added `datasets/public-benchmark-v1/metadata/samples.csv`;
- added `datasets/public-benchmark-v1/metadata/release-criteria.md`;
- updated `evidence/public-benchmark-v1/manifest.json` and `counts.json` to reflect the released subset.
- added `evidence/public-benchmark-v1/evidence-table.md` for descriptive benchmark-subset coverage;
- added `evidence/statistical-validation-v1/` as a no-results validation scaffold for the next implementation layer.
- expanded benchmark perturbation coverage to sentence segmentation, word-order shifts, and style-shift variants.

Current status:
- the benchmark layer is now scaffolded in the repository;
- an expanded small public benchmark subset is now released;
- the active public empirical package remains `evidence/empirical-v1/`.

Next:
- prepare a first small benchmark corpus with explicit licensing and provenance;
- expand the released public subset beyond the initial three baselines and six variants;
- request external review on the current evidence package and manuscript layer;
- implement the planned statistical validation layer after benchmark assembly.

## 2026-04-29 — Statistical Validation v1.1

Completed:
- expanded `evidence/statistical-validation-v1/` from a first-pass descriptive layer into a stronger v1.1 validation package;
- added repeatable multi-draw cross-baseline random reference summaries;
- added threshold-sensitivity outputs across cosine, Euclidean, and Manhattan metric families;
- added richer benchmark-versus-campaign bridge outputs and a dedicated bridge summary;
- updated `paper/empirical-stability-v1.md` to include a separate validation-layer section;
- updated public evidence and review routes to surface the benchmark and validation layer more clearly.

Current status:
- the repository now contains a released benchmark subset and an expanded descriptive validation layer;
- the validation package remains descriptive and corpus-bound;
- it should still be read as support for a follow-up manuscript rather than as a completed inferential programme.

Next:
- use the current validation layer in external review;
- decide which validation components justify a stronger inferential implementation;
- expand corpus diversity only where provenance and release criteria remain clear.

## 2026-04-30 — Benchmark Expansion Execution v1.1 Scaffold

Completed:
- added `datasets/public-benchmark-v1.1/` as the next benchmark-expansion scaffold;
- added `datasets/public-benchmark-v1.1/metadata/intake-candidates.csv` as a target-oriented intake registry for the next release wave;
- added `datasets/public-benchmark-v1.1/metadata/coverage-targets.md`;
- added `datasets/public-benchmark-v1.1/metadata/release-gate.md`;
- added `datasets/public-benchmark-v1.1/metadata/sample-plan-template.csv`;
- added `evidence/public-benchmark-v1.1/` as a zero-count evidence scaffold for the next released benchmark increment;
- extended evidence integrity checks so the new `v1.1` scaffold is validated together with the existing public layers.

Current status:
- `public-benchmark-v1` remains the current released subset;
- `public-benchmark-v1.1` now exists as the next benchmark-expansion surface;
- the next substantive benchmark step is prepared as intake and release-gate work rather than as untracked ad hoc additions.

Next:
- select and verify the next wave of public baselines;
- populate `datasets/public-benchmark-v1.1/metadata/sample-plan-template.csv` with approved release candidates;
- release the next benchmark increment only after provenance, licensing, and counts are internally consistent.

## 2026-04-30 — Public Benchmark v1.1 Second Released Wave

Completed:
- selected a second approved `v1.1` wave from the intake registry;
- added one English public-domain government baseline;
- added one French public-domain literary baseline;
- added six controlled variants for each new baseline across the current perturbation axes;
- updated `evidence/public-benchmark-v1.1/` from a first-wave release to a two-wave release.

Current status:
- `public-benchmark-v1.1` now releases `4` baselines and `24` controlled variants;
- released languages in `v1.1` now include `de`, `ru`, `en`, and `fr`;
- released source classes in `v1.1` now include literary and government prose;
- the benchmark remains small, but it is less narrowly literary than the first released wave.

Next:
- add another small approved wave only if provenance remains as clean as the current release;
- prioritize source-domain balance over raw volume;
- rerun downstream descriptive validation only after the next benchmark increment is large enough to make the comparison meaningful.

## 2026-04-30 — Public Benchmark v1.1 Third Released Wave

Completed:
- selected a third approved `v1.1` wave from the intake registry;
- added one English public-domain political baseline;
- added one Spanish public-domain literary baseline;
- added six controlled variants for each new baseline across the current perturbation axes;
- updated `evidence/public-benchmark-v1.1/` from a two-wave release to a three-wave release.

Current status:
- `public-benchmark-v1.1` now releases `6` baselines and `36` controlled variants;
- released languages in `v1.1` now include `de`, `ru`, `en`, `fr`, and `es`;
- released source classes in `v1.1` now include literary, government, and political prose;
- the benchmark remains small, but it is more suitable for rerunning descriptive validation than the earlier `v1.1` waves alone.

Next:
- rerun descriptive validation against the expanded benchmark layer;
- inspect whether benchmark-versus-campaign bridge summaries shift materially under the broader benchmark mix;
- continue benchmark growth only where provenance remains clear and source-domain skew is reduced rather than hidden.

## 2026-04-30 — Public Benchmark v1.1 Fourth Released Wave

Completed:
- selected a larger fourth approved `v1.1` wave from the intake registry;
- added one French public-domain political baseline;
- added one Spanish public-domain government baseline;
- added one German public-domain government baseline;
- added six controlled variants for each new baseline across the current perturbation axes;
- updated `evidence/public-benchmark-v1.1/` from a three-wave release to a four-wave release.

Current status:
- `public-benchmark-v1.1` now releases `9` baselines and `54` controlled variants;
- released languages remain `de`, `ru`, `en`, `fr`, and `es`, but source-domain balance is broader than in the earlier waves;
- released source classes remain literary, government, and political prose, with a less literary-heavy mix;
- the benchmark is still limited, but it is materially stronger for descriptive reruns than the smaller early `v1.1` releases.

Next:
- rerun descriptive validation against the larger benchmark layer;
- inspect whether benchmark-versus-campaign bridge and random-baseline distributions stabilize under the broader source mix;
- keep the next increment focused on provenance-clean breadth rather than on nominal language count alone.

## 2026-04-20

Completed:
- checked and normalised the core public metadata layer;
- added `.zenodo.json`;
- added `project_brief.md`;
- normalised `README.md` to the canonical research framing;
- created `TODO.md` and `ROADMAP.md`;
- ran repository terminology passes for prohibited public terms;
- updated author metadata in `CITATION.cff` and `.zenodo.json`;
- added `docs/phase2-plan.md` and `docs/terminology-policy.md`;
- added `docs/math.md` as a conservative mathematical note;
- added `docs/preprint-outline.md` and `docs/preprint-draft.md` as preprint scaffolds.

Next:
- historical note retained for context;
- current empirical status is now tracked in the 2026-04-27 entry above.
