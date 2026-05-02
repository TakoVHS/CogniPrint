# Web Performance Notes

This note records the current bounded performance and hygiene state of the optional web layer.

## Current changes

- the chart-heavy scan results surface is lazy-loaded;
- Vite output is expected to split the chart bundle away from the initial shell;
- the frontend keeps its runtime integration surface explicit around `/ready`, `/account/status`, and `/scan`.

## Audit triage

`npm audit` currently reports two moderate advisories tied to the Vite and esbuild toolchain.

Current reading:

- these are development-tooling advisories, not evidence of a runtime compromise in the built static bundle;
- the available automated fix is a semver-major Vite upgrade;
- that upgrade should be handled as a separate bounded pass, because it can change the frontend build and plugin surface materially.

## Next performance pass

The next bounded frontend performance pass should consider:

1. a Vite major-upgrade trial branch with explicit build verification;
2. further chunk analysis if the scan-results bundle continues to grow;
3. optional route- or feature-level splitting only if the hosted app layer gains more UI surface.
