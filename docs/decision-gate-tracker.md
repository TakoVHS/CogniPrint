# Decision Gate Tracker

This tracker is used after reviewers receive the current benchmark decision packet.

Primary decision anchors:

- `docs/benchmark-shift-note-v1.1.md`
- `docs/benchmark-decision-memo-v1.1.md`

## Reviewer decisions

| Reviewer | Decision | Date | Feedback link or note |
| --- | --- | --- | --- |
| reviewer-1 | pending |  |  |
| reviewer-2 | pending |  |  |
| reviewer-3 | pending |  |  |

Accepted values for `Decision`:

- `increment`
- `memo`
- `abstain`

## Decision threshold

- choose `increment` only if at least two thirds of reviewers judge the current shift moderate enough for the next benchmark increment;
- choose `memo` only if at least two thirds of reviewers judge the current descriptive layer still too sensitive to benchmark composition;
- otherwise treat the outcome as ambiguous and use the fallback path.

## Fallback path

If the outcome is ambiguous:

1. do not strengthen inferential wording;
2. do not launch a large new benchmark wave automatically;
3. either ask one clarifying follow-up question to reviewers or prepare a narrow interpretation memo before deciding on `wave-005`.
