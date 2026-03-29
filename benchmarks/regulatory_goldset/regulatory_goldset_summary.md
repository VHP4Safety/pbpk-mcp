# Regulatory Gold-Set Benchmark Summary

This dossier distills the documentation and reproducibility bar implied by the fetched public-code PBPK benchmark packages.

## Benchmark Bar

- Source manifest: `benchmarks/regulatory_goldset/sources.lock.json`
- Source manifest SHA-256: `ba24143cfe7ddd976779d7c60d24754b35f8ecf0d361e15c8ad247e488af337b`
- Fetched lock: `benchmarks/regulatory_goldset/fetched.lock.json`
- Fetched lock SHA-256: `949db5491f40406ab4a0fc185952795bb88f1243ac5c4a3ead1b4fda7661ddca`
- Strict-core sources: tce_tsca_package, epa_voc_template
- Challenge-set sources: epa_pfas_template, pfos_ges_lac
- Documentation-only references: two_butoxyethanol_reference

The strict-core regulatory packages consistently emphasize context of use, runnable artifacts, software specificity, provenance depth, uncertainty treatment, reproducibility packaging, and hash-linked traceability. Challenge sets add stress-testing value, while documentation-only references mainly calibrate the confidence language.

### Consistent core expectations

- `publicTraceabilityHashability`: Public traceability and hashability

### Strong but more variable dimensions

- `contextOfUseClarity`: Context/use clarity
- `runnableCodeModelAvailability`: Runnable code/model availability
- `softwarePlatformSpecificity`: Software/platform specificity
- `parameterProvenanceDepth`: Parameter provenance depth

## Per-Source Findings

### EPA TSCA trichloroethylene PBPK package

- Role: `strict-core`
- Result: `fetched`
- Overall tier: `benchmark-grade`
- Dimension counts: 8 present, 0 partial, 0 missing, 0 not applicable
- Notes: Large public regulatory PBPK package used as the primary completeness benchmark. Archive is large enough that it should stay out of the tracked git tree.
- Strongest signals: Context/use clarity, Runnable code/model availability, Software/platform specificity, Parameter provenance depth

### EPA VOC PBPK template package

- Role: `strict-core`
- Result: `fetched`
- Overall tier: `strong-but-incomplete`
- Dimension counts: 1 present, 4 partial, 3 missing, 0 not applicable
- Notes: Primary public-code package for the solvent/VOC reproducibility benchmark stack. Covers the strict core models other than TCE.
- Strongest signals: Public traceability and hashability

### EPA PFAS PBPK template package

- Role: `adjunct-challenge-set`
- Result: `fetched`
- Overall tier: `challenge-set`
- Dimension counts: 1 present, 2 partial, 5 missing, 0 not applicable
- Notes: Use as the modern reproducibility and transparency stress test.
- Strongest signals: Public traceability and hashability

### PFOS-Ges-Lac open PFOS model

- Role: `adjunct-challenge-set`
- Result: `fetched`
- Overall tier: `challenge-set`
- Dimension counts: 3 present, 4 partial, 1 missing, 0 not applicable
- Notes: Open PFOS model adjunct for the PFAS challenge set.
- Strongest signals: Parameter provenance depth, Calibration vs evaluation separation, Public traceability and hashability

### 2-Butoxyethanol confidence-language benchmark

- Role: `documentation-only`
- Result: `unresolved-source`
- Overall tier: `documentation-only-reference`
- Dimension counts: 0 present, 1 partial, 0 missing, 7 not applicable
- Notes: Keep as a prose confidence benchmark, but do not treat it as a fetched executable/code package until a direct public model archive is confirmed.

## Internal Non-Benchmark Use-Case Comparison

- Internal use case: `var/models/rxode2/reference_compound/reference_compound_population_rxode2_model.R`
- Qualification state: `research-use`
- Benchmark resemblance: `research-example`
- Overall benchmark-readiness status: `below-benchmark-bar`
- Present dimensions: contextOfUseClarity, runnableCodeModelAvailability
- Partial dimensions: softwarePlatformSpecificity, parameterProvenanceDepth, calibrationVsEvaluationSeparation, uncertaintySensitivityVariability, reproducibilityPackCompleteness, publicTraceabilityHashability
- Missing dimensions: none
- Benchmark source manifest SHA-256: `ba24143cfe7ddd976779d7c60d24754b35f8ecf0d361e15c8ad247e488af337b`
- Benchmark fetched-lock SHA-256: `949db5491f40406ab4a0fc185952795bb88f1243ac5c4a3ead1b4fda7661ddca`
- Benchmark source resolution: `direct-lock-files`

