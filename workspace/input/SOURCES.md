# CogniPrint Input Sources

This file records source metadata for local CogniPrint research inputs. It supports reproducibility and does not provide legal advice.

Private or sensitive experimental texts should stay local-only and should not be committed to the public repository.

## source-id: empirical-campaign-002-self-authored-baseline

- source_name: Self-authored CogniPrint baseline note
- source_ref: workspace/input/original.txt
- source_class: self-authored
- license: self-authored local research use
- acquisition_date: 2026-04-22
- usage_note: Baseline text for a local controlled perturbation study. The baseline is short, so resulting campaign outputs should be treated as micro-series empirical notes.
- storage_scope: local-only unless explicitly prepared for public release

## source-id: empirical-campaign-002-light-edit

- source_name: Self-authored light edit
- source_ref: workspace/input/edited.txt
- source_class: self-authored
- license: self-authored local research use
- acquisition_date: 2026-04-22
- usage_note: Light edit derived from the local baseline for measured profile-shift comparison.
- storage_scope: local-only unless explicitly prepared for public release

## source-id: empirical-campaign-002-controlled-variants

- source_name: Self-authored controlled perturbation variants
- source_ref: workspace/input/variants/
- source_class: self-authored
- license: self-authored local research use
- acquisition_date: 2026-04-22
- usage_note: Controlled variants derived from the local baseline. Each variant is intended to vary one main perturbation axis where possible.
- storage_scope: local-only unless explicitly prepared for public release

## variant-map

- 01_punctuation_cleanup.txt: punctuation-only surface change
- 02_minor_lexical_substitution.txt: mild lexical substitution
- 03_sentence_split_merge.txt: sentence segmentation change
- 04_word_order_shift.txt: word-order and syntax shift
- 05_compressed_version.txt: controlled compression
- 06_expanded_version.txt: controlled expansion
- 07_formalized_style.txt: style formalization
- 08_informalized_style.txt: style relaxation
- 09_strong_rewrite_same_claim.txt: stronger paraphrase preserving the central claim
- 10_translated_or_crosslingual.txt: cross-lingual variant preserving the topic
- strongly-edited.txt: earlier strong local edit retained for continuity
