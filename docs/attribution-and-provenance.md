# Attribution And Provenance

CogniPrint campaigns should preserve enough source information to explain where input texts came from and why they were appropriate for the research workflow. This document is not legal advice.

## Minimal Record

For each external source, record:

- `source_id`
- source name
- source reference, URL, or source ID
- license or rights statement
- acquisition date
- usage note
- storage scope

## Local Workflow

1. Put private/self-authored experimental texts in ignored local input paths.
2. Put shareable example texts in `workspace/input/public/` only after source review.
3. Record source metadata in `workspace/input/SOURCES.md`.
4. Run `make validate-sources` before preparing public materials.
5. Include dataset manifests and derived campaign outputs in colleague packs, not raw private texts.

## Campaign And Dataset Notes

Campaign configs may include `sources_file` and per-series `source_record_id` fields. Dataset manifests can reference a source metadata file when one is provided.
