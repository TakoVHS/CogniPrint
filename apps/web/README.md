# CogniPrint Content Scanner Web

React/Vite frontend for the optional application layer deployed separately from the core research workstation.

This frontend is not the primary public scientific surface of CogniPrint. The current research-facing public surface remains the repository documentation, evidence snapshot, manuscript materials, and static site at `cogniprint.org`.

Current frontend behavior:

- calls `GET /ready` to verify API runtime readiness;
- creates and persists a browser-local `user_id`;
- calls `GET /account/status` to restore plan and quota state;
- calls `POST /scan` with that `user_id`;
- calls `POST /api/billing/create-checkout-session` for hosted subscription checkout;
- calls `POST /api/billing/create-portal-session` for customer portal access;
- handles Stripe return states on the root page via `?checkout=success` and `?checkout=cancelled`.

The pricing and account copy should stay research-first: hosted convenience, managed empirical reports, and review-oriented exports, not stronger scientific conclusions.

Current web/API integration expectations:

- `/ready` is the stronger runtime gate;
- `/account/status` restores plan, quota, and checkout availability;
- `/scan` remains the hosted analysis action used by the scanner UI.

Performance and audit notes are tracked in:

- `apps/web/PERFORMANCE.md`
