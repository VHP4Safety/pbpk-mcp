## PBPK-side Object Schemas

This directory publishes the versioned JSON Schemas for the PBPK-side NGRA handoff objects exposed by PBPK MCP.

Current schema family:

- `assessmentContext.v1`
- `pbpkQualificationSummary.v1`
- `uncertaintySummary.v1`
- `uncertaintyHandoff.v1`
- `uncertaintyRegisterReference.v1`
- `internalExposureEstimate.v1`
- `pointOfDepartureReference.v1`
- `berInputBundle.v1`

Example payloads live under `schemas/examples/`.

The published contract inventory for this schema family lives in:

- `docs/architecture/contract_manifest.json`
- `/mcp/resources/contract-manifest`

Schema design rules for this family:

- require only the stable core fields that downstream clients should rely on
- allow additive convenience fields so `pbpk-mcp.v1` can grow without breaking validation
- keep BER calculation and decision policy outside PBPK MCP
- treat these schemas as the published machine-readable contract for the PBPK-side handoff layer
- surface exposure-led NGRA role, population-support boundaries, evidence-basis status, and claim-boundary status additively rather than creating a second hidden qualification layer
