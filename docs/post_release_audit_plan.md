# Post-Release Audit Plan

Run this audit after a public release and again after any incident, hotfix, or materially changed curated model set.

## Audit Window

- Day 0: immediately after release publication
- Day 7: first follow-up audit
- Day 30: confirm no drift in runtime, docs, or packaged contract artifacts

## Runtime Checks

- confirm `/health` returns the released version and expected uptime behavior
- confirm `/mcp/resources/contract-manifest` matches the published contract artifact hash
- confirm `/mcp/resources/release-bundle-manifest` matches the published bundle hash
- confirm anonymous access remains viewer-only
- confirm anonymous access is denied for `/metrics`
- confirm `/console`, `/console/assets/*`, and `/console/api/*` remain absent
- confirm operator-authenticated critical routes still require confirmation

## Trust-Bearing Payload Checks

- run the internal `rxode2` rehearsal model end to end:
  - `load_simulation`
  - `validate_simulation_request`
  - `run_verification_checks`
  - `export_oecd_report`
  - `run_simulation`
  - `get_results`
- verify `pbpkQualificationSummary.exportBlockPolicy` is present
- verify `humanReviewSummary.renderingGuardrails` is present
- verify `misreadRiskSummary` is present
- verify trust-bearing tool results still expose `trustSurfaceContract` for `validate_model_manifest`, `discover_models`, `validate_simulation_request`, `run_verification_checks`, and `export_oecd_report`
- verify `operatorReviewSignoff` remains descriptive and additive
- verify `/review_signoff/history` remains viewer-readable and returns immutable recorded/revoked event traces

## Curated Model Checks

- run `scripts/validate_model_manifests.py --strict --require-explicit-ngra --curated-publication-set`
- run `scripts/generate_regulatory_goldset_audit.py --check`
- verify curated examples still expose explicit NGRA declarations
- verify no curated example has silently widened its claim boundaries
- verify `regulatoryBenchmarkReadiness` remains advisory-only and still reflects the tracked gold-set summary

## Packaging And Integrity Checks

- run `scripts/generate_contract_artifacts.py --check`
- run `scripts/check_distribution_artifacts.py`
- retain the release bundle hash, contract manifest hash, and smoke/readiness JSON artifacts with the release evidence

## Trigger Immediate Investigation If

- runtime and packaged contract hashes diverge
- anonymous access can reach trust-bearing write or admin surfaces
- curated manifests regress to implicit NGRA boundaries
- trust-bearing summaries lose `misreadRiskSummary`, `summaryTransportRisk`, `renderingGuardrails`, or `exportBlockPolicy`
- trust-bearing MCP tool results lose `trustSurfaceContract` or point at stale surface paths
- a reviewer sign-off appears to widen authority rather than remain descriptive
