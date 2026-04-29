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
  - `5` baseline excerpts;
  - `10` controlled variants;
  - `2` released languages;
  - literary, political, and government prose source classes;
- added `datasets/public-benchmark-v1/metadata/samples.csv`;
- added `datasets/public-benchmark-v1/metadata/release-criteria.md`;
- updated `evidence/public-benchmark-v1/manifest.json` and `counts.json` to reflect the released subset.

Current status:
- the benchmark layer is now scaffolded in the repository;
- an expanded small public benchmark subset is now released;
- the active public empirical package remains `evidence/empirical-v1/`.

Next:
- prepare a first small benchmark corpus with explicit licensing and provenance;
- expand the released public subset beyond the initial three baselines and six variants;
- request external review on the current evidence package and manuscript layer;
- implement the planned statistical validation layer after benchmark assembly.

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
