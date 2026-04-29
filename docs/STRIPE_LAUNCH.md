# Stripe Launch Notes

The authoritative setup document for the current billing layer is [`docs/stripe-billing-runbook.md`](docs/stripe-billing-runbook.md).

Current posture:

- Stripe integration is test-mode first.
- Real secret keys must not be committed.
- The billing layer is optional and separate from the research core.
- Hosted access must not be described as stronger scientific evidence.

Use the runbook for:

- test-mode product and price setup;
- Stripe CLI webhook forwarding;
- checkout and customer portal verification;
- local webhook confirmation and subscription-state checks.
