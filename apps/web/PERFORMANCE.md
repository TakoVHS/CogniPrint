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
- the result shell and the chart surface are now split again:
  - `ResultPanel` remains a small result-shell chunk;
  - `FingerprintRadarChart` and `InsightBarChart` load separately;
  - shared Recharts categorical infrastructure remains concentrated in `generateCategoricalChart-*`.

## Audit triage

After the Vite 8 trial upgrade, `npm audit` reports zero vulnerabilities for the optional web layer.

Current reading:

- the prior Vite/esbuild advisories were resolved by the bounded major upgrade to Vite 8 and `@vitejs/plugin-react` 6;
- the main residual risk has shifted from audit noise to normal post-upgrade verification of build output and runtime wiring.

## Next performance pass

The next bounded frontend performance pass should consider:

1. further chunk analysis if the shared `generateCategoricalChart-*` chunk remains the dominant chart payload;
2. optional route- or feature-level splitting only if the hosted app layer gains more UI surface;
3. measuring whether the new CI browser gate stays stable enough to keep as a default required check.