The synthetic reference model remains a `research-use` internal MCP use case. It is useful for smoke testing, audit rehearsal, and trust-surface validation, but it is not part of the regulatory benchmark corpus.

### Top dossier-improvement signals

- `parameterProvenanceDepth`: Stronger parameter provenance expectations. Evaluated from profile.parameterProvenance, profile.parameterTableBundleMetadata, hooks.parameterTable, hooks.parameterTableSidecar. Suggested next artifacts: Attach a tabular parameter provenance bundle with names, units, sources, and rationale fields. Expose whether parameter values are literature-sourced, optimized, transferred, or runtime-only placeholders.
- `calibrationVsEvaluationSeparation`: Clearer calibration-vs-evaluation reporting. Evaluated from profile.modelPerformance, profile.performanceEvidenceBundleMetadata, hooks.performanceEvidence, hooks.performanceEvidenceSidecar. Suggested next artifacts: Separate fit/calibration evidence from evaluation or predictive-check evidence in the manifest-facing dossier. Name which datasets or checks were used for optimization versus evaluation.
- `uncertaintySensitivityVariability`: More structured uncertainty and variability evidence. Evaluated from profile.uncertainty, profile.uncertaintyEvidenceBundleMetadata, profile.populationSupport, hooks.uncertaintyEvidence, hooks.uncertaintyEvidenceSidecar. Suggested next artifacts: Add structured uncertainty rows that distinguish local sensitivity, variability propagation, and other uncertainty classes. State clearly whether variability support is mechanistic, assumed, transferred, or absent.
- `reproducibilityPackCompleteness`: Clearer reproducibility-pack signals. Evaluated from manifestStatus, profileSource, profile.modelPerformance, profile.parameterProvenance, profile.uncertainty, hooks.parameterTable, hooks.performanceEvidence, hooks.uncertaintyEvidence. Suggested next artifacts: Bundle the runnable model, validation-oriented evidence, parameter provenance, and run instructions as one coherent dossier. Avoid leaving key evidence split across ad hoc notes or runtime-only outputs.

## Prioritized MCP Improvement Targets

- `parameterProvenanceDepth`: Stronger parameter provenance expectations. This dimension is part of the documentation/reproducibility bar implied by the fetched regulatory benchmark corpus and should be clearer in MCP trust/reporting surfaces.
- `calibrationVsEvaluationSeparation`: Clearer calibration-vs-evaluation reporting. This dimension is part of the documentation/reproducibility bar implied by the fetched regulatory benchmark corpus and should be clearer in MCP trust/reporting surfaces.
- `uncertaintySensitivityVariability`: More structured uncertainty and variability evidence. This dimension is part of the documentation/reproducibility bar implied by the fetched regulatory benchmark corpus and should be clearer in MCP trust/reporting surfaces.
- `reproducibilityPackCompleteness`: Clearer reproducibility-pack signals. This dimension is part of the documentation/reproducibility bar implied by the fetched regulatory benchmark corpus and should be clearer in MCP trust/reporting surfaces.
- `softwarePlatformSpecificity`: Better software/platform and run-instruction declaration. This dimension is part of the documentation/reproducibility bar implied by the fetched regulatory benchmark corpus and should be clearer in MCP trust/reporting surfaces.
- `publicTraceabilityHashability`: Better traceability and hash-linked evidence packaging. This dimension is part of the documentation/reproducibility bar implied by the fetched regulatory benchmark corpus and should be clearer in MCP trust/reporting surfaces.
- `contextOfUseClarity`: Clearer context-of-use declaration. This dimension is part of the documentation/reproducibility bar implied by the fetched regulatory benchmark corpus and should be clearer in MCP trust/reporting surfaces.
- `runnableCodeModelAvailability`: Sharper runnable-vs-reference model declaration. This dimension is part of the documentation/reproducibility bar implied by the fetched regulatory benchmark corpus and should be clearer in MCP trust/reporting surfaces.
