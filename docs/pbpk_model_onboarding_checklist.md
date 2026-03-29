# PBPK Model Onboarding Checklist

Use this checklist when onboarding any new PBPK/PBK model into PBPK MCP, whether the chemical is diazinon, trichloroethylene, a PFAS, or an internal research example.

This checklist is intentionally about the MCP trust pipeline, not about promoting every runnable model to benchmark or regulatory status.

## Purpose

PBPK MCP should treat a new model as trustworthy only to the extent that its runtime artifact, declared scope, evidence surfaces, and review state support that trust.

The chemical name is not the trust signal.

## Classification First

Before discovery or load, classify the incoming model dossier as one of:

- `research-example`
- `illustrative-example`
- `regulatory-candidate`
- `reproducibility-challenge-set`
- `documentation-only-reference`

Internal examples such as the bundled synthetic reference model are useful for MCP rehearsal, smoke testing, audit generation, and trust-surface checks. They are not part of the external regulatory gold-set benchmark corpus.

## Runtime Artifact Gate

Confirm the model is entering through a supported runtime or normalization path:

- `rxode2` runtime module: `.R`
- OSPSuite runtime model: `.pkml`
- external normalization only: `ingest_external_pbpk_bundle`

Do not treat `.mmd` or `.pksim5` as runtime formats. They are conversion-source formats only.

## Minimum Discovery And Manifest Gate

Before load, run:

```bash
python3 scripts/release_readiness_check.py --skip-unit-tests
curl -s http://localhost:8000/mcp/resources/models | jq .
curl -s http://localhost:8000/mcp/call_tool \
  -H 'Content-Type: application/json' \
  -d '{"tool":"validate_model_manifest","arguments":{"filePath":"/absolute/path/to/model"}}' | jq .
```

The manifest review should explicitly inspect:

- `qualificationState`
- `manifestStatus`
- `manifest.ngraCoverage`
- `curationSummary`
- `curationSummary.regulatoryBenchmarkReadiness`
- `curationSummary.misreadRiskSummary`
- `curationSummary.summaryTransportRisk`
- `curationSummary.cautionSummary`
- `curationSummary.exportBlockPolicy`

## Required Trust Declarations

Do not proceed with a serious onboarding review until the model dossier explicitly declares:

- `contextOfUse`
- `workflowRole`
- `populationSupport`
- `evidenceBasis`
- `workflowClaimBoundaries`

These declarations are the minimum needed to keep runnable, bounded, and decision-adjacent from collapsing into one vague readiness signal.

## Required Evidence Surfaces

A stronger model dossier should also declare, or clearly admit the absence of:

- `parameterProvenance`
- `modelPerformance`
- `uncertainty`
- `platformQualification`

Use `curationSummary.regulatoryBenchmarkReadiness.prioritizedGaps` and `recommendedNextArtifacts` to decide what should be improved next. Those benchmark-derived gaps are advisory only; they do not upgrade or downgrade qualification state by themselves.

## Benchmark Relationship

Use the regulatory gold set as the documentation and reproducibility bar:

- `benchmarks/regulatory_goldset/regulatory_goldset_summary.md`

Use internal examples such as the synthetic reference model only as:

- MCP runtime acceptance cases
- smoke-test and audit fixtures
- bounded research-use comparisons against the benchmark bar

Do not present an internal example as part of the benchmark corpus.

## Execution Gate

Only after the manifest gate is acceptable, run:

```bash
curl -s http://localhost:8000/mcp/call_tool \
  -H 'Content-Type: application/json' \
  -d '{"tool":"load_simulation","arguments":{"filePath":"/absolute/path/to/model","simulationId":"candidate-onboarding"}}' | jq .

curl -s http://localhost:8000/mcp/call_tool \
  -H 'Content-Type: application/json' \
  -d '{"tool":"validate_simulation_request","arguments":{"simulation_id":"candidate-onboarding"}}' | jq .

curl -s http://localhost:8000/mcp/call_tool \
  -H 'Content-Type: application/json' \
  -d '{"tool":"run_verification_checks","arguments":{"simulation_id":"candidate-onboarding"}}' | jq .
```

Treat executable success as runtime evidence only. It does not replace calibration evidence, predictive evaluation, uncertainty analysis, or reviewer judgment.

## Review And Report Gate

Before sharing the output as anything more than a private technical check, inspect:

- `pbpkQualificationSummary.reviewStatus`
- `pbpkQualificationSummary.exportBlockPolicy`
- `humanReviewSummary`
- `humanReviewSummary.renderingGuardrails`
- `humanReviewSummary.summaryTransportRisk`
- `misreadRiskSummary`
- `/review_signoff/history`

Then, if a bounded sign-off is appropriate, use:

- `docs/pbk_reviewer_signoff_checklist.md`

If an OECD export is needed, generate it and confirm the same caution, transport-risk, and governance fields remain visible in the report payload.

## Do Not Do These Things

- Do not treat the chemical identity as a proxy for trust.
- Do not treat runnable as regulatory-ready.
- Do not treat a research-use example as a benchmark.
- Do not collapse operational readiness and scientific support.
- Do not forward a thin summary when `summaryTransportRisk.detachedSummaryUnsafe` is `true`.

## Practical Acceptance Path

For a new chemical such as diazinon, the intended path is:

1. classify the model dossier honestly
2. validate the static manifest
3. close the highest benchmark-derived documentation gaps
4. load and verify the runtime artifact
5. inspect review, caution, and export-boundary surfaces
6. record bounded sign-off only if the declared scope still holds

Use this checklist with:

- `docs/architecture/mcp_payload_conventions.md`
- `docs/pbk_reviewer_signoff_checklist.md`
- `docs/github_publication_checklist.md`
- `benchmarks/regulatory_goldset/regulatory_goldset_summary.md`
