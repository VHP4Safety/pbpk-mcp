# Hardening Migration Notes

These notes summarize the trust-architecture changes that now matter to operators, client developers, and downstream reviewers before public release.

## Security And Runtime Surface

- Anonymous mode is viewer-only. It no longer behaves like an operator or admin shortcut.
- Critical MCP and REST actions remain confirmation-gated even in local development.
- `/metrics` is admin-only, and the retired `/console` surface is no longer shipped.
- The local compose profile binds the anonymous surface to `127.0.0.1` by default.

## Model Curation And Discovery

- `validate_model_manifest` and `/mcp/resources/models` now expose `curationSummary`, not just raw manifest state.
- `validate_model_manifest`, `discover_models`, `validate_simulation_request`, `run_verification_checks`, and `export_oecd_report` now also expose a top-level `trustSurfaceContract` so thin MCP clients can find the nested trust-bearing surfaces and required adjacent caveats without guessing path layouts.
- `curationSummary` includes:
  - `misreadRiskSummary`
  - `summaryTransportRisk`
  - `renderingGuardrails`
  - `exportBlockPolicy`
  - `regulatoryBenchmarkReadiness`
- Client code that previously rendered only a label or manifest status should now co-display the required guardrail fields, or refuse the thin view.
- `regulatoryBenchmarkReadiness` is advisory only. It compares the current model dossier to the documentation/reproducibility bar implied by the fetched regulatory gold set, but it does not change `qualificationState`, release gating, or runtime permissions.

## NGRA Boundary And Review Semantics

- `assessmentContext.workflowRole`, `assessmentContext.populationSupport`, `pbpkQualificationSummary.evidenceBasis`, and `pbpkQualificationSummary.workflowClaimBoundaries` are now first-class trust-bearing boundary objects.
- `pbpkQualificationSummary.reviewStatus` now preserves unresolved dissent, open topics, resolved topics, and intervention summaries.
- `pbpkQualificationSummary.exportBlockPolicy` now carries machine-readable refusal semantics for lossy or decision-leaning downstream reuse.

## OECD Report Export

- `report.humanReviewSummary` now includes:
  - `summaryTransportRisk`
  - `renderingGuardrails`
  - `exportBlockPolicy`
  - `operatorReviewSignoff`
- `report.misreadRiskSummary` is mandatory.
- `report.exportBlockPolicy` mirrors the same refusal semantics at the report root for clients that only inspect top-level report metadata.

## Operator Review Sign-Off

- Sign-off is now auditable and scope-specific.
- The latest sign-off summary remains available at `/review_signoff`, and immutable event history is now viewer-readable at `/review_signoff/history`.
- Current scopes include:
  - `validate_simulation_request`
  - `run_verification_checks`
  - `export_oecd_report`
- Sign-off remains descriptive. It records bounded review, reviewer identity, rationale, and revocation state, but it does not create regulatory authority or override declared claim boundaries.

## Client Migration Guidance

- Stop treating runtime success, report export, or sign-off as implied decision readiness.
- If a reviewer or operator needs to understand how sign-off changed over time, inspect `/review_signoff/history` instead of relying only on the latest summary.
- If a thin MCP client consumes trust-bearing tool results, it should read `trustSurfaceContract` first and refuse any bare or lossy rendering that omits the listed adjacent caveats.
- If a UI cannot show `summaryTransportRisk`, `misreadRiskSummary`, and the required boundary fields inline, it should refuse the lossy rendering.
- If a downstream workflow wants stronger approval or override semantics, it must build that governance explicitly outside PBPK MCP rather than inferring it from the current payloads.
- If maintainers refresh the external benchmark corpus, regenerate `benchmarks/regulatory_goldset/regulatory_goldset_scorecard.json`, `benchmarks/regulatory_goldset/regulatory_goldset_summary.md`, and `benchmarks/regulatory_goldset/regulatory_goldset_audit_manifest.json` so the advisory bar stays hash-linked to the current lock files.
