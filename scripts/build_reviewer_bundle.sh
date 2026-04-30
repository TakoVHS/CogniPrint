#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATE_TAG="${1:-$(date +%Y%m%d)}"
BUNDLE_ROOT="${ROOT}/release_artifacts/cogniprint_reviewer_${DATE_TAG}"
ARCHIVE_PATH="${ROOT}/release_artifacts/cogniprint_reviewer_${DATE_TAG}.tar.gz"

rm -rf "${BUNDLE_ROOT}"
mkdir -p "${BUNDLE_ROOT}/evidence" "${BUNDLE_ROOT}/docs"

cp -R "${ROOT}/evidence/empirical-v1" "${BUNDLE_ROOT}/evidence/"
cp -R "${ROOT}/evidence/public-benchmark-v1" "${BUNDLE_ROOT}/evidence/"
cp -R "${ROOT}/evidence/statistical-validation-v1" "${BUNDLE_ROOT}/evidence/"
cp "${ROOT}/docs/current-state-summary.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/claims-matrix.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/benchmark-protocol.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/public-benchmark-plan.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/statistical-validation-plan.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/manuscript-readiness-checklist.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/due-diligence-response.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/benchmark-shift-note-v1.1.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/benchmark-decision-memo-v1.1.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/reviewer-release-v0.2.0.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/reviewer-handoff-message.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/reviewer-feedback-intake.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/claims-review-questionnaire.md" "${BUNDLE_ROOT}/docs/"
cp "${ROOT}/docs/benchmark-expansion-plan.md" "${BUNDLE_ROOT}/docs/"
test -f "${ROOT}/docs/validation-status.md" && cp "${ROOT}/docs/validation-status.md" "${BUNDLE_ROOT}/docs/" || true
test -f "${ROOT}/docs/validation-status.json" && cp "${ROOT}/docs/validation-status.json" "${BUNDLE_ROOT}/docs/" || true
test -f "${ROOT}/docs/feedback-synthesis-latest.md" && cp "${ROOT}/docs/feedback-synthesis-latest.md" "${BUNDLE_ROOT}/docs/" || true

mkdir -p "${ROOT}/release_artifacts"
tar -czf "${ARCHIVE_PATH}" -C "${ROOT}/release_artifacts" "cogniprint_reviewer_${DATE_TAG}"
printf 'Reviewer bundle written: %s\n' "${ARCHIVE_PATH}"
