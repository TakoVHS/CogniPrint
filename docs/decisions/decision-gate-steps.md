# Decision Gate Workflow

1. [ ] Send reviewers the frozen review packet and the two decision anchors:
   - `docs/benchmark-shift-note-v1.1.md`
   - `docs/benchmark-decision-memo-v1.1.md`
2. [ ] Record reviewer status in `docs/decision-gate-tracker.md`
3. [ ] Set and document a reply deadline
4. [ ] Send one reminder before the deadline
5. [ ] Collect raw responses in `docs/decisions/votes-raw.txt`
6. [ ] Run `python scripts/synthesize_decision.py --input docs/decisions/votes-raw.txt`
7. [ ] If the result is ambiguous, run `python scripts/decision_gate_fallback.py --input docs/decisions/votes-raw.txt`
8. [ ] Save the final outcome in `docs/decisions/final-decision.md`
9. [ ] Commit the decision outcome before any `wave-005` action
