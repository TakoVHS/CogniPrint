# CogniPrint Data Sourcing Policy

This document is a cautious research data policy for CogniPrint. It is not legal advice.

## Preferred Source Classes

- Self-authored texts are preferred for local empirical campaigns.
- Public-domain texts can be used when the source status is recorded.
- Openly licensed texts can be used when attribution and license metadata are recorded.
- Private or sensitive local texts should remain outside public-share paths and should not be committed.

## Public And Private Storage

- Use `workspace/input/public/` only for examples that are safe to share publicly.
- Use `workspace/input/private/` or ignored local paths for private/local-only experimental material.
- Do not store copyright-sensitive full texts in the public repository unless the rights are clearly compatible.
- Do not intentionally include personal data in example corpora.

## Required Source Metadata

Every external text should have a source record with:

- source name
- URL or source ID
- license
- acquisition date
- usage note

Use `workspace/input/SOURCES.md` as the local record template.

## Research Use

The purpose of this policy is reproducibility: campaign inputs should be traceable enough for internal review, future dataset preparation, and colleague-facing scientific discussion. Source records should not be treated as legal clearance.
