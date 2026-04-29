# CogniPrint Content Scanner Web

React/Vite frontend for the optional application layer deployed separately from the core research workstation.

This frontend is not the primary public scientific surface of CogniPrint. The current research-facing public surface remains the repository documentation, evidence snapshot, manuscript materials, and static site at `cogniprint.org`.

Current frontend behavior:

- creates and persists a browser-local `user_id`;
- calls `GET /account/status` to restore plan and quota state;
- calls `POST /scan` with that `user_id`;
- calls `POST /billing/create-checkout-session` for the Pro upgrade flow;
- handles Stripe return states on the root page via `?checkout=success` and `?checkout=cancelled`.
