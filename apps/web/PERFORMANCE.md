# Web Performance Notes

This note records the current bounded performance and hygiene state of the optional web layer.

## Current changes

- the chart-heavy scan results surface is lazy-loaded;
- Vite 8 output splits the chart bundle away from the initial shell;
- the frontend keeps its runtime integration surface explicit around `/ready`, `/account/status`, and `/scan`.
- build-only tooling (`vite`, `typescript`, `@vitejs/plugin-react`) is kept in `devDependencies`, not the runtime dependency set.
- the web package now declares the Vite 8 Node engine requirement (`^20.19.0 || >=22.12.0`).
- the hosted scanner flow now has a browser-level verification path via `make web-browser-verify`.
- the browser-level hosted scanner verification now runs in CI as a separate heavy gate with artifact upload.
- the CI browser gate now emits a structured verification summary JSON and a GitHub Actions step summary for run-to-run stability observation.
- the same gate is scheduled to run daily so flakiness can be observed across repeated runs, not only on code changes.
- the chart surface no longer depends on `recharts`;
- the former `generateCategoricalChart-*` shared payload has been removed from the production build;
- the current post-remediation chunk shape is:
  - `ResultPanel-*` at about `2.50 kB`;
  - `FingerprintRadarChart-*` at about `1.47 kB`;
  - `InsightBarChart-*` at about `1.09 kB`;
  - `index-*` at about `13.96 kB`;
  - `react-vendor-*` at about `139.83 kB`.

## Audit triage

After the Vite 8 trial upgrade, `npm audit` reports zero vulnerabilities for the optional web layer.

Current reading:

- the prior Vite/esbuild advisories were resolved by the bounded major upgrade to Vite 8 and `@vitejs/plugin-react` 6;
- the main residual risk has shifted from audit noise to normal post-upgrade verification of build output and runtime wiring.

## Next performance pass

The next bounded frontend performance pass should consider:

1. observing whether the new browser-level CI gate stays stable enough to remain required by default;
2. optional route- or feature-level splitting only if the hosted app layer gains materially more UI surface;
3. revisiting `react-vendor-*` only if bundle pressure returns after new UI additions.
