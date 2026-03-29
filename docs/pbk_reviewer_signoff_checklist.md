# PBK Reviewer Sign-Off Checklist

Use this checklist before recording a bounded-use operator sign-off on any trust-bearing PBPK MCP surface.

## Scope

This checklist applies to:

- `validate_simulation_request`
- `run_verification_checks`
- `export_oecd_report`

It does not create regulatory authority. It records that a reviewer examined the bounded-use surface and accepted the stated limitations for that scope.

When prior sign-off state matters, inspect `/review_signoff/history` before recording a new disposition so you can see whether the current surface was previously acknowledged, rejected, or revoked.

## Required Review Questions

- Does the requested use stay within the declared context of use and supported workflow role?
- Does the supported population match the intended population, including sex, life-stage, and variability assumptions?
- Does the evidence basis actually support the downstream question, or is this still NAM/IVIVE-only, literature-transferred, or otherwise limited?
- Do the claim boundaries still prohibit direct regulatory dose derivation, final decision recommendation, or broader reuse?
- Are there unresolved reviewer interventions, dissent, or missing-evidence items that should block stronger framing?
- Would the summary become misleading if forwarded as a screenshot, card, or short snippet?

## Required Payload Fields To Inspect

Before sign-off, inspect:

- `qualificationState`
- `pbpkQualificationSummary.reviewStatus`
- `pbpkQualificationSummary.evidenceBasis`
- `pbpkQualificationSummary.workflowClaimBoundaries`
- `pbpkQualificationSummary.exportBlockPolicy`
- `humanReviewSummary.summaryTransportRisk`
- `humanReviewSummary.renderingGuardrails`
- `misreadRiskSummary`
- `/review_signoff/history` for the same `simulationId` and scope when there is any question about prior sign-off state, revocation, or changing rationale

## Acceptable Dispositions

- `acknowledged`
  - Use when the surface was reviewed and the operator is only recording that bounded review occurred.
- `approved-for-bounded-use`
  - Use only when the stated scope, population, and evidence basis are still bounded exactly as declared.
- `rejected`
  - Use when the current surface is too easy to overread or the evidence package does not support the intended reuse.
- `revoked`
  - Use when a previously recorded sign-off no longer applies because context, evidence, or downstream use changed.

## Do Not Approve For Bounded Use When

- `directRegulatoryDoseDerivation` is anything other than truly supported and independently justified outside PBPK MCP.
- `summaryTransportRisk.detachedSummaryUnsafe` is `true` and the downstream consumer plans to forward only a thin summary.
- `reviewStatus.unresolvedDissentCount > 0` and the downstream framing would imply settled approval.
- The model is outside its declared context or supported population.
- Known missing evidence would materially change interpretation.

## Sign-Off Note Requirements

The recorded rationale should state:

- what was reviewed
- what remains bounded
- what remains external
- what stronger claim is still blocked

Good rationale example:

`Reviewed OECD report for research-only synthetic reference-model use. Qualification remains bounded, detached-summary risk remains active, and no direct regulatory dose derivation or external decision authority is implied.`
