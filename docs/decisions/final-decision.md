# Final Decision

Status:

- pending reviewer input

Current state:

- no reviewer votes recorded yet
- no final decision between `increment` and `memo` has been made

Next action:

1. collect reviewer responses in `docs/decisions/votes-raw.txt`
2. run `python scripts/synthesize_decision.py --input docs/decisions/votes-raw.txt --output docs/decisions/final-decision.json`
3. if needed, run `python scripts/decision_gate_fallback.py --input docs/decisions/votes-raw.txt`
