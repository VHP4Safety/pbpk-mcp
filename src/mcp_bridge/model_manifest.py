"""Static manifest validation helpers for supported PBPK model files."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

try:  # pragma: no cover - import fallback for direct module loading in tests
    from .benchmarking.regulatory_goldset import derive_manifest_benchmark_readiness
except ImportError:  # pragma: no cover - direct module loading fallback
    from mcp_bridge.benchmarking.regulatory_goldset import derive_manifest_benchmark_readiness

SUPPORTED_MODEL_EXTENSIONS = {
    ".pkml": "ospsuite",
    ".r": "rxode2",
}

_R_HOOK_PATTERNS = {
    "modelProfile": re.compile(r"\bpbpk_model_profile\s*<-"),
    "validationHook": re.compile(r"\bpbpk_validate_request\s*<-"),
    "deterministicSimulation": re.compile(r"\bpbpk_run_simulation\s*<-"),
    "populationSimulation": re.compile(r"\bpbpk_run_population\s*<-"),
    "parameterTable": re.compile(r"\bpbpk_parameter_table\s*<-"),
    "performanceEvidence": re.compile(r"\bpbpk_performance_evidence\s*<-"),
    "uncertaintyEvidence": re.compile(r"\bpbpk_uncertainty_evidence\s*<-"),
    "verificationEvidence": re.compile(r"\bpbpk_verification_evidence\s*<-"),
    "platformQualificationEvidence": re.compile(r"\bpbpk_platform_qualification_evidence\s*<-"),
    "runtimeVerificationHook": re.compile(r"\bpbpk_run_verification_checks\s*<-"),
}
_R_SECTION_PATTERNS = {
    "contextOfUse": re.compile(r"\bcontextOfUse\s*="),
    "applicabilityDomain": re.compile(r"\bapplicabilityDomain\s*="),
    "modelPerformance": re.compile(r"\bmodelPerformance\s*="),
    "parameterProvenance": re.compile(r"\bparameterProvenance\s*="),
    "uncertainty": re.compile(r"\buncertainty\s*="),
    "implementationVerification": re.compile(r"\bimplementationVerification\s*="),
    "platformQualification": re.compile(r"\bplatformQualification\s*="),
    "peerReview": re.compile(r"\bpeerReview\s*="),
}
_REQUIRED_SECTION_FIELDS = {
    "contextOfUse": ("scientificPurpose", "decisionContext", "regulatoryUse"),
    "applicabilityDomain": ("type", "qualificationLevel"),
    "modelPerformance": ("status",),
    "parameterProvenance": ("status",),
    "uncertainty": ("status",),
    "implementationVerification": ("status",),
    "platformQualification": ("status",),
    "peerReview": ("status",),
}
_NGRA_DECLARATION_FIELDS = {
    "workflowRole": ("workflowRole", "ngraWorkflowRole", "exposureLedWorkflow"),
    "populationSupport": ("populationSupport",),
    "evidenceBasis": ("evidenceBasis",),
    "workflowClaimBoundaries": ("workflowClaimBoundaries", "claimBoundaries"),
}
_NGRA_DECLARATION_MESSAGES = {
    "workflowRole": (
        "Scientific profile does not declare an explicit workflowRole/ngraWorkflowRole block; "
        "runtime exports will keep the PBPK role description conservative rather than implying "
        "model-specific IVIVE or dosimetry ownership."
    ),
    "populationSupport": (
        "Scientific profile does not declare an explicit populationSupport block; runtime exports "
        "will require human review for extrapolation outside declared population contexts."
    ),
    "evidenceBasis": (
        "Scientific profile does not declare an explicit evidenceBasis block; runtime exports will "
        "label in vivo and NAM/IVIVE support as not declared."
    ),
    "workflowClaimBoundaries": (
        "Scientific profile does not declare workflowClaimBoundaries/claimBoundaries; runtime "
        "exports will conservatively avoid claiming direct support for reverse/forward dosimetry "
        "or direct regulatory dose derivation."
    ),
}
_NGRA_ISSUE_CODES = {
    "workflowRole": "ngra_workflow_role_missing",
    "populationSupport": "ngra_population_support_missing",
    "evidenceBasis": "ngra_evidence_basis_missing",
    "workflowClaimBoundaries": "ngra_workflow_claim_boundaries_missing",
}
_NGRA_RUNTIME_FALLBACKS = {
    "workflowRole": (
        "Runtime exports fall back to a conservative PBPK-in-workflow role description and do not "
        "infer model-specific IVIVE ownership."
    ),
    "populationSupport": (
        "Runtime exports fall back to conservative population support semantics and keep "
        "extrapolation outside declared contexts behind human review."
    ),
    "evidenceBasis": (
        "Runtime exports treat in vivo support, mixed-evidence status, and NAM/IVIVE-only support "
        "as not declared."
    ),
    "workflowClaimBoundaries": (
        "Runtime exports conservatively avoid direct support claims for reverse dosimetry, forward "
        "dosimetry, exposure-led prioritization, or regulatory dose derivation unless declared."
    ),
}
_EXAMPLE_QUALIFICATIONS = {"demo-only", "illustrative-example", "integration-example"}
_RESEARCH_QUALIFICATIONS = {
    "research-use",
    "research-only",
    "runtime-guardrails",
    "runtime-load-verified",
}
_REGULATORY_QUALIFICATIONS = {
    "fit-for-purpose",
    "qualified",
    "externally-qualified",
    "regulatory-use",
    "regulatory-qualified",
}


def ospsuite_profile_sidecar_candidates(file_path: Path) -> tuple[Path, ...]:
    stem = file_path.with_suffix("")
    return (
        Path(f"{stem}.profile.json"),
        Path(f"{stem}.pbpk.json"),
        Path(f"{file_path}.profile.json"),
    )


def performance_evidence_sidecar_candidates(file_path: Path) -> tuple[Path, ...]:
    stem = file_path.with_suffix("")
    return (
        Path(f"{stem}.performance.json"),
        Path(f"{stem}.performance-evidence.json"),
        Path(f"{file_path}.performance.json"),
        Path(f"{file_path}.performance-evidence.json"),
    )


def uncertainty_evidence_sidecar_candidates(file_path: Path) -> tuple[Path, ...]:
    stem = file_path.with_suffix("")
    return (
        Path(f"{stem}.uncertainty.json"),
        Path(f"{stem}.uncertainty-evidence.json"),
        Path(f"{file_path}.uncertainty.json"),
        Path(f"{file_path}.uncertainty-evidence.json"),
    )


def parameter_table_sidecar_candidates(file_path: Path) -> tuple[Path, ...]:
    stem = file_path.with_suffix("")
    return (
        Path(f"{stem}.parameters.json"),
        Path(f"{stem}.parameter-table.json"),
        Path(f"{file_path}.parameters.json"),
        Path(f"{file_path}.parameter-table.json"),
    )


def normalize_token(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, Mapping):
        return None
    candidate = str(value).strip().lower()
    if not candidate:
        return None
    normalized = re.sub(r"[^a-z0-9]+", "-", candidate).strip("-")
    return normalized or None


def _safe_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        candidate = value.strip()
        return candidate or None
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            resolved = _safe_text(item)
            if resolved:
                return resolved
        return None
    return str(value)


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _issue(code: str, message: str, *, field: str | None = None, severity: str = "error") -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "field": field,
        "severity": severity,
    }


def _normalize_text_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        candidate = value.strip()
        return [candidate] if candidate else []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        values: list[str] = []
        for item in value:
            values.extend(_normalize_text_values(item))
        deduped: list[str] = []
        for item in values:
            if item not in deduped:
                deduped.append(item)
        return deduped
    text = _safe_text(value)
    return [text] if text else []


def _value_is_declared(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, Mapping):
        return any(_value_is_declared(item) for item in value.values())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return any(_value_is_declared(item) for item in value)
    if isinstance(value, bool):
        return True
    return _safe_text(value) is not None


def _record_entry_count(value: Any) -> int:
    if isinstance(value, Mapping):
        return 1
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return sum(1 for item in value if isinstance(item, Mapping))
    return 0


def _declared_profile_alias(profile: Mapping[str, Any], field_names: Sequence[str]) -> str | None:
    for field_name in field_names:
        if _value_is_declared(profile.get(field_name)):
            return field_name
    return None


def _declared_text_alias(text: str, field_names: Sequence[str]) -> str | None:
    for field_name in field_names:
        if re.search(rf"\b{re.escape(field_name)}\s*=", text):
            return field_name
    return None


def _population_scope_hint_fields(applicability: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(applicability, Mapping):
        return []

    hints: list[str] = []
    for field_name in (
        "species",
        "sex",
        "lifeStage",
        "age",
        "ageGroup",
        "physiology",
        "genotype",
        "phenotype",
    ):
        if _value_is_declared(applicability.get(field_name)):
            hints.append(field_name)
    return hints


def _curation_review_label(
    *,
    qualification_label: str | None,
    manifest_status: str | None,
    ngra_declarations_explicit: bool,
    risk_assessment_ready: bool,
) -> str:
    qualification_prefix = qualification_label or "Undeclared"
    manifest_phrase = {
        "valid": "with complete static curation",
        "partial": "with partial static curation",
        "missing": "without model-specific static curation",
    }.get(manifest_status, "with unknown static curation")
    ngra_phrase = (
        "and explicit NGRA boundaries"
        if ngra_declarations_explicit
        else "and implicit NGRA boundaries"
    )
    readiness_phrase = (
        "risk-assessment-ready"
        if risk_assessment_ready
        else "not regulatory-ready"
    )
    return f"{qualification_prefix} {manifest_phrase} {ngra_phrase}; {readiness_phrase}."


def _curation_human_summary(
    *,
    qualification_label: str | None,
    manifest_status: str | None,
    risk_assessment_ready: bool,
    ngra_declarations_explicit: bool,
    missing_sections: Sequence[str],
    missing_ngra: Sequence[str],
) -> str:
    qualification_prefix = (qualification_label or "Undeclared").lower()
    summary = (
        f"{qualification_prefix.capitalize()} model with static manifest status "
        f"'{manifest_status or 'unknown'}'. "
    )
    if ngra_declarations_explicit:
        summary += "NGRA workflow role, population support, evidence basis, and claim boundaries are explicit. "
    elif missing_ngra:
        summary += (
            "NGRA declarations are still implicit for "
            f"{', '.join(missing_ngra)}. "
        )
    if missing_sections:
        summary += f"Section gaps remain in {', '.join(missing_sections)}. "
    summary += (
        "Treat this as risk-assessment-ready."
        if risk_assessment_ready
        else "Do not treat this as regulatory-ready without further evidence."
    )
    return summary


def _curation_misread_risk_summary(
    *,
    qualification_label: str | None,
    manifest_status: str | None,
    risk_assessment_ready: bool,
    ngra_declarations_explicit: bool,
    missing_sections: Sequence[str],
    missing_ngra: Sequence[str],
) -> dict[str, Any]:
    statements: list[dict[str, Any]] = []

    def add_statement(code: str, message: str, current_status: str | None = None) -> None:
        payload: dict[str, Any] = {"code": code, "message": message}
        if current_status:
            payload["currentStatus"] = current_status
        statements.append(payload)

    qualification_text = qualification_label or "undeclared"
    manifest_text = manifest_status or "unknown"
    add_statement(
        "static-curation-is-not-decision-readiness",
        (
            "Static manifest completeness and explicit NGRA declarations do not, by themselves, "
            "prove broad decision readiness, external validation, or regulatory acceptability."
        ),
        current_status=f"qualification={qualification_text}; manifest={manifest_text}",
    )

    if not risk_assessment_ready:
        add_statement(
            "not-risk-assessment-ready",
            (
                "Do not treat this model as risk-assessment-ready or regulatory-ready without "
                "additional evidence and context-specific human review."
            ),
            current_status=qualification_text,
        )
    else:
        add_statement(
            "declared-context-still-applies",
            (
                "Even when the manifest is structured for within-context qualification, reuse "
                "outside the declared context of use still requires human review."
            ),
            current_status=qualification_text,
        )

    if not ngra_declarations_explicit:
        add_statement(
            "implicit-ngra-boundaries",
            (
                "Some NGRA boundary declarations are still implicit, so downstream runtime and "
                "export surfaces will fall back to conservative defaults rather than model-specific claims."
            ),
            current_status=", ".join(missing_ngra) if missing_ngra else "undeclared-ngra-boundaries",
        )

    if missing_sections:
        add_statement(
            "manifest-section-gaps",
            (
                "Important manifest sections remain missing or incomplete. Treat discovery and "
                "validation summaries as incomplete curation, not as full dossier support."
            ),
            current_status=", ".join(missing_sections),
        )

    add_statement(
        "detached-summary-overread",
        (
            "Discovery cards, screenshots, short API snippets, or forwarded manifest summaries can "
            "make the trust-bearing review label look stronger than its nearby caveats."
        ),
        current_status="summary-context-must-travel-with-label",
    )

    reviewer_checks = [
        "Read the qualification state, review label, and manifest status before treating a discovered model as fit for downstream use.",
        "Check whether workflow role, population support, evidence basis, and claim boundaries are explicit and match the intended context of use.",
        "Check whether missing sections or implicit declarations weaken the intended scientific or regulatory claim.",
    ]
    if not risk_assessment_ready:
        reviewer_checks.append(
            "Treat this model as non-regulatory-ready until stronger evidence and review support are attached."
        )
    if missing_sections:
        reviewer_checks.append(
            "Resolve or explicitly accept the remaining section gaps before relying on static curation summaries."
        )
    if missing_ngra:
        reviewer_checks.append(
            "Do not infer undeclared NGRA boundary details from runtime success or format support."
        )

    return {
        "sectionVersion": "pbpk-curation-misread-risk-summary.v1",
        "sectionTitle": "How discovery or static validation could be misread",
        "requiredReading": True,
        "plainLanguageSummary": (
            "A model can look well-curated in discovery or static validation and still be non-regulatory-ready, "
            "context-limited, or missing important boundary declarations. Read the curation guardrails before reuse."
        ),
        "riskStatements": statements,
        "requiredReviewerChecks": reviewer_checks,
    }


def _curation_summary_transport_risk(
    *,
    risk_assessment_ready: bool,
    ngra_declarations_explicit: bool,
    missing_sections: Sequence[str],
    missing_ngra: Sequence[str],
) -> dict[str, Any]:
    risk_drivers = ["trust-label-can-detach-from-basis"]
    if not risk_assessment_ready:
        risk_drivers.append("non-regulatory-ready-summary-can-be-overread")
    if missing_sections:
        risk_drivers.append("static-section-gaps-can-be-hidden-in-thin-views")
    if missing_ngra:
        risk_drivers.append("implicit-ngra-boundaries-can-be-lost-in-forwarding")
    if not ngra_declarations_explicit and "implicit-ngra-boundaries-can-be-lost-in-forwarding" not in risk_drivers:
        risk_drivers.append("implicit-ngra-boundaries-can-be-lost-in-forwarding")

    risk_level = "high" if len(risk_drivers) > 1 else "medium"
    return {
        "sectionVersion": "pbpk-curation-summary-transport-risk.v1",
        "riskLevel": risk_level,
        "detachedSummaryUnsafe": True,
        "plainLanguageSummary": (
            "Do not let the curation label travel alone. If this summary is forwarded as a card, screenshot, "
            "or short snippet, keep the caveats and boundary statements attached."
        ),
        "lossyViewModes": [
            "catalog-card",
            "screenshot",
            "chat-snippet",
            "forwarded-summary",
            "thin-api-response",
        ],
        "mustTravelWith": [
            "reviewLabel",
            "humanSummary",
            "misreadRiskSummary.plainLanguageSummary",
            "summaryTransportRisk.plainLanguageSummary",
        ],
        "riskDrivers": risk_drivers,
    }


def _curation_export_block_policy(
    *,
    risk_assessment_ready: bool,
    ngra_declarations_explicit: bool,
    missing_sections: Sequence[str],
    missing_ngra: Sequence[str],
) -> dict[str, Any]:
    blocked_view_modes = [
        "catalog-card",
        "screenshot",
        "chat-snippet",
        "forwarded-summary",
        "thin-api-response",
    ]
    required_fields = [
        "reviewLabel",
        "humanSummary",
        "misreadRiskSummary.plainLanguageSummary",
        "summaryTransportRisk.plainLanguageSummary",
    ]
    block_reasons: list[dict[str, Any]] = [
        {
            "code": "bare-review-label-blocked",
            "severity": "high",
            "appliesTo": ["catalog-card", "thin-api-response", "review-badge"],
            "message": (
                "Do not render the trust-bearing review label or manifest state alone. "
                "Adjacent caveats and anti-misread guidance are required."
            ),
            "requiredFields": required_fields,
            "currentStatus": "context-required",
        },
        {
            "code": "detached-summary-blocked",
            "severity": "high",
            "appliesTo": blocked_view_modes,
            "message": (
                "Block lossy discovery or validation summaries when the required caveat fields "
                "cannot travel with the trust-bearing label."
            ),
            "requiredFields": required_fields,
            "currentStatus": "detached-summary-unsafe",
        },
    ]

    if not risk_assessment_ready:
        block_reasons.append(
            {
                "code": "decision-readiness-overclaim-blocked",
                "severity": "high",
                "appliesTo": ["decision-card", "release-highlight", "public-summary"],
                "message": (
                    "Block decision-ready or regulatory-ready framing when the manifest only "
                    "supports static curation or research-use qualification."
                ),
                "currentStatus": "not-risk-assessment-ready",
            }
        )
    if missing_sections:
        block_reasons.append(
            {
                "code": "missing-manifest-sections-blocked",
                "severity": "high",
                "appliesTo": ["approval-badge", "public-summary", "release-highlight"],
                "message": (
                    "Block approval-style presentation when important manifest sections remain "
                    "missing or incomplete."
                ),
                "currentStatus": ", ".join(missing_sections),
            }
        )
    if missing_ngra or not ngra_declarations_explicit:
        block_reasons.append(
            {
                "code": "implicit-ngra-boundaries-blocked",
                "severity": "high",
                "appliesTo": ["decision-card", "workflow-support-badge", "forwarded-summary"],
                "message": (
                    "Block stronger NGRA workflow claims when workflow role, population support, "
                    "evidence basis, or claim boundaries remain implicit."
                ),
                "currentStatus": ", ".join(missing_ngra) if missing_ngra else "implicit-ngra-boundaries",
            }
        )

    return {
        "policyVersion": "pbpk-curation-export-block-policy.v1",
        "defaultAction": "block-lossy-or-decision-leaning-exports",
        "contextualizedRenderOnly": True,
        "blockedViewModes": blocked_view_modes,
        "requiredFields": required_fields,
        "blockReasons": block_reasons,
        "notes": [
            "This policy is descriptive and machine-readable so future analyst-facing clients can refuse unsafe thin views.",
            "Static curation can support discovery and bounded review without implying broader scientific or regulatory authority.",
        ],
    }


def _curation_caution_summary(
    *,
    risk_assessment_ready: bool,
    ngra_declarations_explicit: bool,
    missing_sections: Sequence[str],
    missing_ngra: Sequence[str],
) -> dict[str, Any]:
    cautions: list[dict[str, Any]] = []

    def add_caution(
        code: str,
        caution_type: str,
        severity: str,
        handling: str,
        scope: str,
        source_surface: str,
        message: str,
        *,
        current_status: str | None = None,
    ) -> None:
        payload: dict[str, Any] = {
            "code": code,
            "cautionType": caution_type,
            "severity": severity,
            "handling": handling,
            "scope": scope,
            "sourceSurface": source_surface,
            "message": message,
            "requiresHumanReview": True,
        }
        if current_status:
            payload["currentStatus"] = current_status
        cautions.append(payload)

    add_caution(
        "static-curation-is-not-decision-readiness",
        "decision-overclaim-risk",
        "medium",
        "advisory",
        "model",
        "misreadRiskSummary",
        (
            "Static curation completeness and explicit NGRA declarations do not, by themselves, "
            "establish broad decision readiness or regulatory acceptability."
        ),
        current_status="static-curation-only",
    )
    add_caution(
        "detached-summary-overread",
        "summary-transport-risk",
        "high",
        "blocking",
        "summary-surface",
        "summaryTransportRisk",
        (
            "Thin discovery cards, screenshots, or forwarded snippets can detach the trust-bearing "
            "label from its caveats and make support look stronger than it is."
        ),
        current_status="detached-summary-unsafe",
    )
    if not risk_assessment_ready:
        add_caution(
            "decision-readiness-overclaim",
            "decision-overclaim-risk",
            "high",
            "blocking",
            "workflow-claim",
            "exportBlockPolicy",
            (
                "Decision-ready or regulatory-ready framing should be blocked when static curation "
                "still resolves to research-use or illustrative qualification."
            ),
            current_status="not-risk-assessment-ready",
        )
    if missing_sections:
        add_caution(
            "manifest-section-gaps",
            "evidence-gap",
            "high",
            "blocking",
            "model",
            "validationSummary",
            (
                "Important manifest sections remain missing or incomplete, so approval-style or "
                "broad qualification framing should stay blocked."
            ),
            current_status=", ".join(missing_sections),
        )
    if missing_ngra or not ngra_declarations_explicit:
        add_caution(
            "implicit-ngra-boundaries",
            "implicit-boundary",
            "high",
            "blocking",
            "workflow-boundary",
            "ngraCoverage",
            (
                "Workflow role, population support, evidence basis, or claim boundaries remain "
                "implicit, so stronger NGRA workflow claims should stay blocked."
            ),
            current_status=", ".join(missing_ngra) if missing_ngra else "implicit-ngra-boundaries",
        )

    severity_order = {"low": 0, "medium": 1, "high": 2}
    highest_severity = max(
        (entry["severity"] for entry in cautions),
        key=lambda value: severity_order.get(value, -1),
        default="medium",
    )
    blocking_count = sum(1 for entry in cautions if entry["handling"] == "blocking")
    advisory_count = sum(1 for entry in cautions if entry["handling"] == "advisory")
    return {
        "summaryVersion": "pbpk-curation-caution-summary.v1",
        "highestSeverity": highest_severity,
        "blockingCount": blocking_count,
        "advisoryCount": advisory_count,
        "requiresHumanReview": True,
        "blockingRecommended": blocking_count > 0,
        "cautions": cautions,
    }


def _curation_rendering_guardrails(
    *,
    risk_assessment_ready: bool,
    ngra_declarations_explicit: bool,
    missing_sections: Sequence[str],
    missing_ngra: Sequence[str],
    export_block_policy: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    has_gaps = bool(missing_sections or missing_ngra)
    severity = (
        "warning"
        if has_gaps or not risk_assessment_ready
        else "info"
    )
    if has_gaps:
        inline_warning = (
            "Do not render the review label alone. Show the missing-section and boundary-declaration gaps inline."
        )
    elif not risk_assessment_ready:
        inline_warning = (
            "Do not render the review label as decision-ready or regulatory-ready. Keep the anti-misread guidance adjacent."
        )
    else:
        inline_warning = (
            "Keep the anti-misread guidance adjacent to the review label so within-context qualification is not over-read."
        )

    return {
        "guardVersion": "pbpk-curation-rendering-guardrails.v1",
        "allowBareReviewLabel": False,
        "severity": severity,
        "inlineWarning": inline_warning,
        "actionIfRequiredFieldsMissing": "refuse-rendering",
        "refusalMessage": (
            "Refuse lossy rendering of trust-bearing discovery or validation summaries when the "
            "required caveat fields cannot be shown inline."
        ),
        "requiredFields": [
            "reviewLabel",
            "humanSummary",
            "misreadRiskSummary.plainLanguageSummary",
            "summaryTransportRisk.plainLanguageSummary",
        ],
        "blockedViewModes": list((export_block_policy or {}).get("blockedViewModes") or []),
        "blockReasonCodes": [
            reason.get("code")
            for reason in ((export_block_policy or {}).get("blockReasons") or [])
            if isinstance(reason, Mapping) and reason.get("code")
        ],
        "recommendedOrder": [
            "reviewLabel",
            "humanSummary",
            "summaryTransportRisk.plainLanguageSummary",
            "misreadRiskSummary.sectionTitle",
            "misreadRiskSummary.plainLanguageSummary",
        ],
        "notes": [
            "Qualification or curation labels are trust-bearing and should not be rendered without adjacent caveats.",
            "Manifest completeness and explicit NGRA declarations do not replace human review for the real context of use.",
            "Thin or forwarded views should preserve summary-transport risk guidance so screenshots and snippets do not overstate support.",
        ],
        "requiresInlineMisreadGuidance": True,
        "ngraDeclarationsExplicit": ngra_declarations_explicit,
    }


def build_manifest_curation_summary(manifest: Mapping[str, Any] | None) -> dict[str, Any]:
    manifest_payload = dict(manifest or {})
    qualification_state = dict(manifest_payload.get("qualificationState") or {})
    ngra_coverage = dict(manifest_payload.get("ngraCoverage") or {})
    sections = manifest_payload.get("sections") or {}

    manifest_status = _safe_text(manifest_payload.get("manifestStatus"))
    qualification_state_name = _safe_text(qualification_state.get("state"))
    qualification_label = _safe_text(qualification_state.get("label")) or qualification_state_name
    risk_assessment_ready = bool(qualification_state.get("riskAssessmentReady"))
    missing_sections = sorted(
        section_name
        for section_name, section_payload in sections.items()
        if not bool((section_payload or {}).get("present"))
        or bool((section_payload or {}).get("missingFields"))
    ) if isinstance(sections, Mapping) else []
    missing_ngra = list(ngra_coverage.get("missingDeclarations") or [])
    ngra_declarations_explicit = bool(ngra_coverage.get("allExplicitlyDeclared"))
    export_block_policy = _curation_export_block_policy(
        risk_assessment_ready=risk_assessment_ready,
        ngra_declarations_explicit=ngra_declarations_explicit,
        missing_sections=missing_sections,
        missing_ngra=missing_ngra,
    )

    return {
        "summaryVersion": "pbpk-model-curation-summary.v1",
        "reviewLabel": _curation_review_label(
            qualification_label=qualification_label,
            manifest_status=manifest_status,
            ngra_declarations_explicit=ngra_declarations_explicit,
            risk_assessment_ready=risk_assessment_ready,
        ),
        "manifestStatus": manifest_status,
        "qualificationState": qualification_state_name,
        "riskAssessmentReady": risk_assessment_ready,
        "ngraDeclarationsExplicit": ngra_declarations_explicit,
        "missingSections": missing_sections,
        "missingNgraDeclarations": missing_ngra,
        "humanSummary": _curation_human_summary(
            qualification_label=qualification_label,
            manifest_status=manifest_status,
            risk_assessment_ready=risk_assessment_ready,
            ngra_declarations_explicit=ngra_declarations_explicit,
            missing_sections=missing_sections,
            missing_ngra=missing_ngra,
        ),
        "misreadRiskSummary": _curation_misread_risk_summary(
            qualification_label=qualification_label,
            manifest_status=manifest_status,
            risk_assessment_ready=risk_assessment_ready,
            ngra_declarations_explicit=ngra_declarations_explicit,
            missing_sections=missing_sections,
            missing_ngra=missing_ngra,
        ),
        "summaryTransportRisk": _curation_summary_transport_risk(
            risk_assessment_ready=risk_assessment_ready,
            ngra_declarations_explicit=ngra_declarations_explicit,
            missing_sections=missing_sections,
            missing_ngra=missing_ngra,
        ),
        "cautionSummary": _curation_caution_summary(
            risk_assessment_ready=risk_assessment_ready,
            ngra_declarations_explicit=ngra_declarations_explicit,
            missing_sections=missing_sections,
            missing_ngra=missing_ngra,
        ),
        "exportBlockPolicy": export_block_policy,
        "renderingGuardrails": _curation_rendering_guardrails(
            risk_assessment_ready=risk_assessment_ready,
            ngra_declarations_explicit=ngra_declarations_explicit,
            missing_sections=missing_sections,
            missing_ngra=missing_ngra,
            export_block_policy=export_block_policy,
        ),
        "regulatoryBenchmarkReadiness": derive_manifest_benchmark_readiness(manifest_payload),
    }


def _ngra_coverage_summary(*, scientific_profile: bool, missing: Sequence[str]) -> str:
    if not scientific_profile:
        return (
            "No model-specific scientific profile is declared, so exposure-led workflow role, "
            "population support, evidence basis, and claim boundaries all remain undeclared."
        )
    if not missing:
        return (
            "Explicit NGRA workflow role, population support, evidence basis, and claim-boundary "
            "declarations are present for static curation."
        )
    return (
        "Static manifest is missing explicit NGRA declarations for "
        f"{', '.join(missing)}; runtime exports will fall back to conservative not-declared or "
        "human-review-only semantics until the model profile declares them."
    )


def _build_ngra_coverage(
    declarations: Mapping[str, str | None],
    *,
    scientific_profile: bool,
    population_scope_hints: Sequence[str] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    issues: list[dict[str, Any]] = []
    coverage: dict[str, Any] = {}
    missing: list[str] = []
    hint_list = list(population_scope_hints or [])

    for canonical_name, declared_alias in declarations.items():
        declared = declared_alias is not None
        if declared:
            item: dict[str, Any] = {
                "declared": True,
                "declaredField": f"profile.{declared_alias}",
                "runtimeFallback": _NGRA_RUNTIME_FALLBACKS[canonical_name],
                "summary": f"Declared via profile.{declared_alias}.",
            }
        else:
            item = {
                "declared": False,
                "declaredField": None,
                "runtimeFallback": _NGRA_RUNTIME_FALLBACKS[canonical_name],
                "summary": _NGRA_DECLARATION_MESSAGES[canonical_name],
            }
            missing.append(canonical_name)
            if scientific_profile:
                issues.append(
                    _issue(
                        _NGRA_ISSUE_CODES[canonical_name],
                        _NGRA_DECLARATION_MESSAGES[canonical_name],
                        field=f"profile.{_NGRA_DECLARATION_FIELDS[canonical_name][0]}",
                        severity="warning",
                    )
                )
        if canonical_name == "populationSupport" and hint_list:
            item["scopeHintFields"] = hint_list
        coverage[canonical_name] = item

    coverage["declaredCount"] = sum(
        1 for canonical_name in _NGRA_DECLARATION_FIELDS if coverage[canonical_name]["declared"]
    )
    coverage["missingCount"] = len(missing)
    coverage["allExplicitlyDeclared"] = len(missing) == 0
    coverage["missingDeclarations"] = missing
    coverage["summary"] = _ngra_coverage_summary(
        scientific_profile=scientific_profile,
        missing=missing,
    )
    return coverage, issues


def _performance_section_dataset_records(section: Mapping[str, Any] | None) -> Any:
    if not isinstance(section, Mapping):
        return None
    return (
        section.get("datasetRecords")
        or section.get("records")
        or section.get("benchmarkDatasets")
        or section.get("benchmarkRecords")
    )


def _performance_section_acceptance_criteria(section: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(section, Mapping):
        return []
    return _normalize_text_values(
        section.get("acceptanceCriteria")
        or section.get("acceptanceCriterion")
        or section.get("criteria")
    )


def _performance_profile_supplement_coverage(
    supplement: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    if not isinstance(supplement, Mapping):
        return None

    goodness = supplement.get("goodnessOfFit")
    predictive = supplement.get("predictiveChecks")
    evaluation = supplement.get("evaluationData")

    acceptance_values = []
    acceptance_values.extend(_normalize_text_values(supplement.get("acceptanceCriteria")))
    acceptance_values.extend(_performance_section_acceptance_criteria(goodness if isinstance(goodness, Mapping) else None))
    acceptance_values.extend(_performance_section_acceptance_criteria(predictive if isinstance(predictive, Mapping) else None))
    acceptance_values.extend(_performance_section_acceptance_criteria(evaluation if isinstance(evaluation, Mapping) else None))

    deduped_acceptance: list[str] = []
    for item in acceptance_values:
        if item not in deduped_acceptance:
            deduped_acceptance.append(item)

    return {
        "goodnessOfFitDatasetRecordCount": _record_entry_count(_performance_section_dataset_records(goodness if isinstance(goodness, Mapping) else None)),
        "predictiveDatasetRecordCount": _record_entry_count(_performance_section_dataset_records(predictive if isinstance(predictive, Mapping) else None)),
        "evaluationDatasetRecordCount": _record_entry_count(_performance_section_dataset_records(evaluation if isinstance(evaluation, Mapping) else None)),
        "acceptanceCriterionCount": len(deduped_acceptance),
        "hasExplicitAcceptanceCriteria": bool(deduped_acceptance),
    }


def _performance_traceability_reference_sets(
    performance: Mapping[str, Any] | None,
) -> dict[str, list[str]]:
    if not isinstance(performance, Mapping):
        return {"datasets": [], "targetOutputs": [], "acceptanceCriteria": []}

    goodness = performance.get("goodnessOfFit") if isinstance(performance.get("goodnessOfFit"), Mapping) else None
    predictive = performance.get("predictiveChecks") if isinstance(performance.get("predictiveChecks"), Mapping) else None
    evaluation = performance.get("evaluationData") if isinstance(performance.get("evaluationData"), Mapping) else None

    datasets = _normalize_text_values(
        [
            _performance_section_dataset_records(goodness),
            _performance_section_dataset_records(predictive),
            _performance_section_dataset_records(evaluation),
            goodness.get("datasets") if isinstance(goodness, Mapping) else None,
            goodness.get("datasetIds") if isinstance(goodness, Mapping) else None,
            goodness.get("datasetNames") if isinstance(goodness, Mapping) else None,
            predictive.get("datasets") if isinstance(predictive, Mapping) else None,
            predictive.get("datasetIds") if isinstance(predictive, Mapping) else None,
            predictive.get("datasetNames") if isinstance(predictive, Mapping) else None,
            evaluation.get("datasets") if isinstance(evaluation, Mapping) else None,
            evaluation.get("datasetIds") if isinstance(evaluation, Mapping) else None,
            evaluation.get("datasetNames") if isinstance(evaluation, Mapping) else None,
        ]
    )

    for section in (goodness, predictive, evaluation):
        records = _performance_section_dataset_records(section if isinstance(section, Mapping) else None)
        if isinstance(records, Sequence) and not isinstance(records, (str, bytes, bytearray)):
            for entry in records:
                if isinstance(entry, Mapping):
                    datasets.extend(
                        _normalize_text_values(
                            entry.get("dataset")
                            or entry.get("datasetId")
                            or entry.get("datasetName")
                            or entry.get("study")
                            or entry.get("studyId")
                            or entry.get("id")
                        )
                    )
        elif isinstance(records, Mapping):
            datasets.extend(
                _normalize_text_values(
                    records.get("dataset")
                    or records.get("datasetId")
                    or records.get("datasetName")
                    or records.get("study")
                    or records.get("studyId")
                    or records.get("id")
                )
            )

    return {
        "datasets": _normalize_text_values(datasets),
        "targetOutputs": _normalize_text_values(performance.get("targetOutputs")),
        "acceptanceCriteria": _normalize_text_values(
            [
                performance.get("acceptanceCriteria"),
                _performance_section_acceptance_criteria(goodness),
                _performance_section_acceptance_criteria(predictive),
                _performance_section_acceptance_criteria(evaluation),
            ]
        ),
    }


def _section_status(section_name: str, payload: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    issues: list[dict[str, Any]] = []
    required_fields = _REQUIRED_SECTION_FIELDS.get(section_name, ())

    if payload is None:
        issues.append(
            _issue(
                "section_missing",
                f"Section '{section_name}' is not declared in the manifest.",
                field=f"profile.{section_name}",
            )
        )
        return {
            "present": False,
            "declaredFields": [],
            "missingFields": list(required_fields),
            "summary": None,
        }, issues

    if isinstance(payload, Mapping):
        declared_fields = []
        missing_fields = []
        for field in required_fields:
            value = payload.get(field)
            if isinstance(value, Mapping):
                if len(value) > 0:
                    declared_fields.append(field)
                else:
                    missing_fields.append(field)
            elif _safe_text(value):
                declared_fields.append(field)
            else:
                missing_fields.append(field)
        if missing_fields:
            issues.append(
                _issue(
                    "section_incomplete",
                    f"Section '{section_name}' is missing required fields: {', '.join(missing_fields)}.",
                    field=f"profile.{section_name}",
                )
            )
        return {
            "present": True,
            "declaredFields": declared_fields,
            "missingFields": missing_fields,
            "summary": _safe_text(payload.get("summary") or payload.get("status")),
        }, issues

    summary = _safe_text(payload)
    if required_fields:
        issues.append(
            _issue(
                "section_scalar_only",
                f"Section '{section_name}' is declared only as a scalar summary and does not expose the required fields.",
                field=f"profile.{section_name}",
                severity="warning",
            )
        )
    return {
        "present": bool(summary),
        "declaredFields": [],
        "missingFields": list(required_fields),
        "summary": summary,
    }, issues


def _manifest_status(issues: Sequence[Mapping[str, Any]], has_scientific_profile: bool, core_complete: bool) -> str:
    error_count = sum(1 for issue in issues if str(issue.get("severity")) == "error")
    if not has_scientific_profile:
        return "missing"
    if error_count == 0 and core_complete:
        return "valid"
    return "partial"


def derive_qualification_state(
    *,
    scientific_profile: bool,
    profile_source: str | None,
    qualification_level: str | None,
    core_sections_complete: bool,
    evidence_sections_complete: bool,
) -> dict[str, Any]:
    token = normalize_token(qualification_level)
    source_token = normalize_token(profile_source)

    if not scientific_profile or source_token in {None, "bridge-default"}:
      state = "exploratory"
      label = "Exploratory"
      summary = "Runtime format is supported, but no model-specific scientific manifest is declared."
      risk_ready = False
    elif token in _EXAMPLE_QUALIFICATIONS:
      state = "illustrative-example"
      label = "Illustrative example"
      summary = "Manifest identifies this model as an example or integration fixture."
      risk_ready = False
    elif token in _RESEARCH_QUALIFICATIONS:
      state = "research-use"
      label = "Research use"
      summary = "Manifest supports research-oriented use within declared guardrails, not regulatory qualification."
      risk_ready = False
    elif token in _REGULATORY_QUALIFICATIONS:
      if core_sections_complete and evidence_sections_complete:
          state = "qualified-within-context"
          label = "Qualified within context"
          summary = "Manifest declares a qualification-oriented context with the key dossier sections in place."
          risk_ready = True
      else:
          state = "regulatory-candidate"
          label = "Regulatory candidate"
          summary = "Manifest targets qualification-oriented use, but dossier completeness is still partial."
          risk_ready = False
    else:
      if core_sections_complete:
          state = "regulatory-candidate"
          label = "Regulatory candidate"
          summary = "Manifest is structured enough to be developed toward qualification, but the declared state is incomplete."
      else:
          state = "research-use"
          label = "Research use"
          summary = "Manifest is partially structured but not complete enough for qualification-oriented claims."
      risk_ready = False

    return {
        "state": state,
        "label": label,
        "summary": summary,
        "qualificationLevel": qualification_level,
        "riskAssessmentReady": risk_ready,
        "coreSectionsComplete": core_sections_complete,
        "evidenceSectionsComplete": evidence_sections_complete,
    }


def _validate_profile_manifest(
    profile: Mapping[str, Any],
    *,
    backend: str,
    profile_source: str | None,
    sidecar_path: str | None = None,
) -> dict[str, Any]:
    sections: dict[str, Any] = {}
    issues: list[dict[str, Any]] = []

    for section_name in _REQUIRED_SECTION_FIELDS:
        section_status, section_issues = _section_status(section_name, profile.get(section_name))
        sections[section_name] = section_status
        issues.extend(section_issues)

    qualification_level = None
    applicability = profile.get("applicabilityDomain")
    if isinstance(applicability, Mapping):
        qualification_level = _safe_text(applicability.get("qualificationLevel"))

    scientific_profile = profile_source not in {None, "bridge-default"}
    core_sections_complete = all(
        bool(section["present"]) and not section["missingFields"]
        for section in sections.values()
    )
    evidence_sections_complete = all(
        not sections[name]["missingFields"]
        for name in (
            "modelPerformance",
            "parameterProvenance",
            "uncertainty",
            "implementationVerification",
            "platformQualification",
            "peerReview",
        )
    )

    if sidecar_path:
        metadata = {"sidecarPath": sidecar_path}
    else:
        metadata = {}

    ngra_coverage, ngra_issues = _build_ngra_coverage(
        {
            canonical_name: _declared_profile_alias(profile, field_names)
            for canonical_name, field_names in _NGRA_DECLARATION_FIELDS.items()
        },
        scientific_profile=scientific_profile,
        population_scope_hints=_population_scope_hint_fields(
            applicability if isinstance(applicability, Mapping) else None
        ),
    )
    issues.extend(ngra_issues)

    qualification_state = derive_qualification_state(
        scientific_profile=scientific_profile,
        profile_source=profile_source,
        qualification_level=qualification_level,
        core_sections_complete=core_sections_complete,
        evidence_sections_complete=evidence_sections_complete,
    )

    return {
        "validationMode": "static-manifest-inspection",
        "backend": backend,
        "scientificProfile": scientific_profile,
        "profileSource": profile_source,
        "qualificationLevel": qualification_level,
        "manifestStatus": _manifest_status(issues, scientific_profile, core_sections_complete),
        "qualificationState": qualification_state,
        "sections": sections,
        "ngraCoverage": ngra_coverage,
        "issues": issues,
        **metadata,
    }


def _load_sidecar_profile(file_path: Path) -> tuple[dict[str, Any] | None, str | None, list[dict[str, Any]]]:
    issues: list[dict[str, Any]] = []
    for candidate in ospsuite_profile_sidecar_candidates(file_path):
        if not candidate.exists():
            continue
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                _issue(
                    "sidecar_parse_error",
                    f"Failed to parse sidecar JSON: {exc}",
                    field=str(candidate),
                )
            )
            return None, str(candidate), issues

        profile_payload = payload.get("profile", payload)
        if not isinstance(profile_payload, Mapping):
            issues.append(
                _issue(
                    "sidecar_profile_missing",
                    "Sidecar JSON must provide a top-level 'profile' object or itself be a profile object.",
                    field=str(candidate),
                )
            )
            return None, str(candidate), issues
        return dict(profile_payload), str(candidate), issues

    issues.append(
        _issue(
            "sidecar_missing",
            "No profile sidecar was found for this OSPSuite transfer file.",
            field=str(file_path),
        )
    )
    return None, None, issues


def _extract_performance_evidence_rows(payload: Any) -> list[Any] | None:
    if isinstance(payload, Sequence) and not isinstance(payload, (str, bytes, bytearray)):
        if payload and not isinstance(payload, Mapping):
            return list(payload)
    if not isinstance(payload, Mapping):
        return None

    candidates = (
        payload.get("rows"),
        payload.get("performanceEvidence", {}).get("rows") if isinstance(payload.get("performanceEvidence"), Mapping) else None,
        payload.get("performanceEvidence"),
        payload.get("evidence"),
    )
    for candidate in candidates:
        if isinstance(candidate, Sequence) and not isinstance(candidate, (str, bytes, bytearray)):
            return list(candidate)
    return None


def _extract_performance_evidence_metadata(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, Mapping):
        return None
    metadata = payload.get("metadata")
    if metadata is None and isinstance(payload.get("performanceEvidence"), Mapping):
        metadata = payload["performanceEvidence"].get("metadata")
    if not isinstance(metadata, Mapping):
        return None
    return dict(metadata)


def _extract_performance_evidence_profile_supplement(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, Mapping):
        return None
    supplement = payload.get("profileSupplement")
    if supplement is None and isinstance(payload.get("performanceEvidence"), Mapping):
        performance_payload = payload["performanceEvidence"]
        supplement = performance_payload.get("profileSupplement") or performance_payload.get("modelPerformance")
    if supplement is None and isinstance(payload.get("modelPerformance"), Mapping):
        supplement = payload.get("modelPerformance")
    if not isinstance(supplement, Mapping):
        return None
    return dict(supplement)


def _extract_uncertainty_evidence_rows(payload: Any) -> list[Any] | None:
    if isinstance(payload, Sequence) and not isinstance(payload, (str, bytes, bytearray)):
        if payload and not isinstance(payload, Mapping):
            return list(payload)
    if not isinstance(payload, Mapping):
        return None

    candidates = (
        payload.get("rows"),
        payload.get("uncertaintyEvidence", {}).get("rows") if isinstance(payload.get("uncertaintyEvidence"), Mapping) else None,
        payload.get("uncertaintyEvidence"),
        payload.get("evidence"),
    )
    for candidate in candidates:
        if isinstance(candidate, Sequence) and not isinstance(candidate, (str, bytes, bytearray)):
            return list(candidate)
    return None


def _extract_uncertainty_evidence_metadata(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, Mapping):
        return None
    metadata = payload.get("metadata")
    if metadata is None and isinstance(payload.get("uncertaintyEvidence"), Mapping):
        metadata = payload["uncertaintyEvidence"].get("metadata")
    if not isinstance(metadata, Mapping):
        return None
    return dict(metadata)


def _extract_parameter_table_rows(payload: Any) -> list[Any] | None:
    if isinstance(payload, Sequence) and not isinstance(payload, (str, bytes, bytearray)):
        if payload and not isinstance(payload, Mapping):
            return list(payload)
    if not isinstance(payload, Mapping):
        return None

    candidates = (
        payload.get("rows"),
        payload.get("parameterTable", {}).get("rows") if isinstance(payload.get("parameterTable"), Mapping) else None,
        payload.get("parameters"),
    )
    for candidate in candidates:
        if isinstance(candidate, Sequence) and not isinstance(candidate, (str, bytes, bytearray)):
            return list(candidate)
    return None


def _extract_parameter_table_metadata(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, Mapping):
        return None
    metadata = payload.get("metadata")
    if metadata is None and isinstance(payload.get("parameterTable"), Mapping):
        metadata = payload["parameterTable"].get("metadata")
    if not isinstance(metadata, Mapping):
        return None
    return dict(metadata)


def _validate_performance_evidence_rows(rows: Sequence[Any], *, field_prefix: str) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for index, entry in enumerate(rows, start=1):
        if not isinstance(entry, Mapping):
            continue
        evidence_class = _safe_text(
            entry.get("evidenceClass")
            or entry.get("evidence_class")
            or entry.get("kind")
            or entry.get("type")
        ) or "other"
        row_id = _safe_text(entry.get("id")) or f"row-{index:03d}"
        row_field_prefix = f"{field_prefix}[{index}]"

        def add_issue(code: str, message: str, field: str) -> None:
            issues.append(
                _issue(
                    code,
                    message,
                    field=field,
                    severity="warning",
                )
            )

        acceptance = _safe_text(entry.get("acceptanceCriterion") or entry.get("acceptance_criterion"))
        dataset = _safe_text(entry.get("dataset") or entry.get("datasetId") or entry.get("study"))
        qualification_basis = _safe_text(entry.get("qualificationBasis") or entry.get("qualification_basis"))

        if evidence_class == "runtime-smoke" and not acceptance:
            add_issue(
                "performance_row_acceptance_missing",
                f"Runtime smoke row '{row_id}' should declare an acceptanceCriterion.",
                f"{row_field_prefix}.acceptanceCriterion",
            )
        if evidence_class == "observed-vs-predicted":
            if entry.get("observedValue") is None:
                add_issue(
                    "performance_row_observed_missing",
                    f"Observed-versus-predicted row '{row_id}' should include observedValue.",
                    f"{row_field_prefix}.observedValue",
                )
            if entry.get("predictedValue") is None:
                add_issue(
                    "performance_row_predicted_missing",
                    f"Observed-versus-predicted row '{row_id}' should include predictedValue.",
                    f"{row_field_prefix}.predictedValue",
                )
            if not dataset:
                add_issue(
                    "performance_row_dataset_missing",
                    f"Observed-versus-predicted row '{row_id}' should identify the benchmark dataset or study.",
                    f"{row_field_prefix}.dataset",
                )
            if not acceptance:
                add_issue(
                    "performance_row_acceptance_missing",
                    f"Observed-versus-predicted row '{row_id}' should declare the comparison acceptanceCriterion.",
                    f"{row_field_prefix}.acceptanceCriterion",
                )
        if evidence_class == "predictive-dataset":
            if not dataset:
                add_issue(
                    "performance_row_dataset_missing",
                    f"Predictive-dataset row '{row_id}' should identify the dataset or benchmark package.",
                    f"{row_field_prefix}.dataset",
                )
            if not acceptance:
                add_issue(
                    "performance_row_acceptance_missing",
                    f"Predictive-dataset row '{row_id}' should declare the dataset-level acceptanceCriterion.",
                    f"{row_field_prefix}.acceptanceCriterion",
                )
        if evidence_class == "external-qualification":
            if not dataset and not qualification_basis:
                add_issue(
                    "performance_row_external_basis_missing",
                    f"External-qualification row '{row_id}' should declare a dataset or qualificationBasis.",
                    row_field_prefix,
                )
            if not acceptance:
                add_issue(
                    "performance_row_acceptance_missing",
                    f"External-qualification row '{row_id}' should declare the qualification acceptanceCriterion.",
                    f"{row_field_prefix}.acceptanceCriterion",
                )
    return issues


def _validate_performance_traceability_consistency(
    rows: Sequence[Any],
    *,
    performance: Mapping[str, Any] | None,
    field_prefix: str,
) -> list[dict[str, Any]]:
    references = _performance_traceability_reference_sets(performance)
    issues: list[dict[str, Any]] = []
    if not any(references.values()):
        return issues

    for index, entry in enumerate(rows, start=1):
        if not isinstance(entry, Mapping):
            continue
        evidence_class = _safe_text(
            entry.get("evidenceClass")
            or entry.get("evidence_class")
            or entry.get("kind")
            or entry.get("type")
        ) or "other"
        row_id = _safe_text(entry.get("id")) or f"row-{index:03d}"
        row_field_prefix = f"{field_prefix}[{index}]"
        dataset = _safe_text(entry.get("dataset") or entry.get("datasetId") or entry.get("study"))
        target_output = _safe_text(entry.get("targetOutput") or entry.get("target_output") or entry.get("output"))
        acceptance = _safe_text(entry.get("acceptanceCriterion") or entry.get("acceptance_criterion"))
        dataset_relevant = evidence_class in {"observed-vs-predicted", "predictive-dataset", "external-qualification"}
        target_relevant = evidence_class in {"observed-vs-predicted", "predictive-dataset"}

        if dataset_relevant and dataset and references["datasets"] and dataset not in references["datasets"]:
            issues.append(
                _issue(
                    "performance_row_dataset_traceability_missing",
                    f"Performance evidence row '{row_id}' names dataset '{dataset}', but that dataset is not declared in the current performance traceability.",
                    field=f"{row_field_prefix}.dataset",
                    severity="warning",
                )
            )
        if target_relevant and target_output and references["targetOutputs"] and target_output not in references["targetOutputs"]:
            issues.append(
                _issue(
                    "performance_row_target_output_traceability_missing",
                    f"Performance evidence row '{row_id}' names targetOutput '{target_output}', but that output is not declared in the current performance traceability.",
                    field=f"{row_field_prefix}.targetOutput",
                    severity="warning",
                )
            )
        if dataset_relevant and acceptance and references["acceptanceCriteria"] and acceptance not in references["acceptanceCriteria"]:
            issues.append(
                _issue(
                    "performance_row_acceptance_traceability_missing",
                    f"Performance evidence row '{row_id}' declares acceptanceCriterion '{acceptance}', but that criterion is not declared in the current performance traceability.",
                    field=f"{row_field_prefix}.acceptanceCriterion",
                    severity="warning",
                )
            )
    return issues


def _validate_performance_evidence_metadata(
    metadata: Mapping[str, Any] | None,
    *,
    field_prefix: str,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    metadata_dict = dict(metadata or {})
    if not _safe_text(metadata_dict.get("bundleVersion")):
        issues.append(
            _issue(
                "performance_bundle_version_missing",
                "Performance evidence bundle metadata should declare bundleVersion.",
                field=f"{field_prefix}.bundleVersion",
                severity="warning",
            )
        )
    if not _safe_text(metadata_dict.get("summary")):
        issues.append(
            _issue(
                "performance_bundle_summary_missing",
                "Performance evidence bundle metadata should declare summary.",
                field=f"{field_prefix}.summary",
                severity="warning",
            )
        )
    return issues


def _validate_uncertainty_evidence_rows(rows: Sequence[Any], *, field_prefix: str) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for index, entry in enumerate(rows, start=1):
        if not isinstance(entry, Mapping):
            continue
        kind = _safe_text(entry.get("kind") or entry.get("type")) or "unspecified"
        row_id = _safe_text(entry.get("id")) or f"row-{index:03d}"
        row_field_prefix = f"{field_prefix}[{index}]"

        def add_issue(code: str, message: str, field: str) -> None:
            issues.append(
                _issue(
                    code,
                    message,
                    field=field,
                    severity="warning",
                )
            )

        summary = _safe_text(entry.get("summary") or entry.get("description"))
        method = _safe_text(entry.get("method"))
        metric = _safe_text(entry.get("metric") or entry.get("metricName") or entry.get("metric_name"))
        target_output = _safe_text(entry.get("targetOutput") or entry.get("target_output") or entry.get("output"))
        varied_parameters = entry.get("variedParameters") or entry.get("parameters")
        has_varied_parameters = isinstance(varied_parameters, Sequence) and not isinstance(varied_parameters, (str, bytes, bytearray)) and len(varied_parameters) > 0
        has_quantitative_signal = any(
            _safe_float(entry.get(field)) is not None
            for field in ("value", "lowerBound", "upperBound", "mean", "sd")
        )

        if kind == "variability-approach":
            if not summary and not method:
                add_issue(
                    "uncertainty_row_summary_missing",
                    f"Variability-approach row '{row_id}' should declare a method or summary.",
                    row_field_prefix,
                )
        elif kind in {"variability-propagation", "sensitivity-analysis"}:
            if not summary and not method:
                add_issue(
                    "uncertainty_row_summary_missing",
                    f"Uncertainty row '{row_id}' should declare a method or summary.",
                    row_field_prefix,
                )
            if not metric and not target_output and not has_varied_parameters:
                add_issue(
                    "uncertainty_row_scope_missing",
                    f"Uncertainty row '{row_id}' should declare a metric, targetOutput, or variedParameters.",
                    row_field_prefix,
                )
            if kind == "variability-propagation" and not has_quantitative_signal:
                add_issue(
                    "uncertainty_row_quantitative_signal_missing",
                    f"Variability-propagation row '{row_id}' should include quantitative outputs such as bounds, summary statistics, or values.",
                    row_field_prefix,
                )
        elif kind == "residual-uncertainty":
            if not summary:
                add_issue(
                    "uncertainty_row_summary_missing",
                    f"Residual-uncertainty row '{row_id}' should declare a summary.",
                    f"{row_field_prefix}.summary",
                )
    return issues


def _validate_uncertainty_evidence_metadata(
    metadata: Mapping[str, Any] | None,
    *,
    field_prefix: str,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    metadata_dict = dict(metadata or {})
    if not _safe_text(metadata_dict.get("bundleVersion")):
        issues.append(
            _issue(
                "uncertainty_bundle_version_missing",
                "Uncertainty evidence bundle metadata should declare bundleVersion.",
                field=f"{field_prefix}.bundleVersion",
                severity="warning",
            )
        )
    if not _safe_text(metadata_dict.get("summary")):
        issues.append(
            _issue(
                "uncertainty_bundle_summary_missing",
                "Uncertainty evidence bundle metadata should declare summary.",
                field=f"{field_prefix}.summary",
                severity="warning",
            )
        )
    return issues


def _validate_parameter_table_rows(rows: Sequence[Any], *, field_prefix: str) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for index, entry in enumerate(rows, start=1):
        if not isinstance(entry, Mapping):
            continue
        row_id = _safe_text(entry.get("id") or entry.get("path")) or f"row-{index:03d}"
        row_field_prefix = f"{field_prefix}[{index}]"

        def add_issue(code: str, message: str, field: str) -> None:
            issues.append(
                _issue(
                    code,
                    message,
                    field=field,
                    severity="warning",
                )
            )

        path = _safe_text(entry.get("path"))
        if not path:
            add_issue(
                "parameter_row_path_missing",
                f"Parameter-table row '{row_id}' should declare a path.",
                f"{row_field_prefix}.path",
            )
            continue

        source = _safe_text(entry.get("source"))
        source_citation = _safe_text(entry.get("sourceCitation") or entry.get("source_citation"))
        source_table = _safe_text(entry.get("sourceTable") or entry.get("source_table"))
        source_type = _safe_text(entry.get("sourceType") or entry.get("source_type"))
        evidence_type = _safe_text(entry.get("evidenceType") or entry.get("evidence_type"))
        rationale = _safe_text(entry.get("rationale") or entry.get("motivation"))
        experimental_conditions = entry.get("experimentalConditions") or entry.get("testConditions") or entry.get("studyConditions")
        has_conditions = _safe_text(experimental_conditions) is not None or (
            isinstance(experimental_conditions, Sequence) and not isinstance(experimental_conditions, (str, bytes, bytearray)) and len(experimental_conditions) > 0
        )

        has_provenance = any(value is not None for value in (
            source,
            source_citation,
            source_table,
            source_type,
            evidence_type,
            rationale,
            _safe_text(entry.get("distribution") or entry.get("distributionType") or entry.get("distribution_type")),
            entry.get("mean"),
            entry.get("sd"),
            entry.get("standardDeviation"),
            entry.get("lowerBound"),
            entry.get("upperBound"),
            experimental_conditions,
        ))

        if has_provenance and not any(value is not None for value in (source, source_citation, source_table)):
            add_issue(
                "parameter_row_source_missing",
                f"Parameter row '{row_id}' declares provenance metadata but does not identify a source, citation, or source table.",
                row_field_prefix,
            )

        distribution = _safe_text(entry.get("distribution") or entry.get("distributionType") or entry.get("distribution_type"))
        if distribution and all(entry.get(field) is None for field in ("mean", "sd", "standardDeviation", "lowerBound", "upperBound")):
            add_issue(
                "parameter_row_distribution_details_missing",
                f"Parameter row '{row_id}' declares a distribution but does not provide supporting statistics or bounds.",
                f"{row_field_prefix}.distribution",
            )

        source_type_token = normalize_token(source_type)
        evidence_type_token = normalize_token(evidence_type)
        experimental_source = (
            bool(source_type_token and re.search(r"in-vitro|in-vivo|in-silico|experimental|study|guideline", source_type_token))
            or bool(evidence_type_token and re.search(r"experimental|study|literature", evidence_type_token))
        )
        if experimental_source and not has_conditions and rationale is None:
            add_issue(
                "parameter_row_conditions_missing",
                f"Parameter row '{row_id}' looks experimental or study-derived but does not declare study conditions or rationale.",
                row_field_prefix,
            )

    return issues


def _validate_parameter_table_metadata(
    metadata: Mapping[str, Any] | None,
    *,
    field_prefix: str,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    metadata_dict = dict(metadata or {})
    if not _safe_text(metadata_dict.get("bundleVersion")):
        issues.append(
            _issue(
                "parameter_table_bundle_version_missing",
                "Parameter-table bundle metadata should declare bundleVersion.",
                field=f"{field_prefix}.bundleVersion",
                severity="warning",
            )
        )
    if not _safe_text(metadata_dict.get("summary")):
        issues.append(
            _issue(
                "parameter_table_bundle_summary_missing",
                "Parameter-table bundle metadata should declare summary.",
                field=f"{field_prefix}.summary",
                severity="warning",
            )
        )
    return issues


def _load_performance_evidence_sidecar(
    file_path: Path,
) -> tuple[list[Any], dict[str, Any] | None, dict[str, Any] | None, str | None, list[dict[str, Any]]]:
    issues: list[dict[str, Any]] = []
    for candidate in performance_evidence_sidecar_candidates(file_path):
        if not candidate.exists():
            continue
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                _issue(
                    "performance_sidecar_parse_error",
                    f"Failed to parse performance evidence sidecar JSON: {exc}",
                    field=str(candidate),
                    severity="warning",
                )
            )
            return [], None, None, str(candidate), issues

        rows = _extract_performance_evidence_rows(payload)
        metadata = _extract_performance_evidence_metadata(payload)
        profile_supplement = _extract_performance_evidence_profile_supplement(payload)
        if rows is None:
            issues.append(
                _issue(
                    "performance_sidecar_rows_missing",
                    "Performance evidence sidecar must provide 'rows', 'performanceEvidence.rows', or a top-level row array.",
                    field=str(candidate),
                    severity="warning",
                )
            )
            return [], metadata, profile_supplement, str(candidate), issues
        issues.extend(_validate_performance_evidence_metadata(metadata, field_prefix=f"{candidate}:metadata"))
        issues.extend(_validate_performance_evidence_rows(rows, field_prefix=f"{candidate}:rows"))
        issues.extend(
            _validate_performance_traceability_consistency(
                rows,
                performance=profile_supplement,
                field_prefix=f"{candidate}:rows",
            )
        )
        return rows, metadata, profile_supplement, str(candidate), issues

    return [], None, None, None, issues


def _load_uncertainty_evidence_sidecar(
    file_path: Path,
) -> tuple[list[Any], dict[str, Any] | None, str | None, list[dict[str, Any]]]:
    issues: list[dict[str, Any]] = []
    for candidate in uncertainty_evidence_sidecar_candidates(file_path):
        if not candidate.exists():
            continue
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                _issue(
                    "uncertainty_sidecar_parse_error",
                    f"Failed to parse uncertainty evidence sidecar JSON: {exc}",
                    field=str(candidate),
                    severity="warning",
                )
            )
            return [], None, str(candidate), issues

        rows = _extract_uncertainty_evidence_rows(payload)
        metadata = _extract_uncertainty_evidence_metadata(payload)
        if rows is None:
            issues.append(
                _issue(
                    "uncertainty_sidecar_rows_missing",
                    "Uncertainty evidence sidecar must provide 'rows', 'uncertaintyEvidence.rows', or a top-level row array.",
                    field=str(candidate),
                    severity="warning",
                )
            )
            return [], metadata, str(candidate), issues
        issues.extend(_validate_uncertainty_evidence_metadata(metadata, field_prefix=f"{candidate}:metadata"))
        issues.extend(_validate_uncertainty_evidence_rows(rows, field_prefix=f"{candidate}:rows"))
        return rows, metadata, str(candidate), issues

    return [], None, None, issues


def _load_parameter_table_sidecar(
    file_path: Path,
) -> tuple[list[Any], dict[str, Any] | None, str | None, list[dict[str, Any]]]:
    issues: list[dict[str, Any]] = []
    for candidate in parameter_table_sidecar_candidates(file_path):
        if not candidate.exists():
            continue
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                _issue(
                    "parameter_table_sidecar_parse_error",
                    f"Failed to parse parameter-table sidecar JSON: {exc}",
                    field=str(candidate),
                    severity="warning",
                )
            )
            return [], None, str(candidate), issues

        rows = _extract_parameter_table_rows(payload)
        metadata = _extract_parameter_table_metadata(payload)
        if rows is None:
            issues.append(
                _issue(
                    "parameter_table_sidecar_rows_missing",
                    "Parameter-table sidecar must provide 'rows', 'parameterTable.rows', or a top-level row array.",
                    field=str(candidate),
                    severity="warning",
                )
            )
            return [], metadata, str(candidate), issues

        issues.extend(_validate_parameter_table_metadata(metadata, field_prefix=f"{candidate}:metadata"))
        issues.extend(_validate_parameter_table_rows(rows, field_prefix=f"{candidate}:rows"))
        return list(rows), metadata, str(candidate), issues

    return [], None, None, issues


def _extract_assignment(text: str, field_name: str) -> str | None:
    pattern = re.compile(rf"\b{re.escape(field_name)}\s*=\s*['\"]([^'\"]+)['\"]")
    match = pattern.search(text)
    if not match:
        return None
    candidate = match.group(1).strip()
    return candidate or None


def _validate_r_model(file_path: Path) -> dict[str, Any]:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    parameter_table_sidecar_rows, parameter_table_sidecar_metadata, parameter_table_sidecar_path, parameter_table_sidecar_issues = _load_parameter_table_sidecar(file_path)
    (
        performance_sidecar_rows,
        performance_sidecar_metadata,
        performance_sidecar_profile_supplement,
        performance_sidecar_path,
        performance_sidecar_issues,
    ) = _load_performance_evidence_sidecar(file_path)
    uncertainty_sidecar_rows, uncertainty_sidecar_metadata, uncertainty_sidecar_path, uncertainty_sidecar_issues = _load_uncertainty_evidence_sidecar(file_path)
    hooks = {
        name: bool(pattern.search(text))
        for name, pattern in _R_HOOK_PATTERNS.items()
    }
    hooks["parameterTableSidecar"] = parameter_table_sidecar_path is not None
    hooks["performanceEvidenceSidecar"] = performance_sidecar_path is not None
    hooks["uncertaintyEvidenceSidecar"] = uncertainty_sidecar_path is not None
    ngra_coverage, ngra_issues = _build_ngra_coverage(
        {
            canonical_name: _declared_text_alias(text, field_names)
            for canonical_name, field_names in _NGRA_DECLARATION_FIELDS.items()
        },
        scientific_profile=hooks["modelProfile"],
    )
    sections = {
        name: {
            "present": bool(pattern.search(text)),
            "declaredFields": [],
            "missingFields": [],
            "summary": None,
        }
        for name, pattern in _R_SECTION_PATTERNS.items()
    }

    issues: list[dict[str, Any]] = []
    issues.extend(parameter_table_sidecar_issues)
    issues.extend(performance_sidecar_issues)
    issues.extend(uncertainty_sidecar_issues)
    issues.extend(ngra_issues)
    if not hooks["modelProfile"]:
        issues.append(
            _issue(
                "profile_hook_missing",
                "R model does not declare pbpk_model_profile(...).",
                field=str(file_path),
            )
        )
    if not hooks["validationHook"]:
        issues.append(
            _issue(
                "validation_hook_missing",
                "R model does not declare pbpk_validate_request(...).",
                field=str(file_path),
                severity="warning",
            )
        )
    if not hooks["parameterTable"] and not hooks["parameterTableSidecar"]:
        issues.append(
            _issue(
                "parameter_table_hook_missing",
                "R model does not declare pbpk_parameter_table(...) and no parameter-table sidecar was found.",
                field=str(file_path),
                severity="warning",
            )
        )
    if not hooks["performanceEvidence"] and not hooks["performanceEvidenceSidecar"]:
        issues.append(
            _issue(
                "performance_evidence_hook_missing",
                "R model does not declare pbpk_performance_evidence(...) and no performance evidence sidecar was found.",
                field=str(file_path),
                severity="warning",
            )
        )
    if not hooks["uncertaintyEvidence"] and not hooks["uncertaintyEvidenceSidecar"]:
        issues.append(
            _issue(
                "uncertainty_evidence_hook_missing",
                "R model does not declare pbpk_uncertainty_evidence(...) and no uncertainty evidence sidecar was found.",
                field=str(file_path),
                severity="warning",
            )
        )
    if not hooks["verificationEvidence"]:
        issues.append(
            _issue(
                "verification_evidence_hook_missing",
                "R model does not declare pbpk_verification_evidence(...).",
                field=str(file_path),
                severity="warning",
            )
        )
    if not hooks["platformQualificationEvidence"]:
        issues.append(
            _issue(
                "platform_qualification_evidence_hook_missing",
                "R model does not declare pbpk_platform_qualification_evidence(...).",
                field=str(file_path),
                severity="warning",
            )
        )

    for name, status in sections.items():
        if not status["present"]:
            issues.append(
                _issue(
                    "profile_section_not_detected",
                    f"Could not detect profile section '{name}' in the R module text.",
                    field=f"{file_path}:{name}",
                    severity="warning",
                )
            )

    qualification_level = _extract_assignment(text, "qualificationLevel")
    scientific_profile = hooks["modelProfile"]
    profile_source = "module-hook-detected" if scientific_profile else "bridge-default"
    core_sections_complete = scientific_profile and hooks["validationHook"] and all(
        status["present"] for status in sections.values()
    )
    evidence_sections_complete = (
        (hooks["parameterTable"] or hooks["parameterTableSidecar"]) and
        (hooks["performanceEvidence"] or hooks["performanceEvidenceSidecar"]) and
        (hooks["uncertaintyEvidence"] or hooks["uncertaintyEvidenceSidecar"]) and
        hooks["verificationEvidence"] and
        hooks["platformQualificationEvidence"] and
        all(
        sections[name]["present"]
        for name in (
            "modelPerformance",
            "parameterProvenance",
            "uncertainty",
            "implementationVerification",
            "platformQualification",
            "peerReview",
        )
        )
    )

    return {
        "validationMode": "static-manifest-inspection",
        "backend": "rxode2",
        "scientificProfile": scientific_profile,
        "profileSource": profile_source,
        "qualificationLevel": qualification_level,
        "manifestStatus": _manifest_status(issues, scientific_profile, core_sections_complete),
        "qualificationState": derive_qualification_state(
            scientific_profile=scientific_profile,
            profile_source=profile_source,
            qualification_level=qualification_level,
            core_sections_complete=core_sections_complete,
            evidence_sections_complete=evidence_sections_complete,
        ),
        "hooks": hooks,
        "sections": sections,
        "ngraCoverage": ngra_coverage,
        "issues": issues,
        "supplementalEvidence": {
            "parameterTableSidecarPath": parameter_table_sidecar_path,
            "parameterTableRowCount": len(parameter_table_sidecar_rows),
            "parameterTableBundleMetadata": parameter_table_sidecar_metadata,
            "performanceEvidenceSidecarPath": performance_sidecar_path,
            "performanceEvidenceRowCount": len(performance_sidecar_rows),
            "performanceEvidenceBundleMetadata": performance_sidecar_metadata,
            "performanceEvidenceProfileSupplementCoverage": _performance_profile_supplement_coverage(
                performance_sidecar_profile_supplement
            ),
            "uncertaintyEvidenceSidecarPath": uncertainty_sidecar_path,
            "uncertaintyEvidenceRowCount": len(uncertainty_sidecar_rows),
            "uncertaintyEvidenceBundleMetadata": uncertainty_sidecar_metadata,
        },
    }


def validate_model_manifest(file_path: str | Path) -> dict[str, Any]:
    path = Path(file_path).expanduser().resolve()
    suffix = path.suffix.lower()
    backend = SUPPORTED_MODEL_EXTENSIONS.get(suffix)
    if backend is None:
        raise ValueError(f"Unsupported model manifest type for '{path}'")
    if not path.is_file():
        raise FileNotFoundError(path)

    def build_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
        manifest_payload = dict(manifest)
        return {
            "filePath": str(path),
            "backend": backend,
            "runtimeFormat": suffix.lstrip("."),
            "manifest": manifest_payload,
            "curationSummary": build_manifest_curation_summary(manifest_payload),
        }

    if backend == "ospsuite":
        profile, sidecar_path, sidecar_issues = _load_sidecar_profile(path)
        parameter_table_sidecar_rows, parameter_table_sidecar_metadata, parameter_table_sidecar_path, parameter_table_sidecar_issues = _load_parameter_table_sidecar(path)
        (
            performance_sidecar_rows,
            performance_sidecar_metadata,
            performance_sidecar_profile_supplement,
            performance_sidecar_path,
            performance_sidecar_issues,
        ) = _load_performance_evidence_sidecar(path)
        uncertainty_sidecar_rows, uncertainty_sidecar_metadata, uncertainty_sidecar_path, uncertainty_sidecar_issues = _load_uncertainty_evidence_sidecar(path)
        if profile is None:
            scientific_profile = False
            ngra_coverage, _ = _build_ngra_coverage(
                {canonical_name: None for canonical_name in _NGRA_DECLARATION_FIELDS},
                scientific_profile=False,
            )
            return build_payload(
                {
                    "validationMode": "static-manifest-inspection",
                    "backend": backend,
                    "scientificProfile": scientific_profile,
                    "profileSource": "bridge-default",
                    "qualificationLevel": None,
                    "manifestStatus": "missing",
                    "qualificationState": derive_qualification_state(
                        scientific_profile=False,
                        profile_source="bridge-default",
                        qualification_level=None,
                        core_sections_complete=False,
                        evidence_sections_complete=False,
                    ),
                    "sections": {},
                    "ngraCoverage": ngra_coverage,
                    "issues": [*sidecar_issues, *parameter_table_sidecar_issues, *performance_sidecar_issues, *uncertainty_sidecar_issues],
                    "sidecarPath": sidecar_path,
                    "supplementalEvidence": {
                        "parameterTableSidecarPath": parameter_table_sidecar_path,
                        "parameterTableRowCount": len(parameter_table_sidecar_rows),
                        "parameterTableBundleMetadata": parameter_table_sidecar_metadata,
                        "performanceEvidenceSidecarPath": performance_sidecar_path,
                        "performanceEvidenceRowCount": len(performance_sidecar_rows),
                        "performanceEvidenceBundleMetadata": performance_sidecar_metadata,
                        "performanceEvidenceProfileSupplementCoverage": _performance_profile_supplement_coverage(
                            performance_sidecar_profile_supplement
                        ),
                        "uncertaintyEvidenceSidecarPath": uncertainty_sidecar_path,
                        "uncertaintyEvidenceRowCount": len(uncertainty_sidecar_rows),
                        "uncertaintyEvidenceBundleMetadata": uncertainty_sidecar_metadata,
                    },
                }
            )

        manifest = _validate_profile_manifest(
            profile,
            backend=backend,
            profile_source="sidecar",
            sidecar_path=sidecar_path,
        )
        manifest["issues"] = [*sidecar_issues, *parameter_table_sidecar_issues, *performance_sidecar_issues, *uncertainty_sidecar_issues, *manifest["issues"]]
        manifest["supplementalEvidence"] = {
            "parameterTableSidecarPath": parameter_table_sidecar_path,
            "parameterTableRowCount": len(parameter_table_sidecar_rows),
            "parameterTableBundleMetadata": parameter_table_sidecar_metadata,
            "performanceEvidenceSidecarPath": performance_sidecar_path,
            "performanceEvidenceRowCount": len(performance_sidecar_rows),
            "performanceEvidenceBundleMetadata": performance_sidecar_metadata,
            "performanceEvidenceProfileSupplementCoverage": _performance_profile_supplement_coverage(
                performance_sidecar_profile_supplement
            ),
            "uncertaintyEvidenceSidecarPath": uncertainty_sidecar_path,
            "uncertaintyEvidenceRowCount": len(uncertainty_sidecar_rows),
            "uncertaintyEvidenceBundleMetadata": uncertainty_sidecar_metadata,
        }
        return build_payload(manifest)

    return build_payload(_validate_r_model(path))


__all__ = [
    "build_manifest_curation_summary",
    "derive_qualification_state",
    "validate_model_manifest",
]
