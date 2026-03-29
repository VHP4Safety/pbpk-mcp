"""Regulatory gold-set documentation benchmark helpers."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_GOLDSET_ROOT = WORKSPACE_ROOT / "benchmarks" / "regulatory_goldset"
DEFAULT_SOURCE_MANIFEST = DEFAULT_GOLDSET_ROOT / "sources.lock.json"
DEFAULT_FETCHED_LOCK = DEFAULT_GOLDSET_ROOT / "fetched.lock.json"
DEFAULT_AUDIT_MANIFEST = DEFAULT_GOLDSET_ROOT / "regulatory_goldset_audit_manifest.json"

DIMENSIONS: tuple[dict[str, str], ...] = (
    {
        "id": "contextOfUseClarity",
        "label": "Context/use clarity",
        "target": "Explicit context-of-use statement, README, or run guide.",
    },
    {
        "id": "runnableCodeModelAvailability",
        "label": "Runnable code/model availability",
        "target": "Public model/code files with enough structure to reproduce simulations.",
    },
    {
        "id": "softwarePlatformSpecificity",
        "label": "Software/platform specificity",
        "target": "Named runtime artifacts or instructions that identify the software stack.",
    },
    {
        "id": "parameterProvenanceDepth",
        "label": "Parameter provenance depth",
        "target": "Parameter labels, codebooks, source tables, or other provenance-oriented tables.",
    },
    {
        "id": "calibrationVsEvaluationSeparation",
        "label": "Calibration vs evaluation separation",
        "target": "Distinct fit/check/evaluation artifacts rather than one undifferentiated bundle.",
    },
    {
        "id": "uncertaintySensitivityVariability",
        "label": "Uncertainty, sensitivity, and variability",
        "target": "Explicit uncertainty or population-variability treatment.",
    },
    {
        "id": "reproducibilityPackCompleteness",
        "label": "Reproducibility-pack completeness",
        "target": "Model files, code, data, outputs, and instructions together.",
    },
    {
        "id": "publicTraceabilityHashability",
        "label": "Public traceability and hashability",
        "target": "Public download paths plus reproducible hashes and stable local evidence paths.",
    },
)
DIMENSION_IDS = tuple(item["id"] for item in DIMENSIONS)
STRICT_CORE_GAP_PRIORITY = (
    "parameterProvenanceDepth",
    "calibrationVsEvaluationSeparation",
    "uncertaintySensitivityVariability",
    "reproducibilityPackCompleteness",
    "softwarePlatformSpecificity",
    "publicTraceabilityHashability",
    "contextOfUseClarity",
    "runnableCodeModelAvailability",
)
MCP_GAP_PRIORITIES = {
    "parameterProvenanceDepth": "Stronger parameter provenance expectations",
    "calibrationVsEvaluationSeparation": "Clearer calibration-vs-evaluation reporting",
    "uncertaintySensitivityVariability": "More structured uncertainty and variability evidence",
    "reproducibilityPackCompleteness": "Clearer reproducibility-pack signals",
    "softwarePlatformSpecificity": "Better software/platform and run-instruction declaration",
    "publicTraceabilityHashability": "Better traceability and hash-linked evidence packaging",
    "contextOfUseClarity": "Clearer context-of-use declaration",
    "runnableCodeModelAvailability": "Sharper runnable-vs-reference model declaration",
}

DOC_EXTENSIONS = {".doc", ".docx", ".html", ".md", ".pdf", ".rmd", ".txt"}
MODEL_EXTENSIONS = {".json", ".mmd", ".model", ".pkml", ".pksim5"}
SCRIPT_EXTENSIONS = {".c", ".cpp", ".dll", ".exe", ".m", ".py", ".r"}
DATA_EXTENSIONS = {".csv", ".dat", ".json", ".rds", ".txt", ".xls", ".xlsx"}
OUTPUT_EXTENSIONS = {".html", ".out", ".pdf", ".png"}

DIMENSION_GUIDANCE: dict[str, dict[str, Sequence[str]]] = {
    "contextOfUseClarity": {
        "evaluatedFrom": (
            "contextOfUse",
            "qualificationState.state",
            "workflowRole",
        ),
        "recommendedNextArtifacts": (
            "Add a model-specific context-of-use note that names the intended regulatory or research question.",
            "Bind the declared workflow role to a bounded use case rather than a generic research label.",
        ),
        "benchmarkExampleIds": ("tce_tsca_package", "epa_voc_template"),
    },
    "runnableCodeModelAvailability": {
        "evaluatedFrom": (
            "manifestStatus",
            "runtimeFormat",
            "profileSource",
        ),
        "recommendedNextArtifacts": (
            "Keep runnable model/code artifacts packaged with a minimal run path that reproduces the declared workflow.",
            "State explicitly whether the runtime artifact is a benchmark-style packaged model, a research example, or an external reference only.",
        ),
        "benchmarkExampleIds": ("tce_tsca_package", "epa_voc_template"),
    },
    "softwarePlatformSpecificity": {
        "evaluatedFrom": (
            "profile.platformQualification",
            "profile.implementationVerification",
            "hooks.platformQualificationEvidence",
            "profileSource",
        ),
        "recommendedNextArtifacts": (
            "Add explicit software, solver, and runtime-version declarations near the model dossier.",
            "Record the platform or adapter assumptions needed to reproduce the exported results.",
        ),
        "benchmarkExampleIds": ("tce_tsca_package", "epa_voc_template"),
    },
    "parameterProvenanceDepth": {
        "evaluatedFrom": (
            "profile.parameterProvenance",
            "profile.parameterTableBundleMetadata",
            "hooks.parameterTable",
            "hooks.parameterTableSidecar",
        ),
        "recommendedNextArtifacts": (
            "Attach a tabular parameter provenance bundle with names, units, sources, and rationale fields.",
            "Expose whether parameter values are literature-sourced, optimized, transferred, or runtime-only placeholders.",
        ),
        "benchmarkExampleIds": ("tce_tsca_package", "epa_voc_template"),
    },
    "calibrationVsEvaluationSeparation": {
        "evaluatedFrom": (
            "profile.modelPerformance",
            "profile.performanceEvidenceBundleMetadata",
            "hooks.performanceEvidence",
            "hooks.performanceEvidenceSidecar",
        ),
        "recommendedNextArtifacts": (
            "Separate fit/calibration evidence from evaluation or predictive-check evidence in the manifest-facing dossier.",
            "Name which datasets or checks were used for optimization versus evaluation.",
        ),
        "benchmarkExampleIds": ("tce_tsca_package",),
    },
    "uncertaintySensitivityVariability": {
        "evaluatedFrom": (
            "profile.uncertainty",
            "profile.uncertaintyEvidenceBundleMetadata",
            "profile.populationSupport",
            "hooks.uncertaintyEvidence",
            "hooks.uncertaintyEvidenceSidecar",
        ),
        "recommendedNextArtifacts": (
            "Add structured uncertainty rows that distinguish local sensitivity, variability propagation, and other uncertainty classes.",
            "State clearly whether variability support is mechanistic, assumed, transferred, or absent.",
        ),
        "benchmarkExampleIds": ("tce_tsca_package", "epa_pfas_template"),
    },
    "reproducibilityPackCompleteness": {
        "evaluatedFrom": (
            "manifestStatus",
            "profileSource",
            "profile.modelPerformance",
            "profile.parameterProvenance",
            "profile.uncertainty",
            "hooks.parameterTable",
            "hooks.performanceEvidence",
            "hooks.uncertaintyEvidence",
        ),
        "recommendedNextArtifacts": (
            "Bundle the runnable model, validation-oriented evidence, parameter provenance, and run instructions as one coherent dossier.",
            "Avoid leaving key evidence split across ad hoc notes or runtime-only outputs.",
        ),
        "benchmarkExampleIds": ("tce_tsca_package", "epa_voc_template"),
    },
    "publicTraceabilityHashability": {
        "evaluatedFrom": (
            "manifestStatus",
            "profile.parameterTableBundleMetadata",
            "profile.performanceEvidenceBundleMetadata",
            "profile.uncertaintyEvidenceBundleMetadata",
            "hooks.parameterTable",
            "hooks.performanceEvidence",
            "hooks.uncertaintyEvidence",
        ),
        "recommendedNextArtifacts": (
            "Attach hash-linked evidence bundle metadata for the parameter, performance, and uncertainty surfaces.",
            "Keep the model dossier reproducible enough that an external reviewer can trace files back to the exported summary.",
        ),
        "benchmarkExampleIds": ("tce_tsca_package", "epa_pfas_template", "pfos_ges_lac"),
    },
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _workspace_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(WORKSPACE_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _safe_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _lookup_path(payload: Mapping[str, Any] | None, dotted_path: str) -> Any:
    current: Any = payload
    for part in dotted_path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


def _path_present(payload: Mapping[str, Any] | None, dotted_path: str) -> bool:
    value = _lookup_path(payload, dotted_path)
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return bool(value)
    return True


def _unique(items: Sequence[str]) -> list[str]:
    deduped: list[str] = []
    for item in items:
        if item and item not in deduped:
            deduped.append(item)
    return deduped


def _contains_any(paths: Sequence[str], tokens: Sequence[str]) -> list[str]:
    matches: list[str] = []
    for path in paths:
        lowered = path.lower()
        if any(token in lowered for token in tokens):
            matches.append(path)
    return matches


def _scan_fetched_source_artifacts(source: Mapping[str, Any] | None) -> dict[str, Any]:
    artifacts = list((source or {}).get("artifacts") or [])
    candidate_paths = _unique(
        [
            str(path)
            for artifact in artifacts
            for path in ((artifact or {}).get("candidateFilesSample") or [])
            if _safe_text(path)
        ]
    )
    extension_counts = Counter(
        (Path(path).suffix.lower() or "<none>")
        for path in candidate_paths
    )
    readme_paths = _contains_any(candidate_paths, ("readme",))
    instruction_paths = _contains_any(candidate_paths, ("instruction", "run_guide", "run-guide"))
    parameter_paths = _contains_any(
        candidate_paths,
        ("datalabs", "codebook", "codingbook", "outputvar-labels", "parameter", "source"),
    )
    fit_paths = _contains_any(candidate_paths, ("fit", "posterior", "priors", "mcmc", "seqpriors"))
    evaluation_paths = _contains_any(
        candidate_paths,
        ("check", "evaluation", "validation", "poppred", "predictive", "modelresults", "results"),
    )
    uncertainty_paths = _contains_any(
        candidate_paths,
        ("uncertainty", "sensitivity", "posterior", "priors", "mcmc", "seqpriors"),
    )
    variability_paths = _contains_any(candidate_paths, ("population", "poppred", "seqpriors", ".pop."))

    file_count = 0
    for artifact in artifacts:
        extracted = artifact.get("extractedFileCount")
        candidate = artifact.get("candidateFileCount")
        if isinstance(extracted, int) and extracted > file_count:
            file_count = extracted
        elif isinstance(candidate, int) and candidate > file_count:
            file_count = candidate

    evidence_paths = _unique(
        readme_paths[:2]
        + instruction_paths[:2]
        + parameter_paths[:3]
        + fit_paths[:3]
        + evaluation_paths[:3]
        + uncertainty_paths[:3]
    )[:12]

    return {
        "available": bool(artifacts),
        "rootPath": next(
            (
                str((artifact or {}).get("extractPath"))
                for artifact in artifacts
                if _safe_text((artifact or {}).get("extractPath"))
            ),
            None,
        ),
        "fileCount": file_count,
        "extensionCounts": dict(sorted(extension_counts.items())),
        "docFileCount": sum(1 for path in candidate_paths if Path(path).suffix.lower() in DOC_EXTENSIONS),
        "modelFileCount": sum(1 for path in candidate_paths if Path(path).suffix.lower() in MODEL_EXTENSIONS),
        "scriptFileCount": sum(1 for path in candidate_paths if Path(path).suffix.lower() in SCRIPT_EXTENSIONS),
        "dataFileCount": sum(1 for path in candidate_paths if Path(path).suffix.lower() in DATA_EXTENSIONS),
        "outputFileCount": sum(1 for path in candidate_paths if Path(path).suffix.lower() in OUTPUT_EXTENSIONS),
        "flags": {
            "hasReadme": bool(readme_paths),
            "hasInstructions": bool(instruction_paths),
            "hasParameterArtifacts": bool(parameter_paths),
            "hasCalibrationArtifacts": bool(fit_paths),
            "hasEvaluationArtifacts": bool(evaluation_paths),
            "hasUncertaintyArtifacts": bool(uncertainty_paths),
            "hasVariabilityArtifacts": bool(variability_paths),
            "hasCompiledRuntimeArtifacts": any(
                Path(path).suffix.lower() in {".dll", ".exe"}
                for path in candidate_paths
            ),
        },
        "evidencePaths": evidence_paths,
    }


def _documentation_only_dimension(source: Mapping[str, Any], dimension_id: str) -> dict[str, Any]:
    notes = [str(item) for item in (source.get("notes") or []) if _safe_text(item)]
    if dimension_id == "contextOfUseClarity":
        status = "partial" if notes else "missing"
        reason = (
            "This source is tracked as a documentation-only confidence benchmark, so only prose-level context is available."
            if notes
            else "No direct public package is available yet."
        )
        return {
            "id": dimension_id,
            "status": status,
            "reason": reason,
            "evidence": notes[:2],
        }
    return {
        "id": dimension_id,
        "status": "not-applicable",
        "reason": "This source is documentation-only and is not being scored as an executable/code package in phase 1.",
        "evidence": [],
    }


def _score_source_dimension(
    source: Mapping[str, Any],
    fetched_source: Mapping[str, Any] | None,
    scan: Mapping[str, Any],
    *,
    dimension_id: str,
) -> dict[str, Any]:
    if source.get("benchmarkRole") == "documentation-only":
        return _documentation_only_dimension(source, dimension_id)

    notes = [str(item) for item in (source.get("notes") or []) if _safe_text(item)]
    coverage_models = [str(item) for item in (source.get("coverageModels") or []) if _safe_text(item)]
    artifacts = fetched_source.get("artifacts") if isinstance(fetched_source, Mapping) else []
    file_count = int(scan.get("fileCount") or 0)
    flags = dict(scan.get("flags") or {})
    evidence_paths = list(scan.get("evidencePaths") or [])
    has_readme_or_instructions = bool(flags.get("hasReadme") or flags.get("hasInstructions"))
    has_model_runtime = int(scan.get("modelFileCount") or 0) > 0
    has_scripts = int(scan.get("scriptFileCount") or 0) > 0
    has_data = int(scan.get("dataFileCount") or 0) > 0
    has_parameter = bool(flags.get("hasParameterArtifacts"))
    has_fit = bool(flags.get("hasCalibrationArtifacts"))
    has_eval = bool(flags.get("hasEvaluationArtifacts"))
    has_uncertainty = bool(flags.get("hasUncertaintyArtifacts"))
    has_variability = bool(flags.get("hasVariabilityArtifacts"))
    has_hashes = bool(artifacts) and all(
        _safe_text((artifact or {}).get("sha256")) and _safe_text((artifact or {}).get("downloadPath"))
        for artifact in artifacts
    )

    if dimension_id == "contextOfUseClarity":
        if coverage_models and has_readme_or_instructions and notes:
            return {
                "id": dimension_id,
                "status": "present",
                "reason": "The package includes explicit model coverage plus a README or run-guide artifact.",
                "evidence": _unique([*coverage_models, *evidence_paths[:3], *notes[:1]])[:4],
            }
        if coverage_models or has_readme_or_instructions or notes:
            return {
                "id": dimension_id,
                "status": "partial",
                "reason": "The package provides some context signals, but not a consistently explicit context-of-use framing.",
                "evidence": _unique([*coverage_models, *evidence_paths[:2], *notes[:1]])[:4],
            }
        return {
            "id": dimension_id,
            "status": "missing",
            "reason": "No clear README, run guide, or explicit coverage statement was found.",
            "evidence": [],
        }

    if dimension_id == "runnableCodeModelAvailability":
        if has_model_runtime and has_scripts:
            return {
                "id": dimension_id,
                "status": "present",
                "reason": "Model/runtime files and executable scripts are both present.",
                "evidence": evidence_paths[:4],
            }
        if has_model_runtime or has_scripts:
            return {
                "id": dimension_id,
                "status": "partial",
                "reason": "Some code or model artifacts are present, but the runnable stack is incomplete.",
                "evidence": evidence_paths[:4],
            }
        return {
            "id": dimension_id,
            "status": "missing",
            "reason": "No public model/code package was found in the fetched contents.",
            "evidence": [],
        }

    if dimension_id == "softwarePlatformSpecificity":
        if has_readme_or_instructions and (has_model_runtime or bool(flags.get("hasCompiledRuntimeArtifacts"))):
            return {
                "id": dimension_id,
                "status": "present",
                "reason": "The package identifies the runtime through instructions and software-specific artifacts.",
                "evidence": evidence_paths[:4],
            }
        if has_model_runtime or has_scripts or has_readme_or_instructions:
            return {
                "id": dimension_id,
                "status": "partial",
                "reason": "The package hints at a software stack, but platform/run details are still thin.",
                "evidence": evidence_paths[:4],
            }
        return {
            "id": dimension_id,
            "status": "missing",
            "reason": "No clear software/platform declaration was found.",
            "evidence": [],
        }

    if dimension_id == "parameterProvenanceDepth":
        if has_parameter and has_data:
            return {
                "id": dimension_id,
                "status": "present",
                "reason": "The package contains parameter-label or codebook style artifacts alongside tabular data.",
                "evidence": evidence_paths[:5],
            }
        if has_parameter or has_data:
            return {
                "id": dimension_id,
                "status": "partial",
                "reason": "Some data or parameter hints are present, but provenance depth is limited.",
                "evidence": evidence_paths[:4],
            }
        return {
            "id": dimension_id,
            "status": "missing",
            "reason": "No parameter-table or parameter-provenance artifacts were detected.",
            "evidence": [],
        }

    if dimension_id == "calibrationVsEvaluationSeparation":
        if has_fit and has_eval:
            return {
                "id": dimension_id,
                "status": "present",
                "reason": "The package separates fit-oriented artifacts from evaluation/check outputs.",
                "evidence": evidence_paths[:5],
            }
        if has_fit or has_eval:
            return {
                "id": dimension_id,
                "status": "partial",
                "reason": "The package shows some validation or fitting structure, but not a clear separation.",
                "evidence": evidence_paths[:4],
            }
        return {
            "id": dimension_id,
            "status": "missing",
            "reason": "No distinct calibration or evaluation artifacts were detected.",
            "evidence": [],
        }

    if dimension_id == "uncertaintySensitivityVariability":
        if has_uncertainty and has_variability:
            return {
                "id": dimension_id,
                "status": "present",
                "reason": "The package includes explicit uncertainty and population-variability signals.",
                "evidence": evidence_paths[:5],
            }
        if has_uncertainty or has_variability:
            return {
                "id": dimension_id,
                "status": "partial",
                "reason": "The package includes some uncertainty or variability signals, but coverage is limited.",
                "evidence": evidence_paths[:4],
            }
        return {
            "id": dimension_id,
            "status": "missing",
            "reason": "No explicit uncertainty, sensitivity, or variability artifacts were detected.",
            "evidence": [],
        }

    if dimension_id == "reproducibilityPackCompleteness":
        supporting_count = sum(
            [
                1 if has_readme_or_instructions else 0,
                1 if has_model_runtime else 0,
                1 if has_scripts else 0,
                1 if has_data else 0,
                1 if has_eval else 0,
            ]
        )
        if supporting_count >= 5 and file_count >= 10:
            return {
                "id": dimension_id,
                "status": "present",
                "reason": "The package includes instructions, model/code artifacts, data, and evaluation outputs together.",
                "evidence": evidence_paths[:6],
            }
        if supporting_count >= 3:
            return {
                "id": dimension_id,
                "status": "partial",
                "reason": "The package is reproducible enough to inspect, but it is still missing some pack elements.",
                "evidence": evidence_paths[:5],
            }
        return {
            "id": dimension_id,
            "status": "missing",
            "reason": "The package does not yet look like a coherent reproducibility pack.",
            "evidence": [],
        }

    if dimension_id == "publicTraceabilityHashability":
        if has_hashes and (fetched_source or {}).get("result") == "fetched":
            return {
                "id": dimension_id,
                "status": "present",
                "reason": "The package has public download paths, stable local evidence paths, and SHA-256 hashes.",
                "evidence": [
                    str((artifact or {}).get("downloadPath"))
                    for artifact in artifacts[:3]
                    if _safe_text((artifact or {}).get("downloadPath"))
                ],
            }
        if artifacts or notes:
            return {
                "id": dimension_id,
                "status": "partial",
                "reason": "Some source-traceability information is available, but the package is not fully hash-linked.",
                "evidence": [
                    str((artifact or {}).get("downloadPath"))
                    for artifact in artifacts[:2]
                    if _safe_text((artifact or {}).get("downloadPath"))
                ][:2]
                + notes[:1],
            }
        return {
            "id": dimension_id,
            "status": "missing",
            "reason": "No stable public traceability or hash-linked acquisition path was found.",
            "evidence": [],
        }

    raise KeyError(f"Unsupported dimension: {dimension_id}")


def _overall_tier(source: Mapping[str, Any], dimensions: Sequence[Mapping[str, Any]]) -> str:
    benchmark_role = _safe_text(source.get("benchmarkRole")) or "unknown"
    if benchmark_role == "documentation-only":
        return "documentation-only-reference"
    present_count = sum(1 for item in dimensions if item.get("status") == "present")
    partial_count = sum(1 for item in dimensions if item.get("status") == "partial")
    if benchmark_role == "adjunct-challenge-set":
        return "challenge-set"
    if present_count >= 6 and partial_count <= 2:
        return "benchmark-grade"
    if present_count + partial_count >= 5:
        return "strong-but-incomplete"
    return "reference-only"


def _source_card(
    source: Mapping[str, Any],
    fetched_source: Mapping[str, Any] | None,
) -> dict[str, Any]:
    scan = _scan_fetched_source_artifacts(fetched_source)
    dimensions = [
        _score_source_dimension(source, fetched_source, scan, dimension_id=dimension_id)
        for dimension_id in DIMENSION_IDS
    ]
    for item in dimensions:
        item["label"] = next(defn["label"] for defn in DIMENSIONS if defn["id"] == item["id"])
    dimension_summary = {
        "present": sum(1 for item in dimensions if item["status"] == "present"),
        "partial": sum(1 for item in dimensions if item["status"] == "partial"),
        "missing": sum(1 for item in dimensions if item["status"] == "missing"),
        "notApplicable": sum(1 for item in dimensions if item["status"] == "not-applicable"),
    }
    return {
        "id": source.get("id"),
        "title": source.get("title"),
        "benchmarkRole": source.get("benchmarkRole"),
        "coverageModels": list(source.get("coverageModels") or []),
        "sourceType": source.get("sourceType"),
        "status": source.get("status"),
        "result": (fetched_source or {}).get("result") or source.get("status"),
        "notes": list(source.get("notes") or []),
        "scanSummary": scan,
        "scorecard": {
            "scorecardVersion": "pbpk-regulatory-goldset-source-scorecard.v1",
            "overallTier": _overall_tier(source, dimensions),
            "dimensionCounts": dimension_summary,
            "dimensions": dimensions,
        },
        "artifacts": list((fetched_source or {}).get("artifacts") or []),
    }


def _aggregate_benchmark_bar(source_cards: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    strict_core = [
        item
        for item in source_cards
        if item.get("benchmarkRole") == "strict-core" and item.get("result") == "fetched"
    ]
    adjunct = [item.get("id") for item in source_cards if item.get("benchmarkRole") == "adjunct-challenge-set"]
    documentation = [item.get("id") for item in source_cards if item.get("benchmarkRole") == "documentation-only"]

    coverage: dict[str, dict[str, Any]] = {}
    required_dimensions: list[str] = []
    strong_dimensions: list[str] = []
    variable_dimensions: list[str] = []

    for dimension in DIMENSIONS:
        dimension_id = dimension["id"]
        statuses = [
            next(
                item for item in (card.get("scorecard") or {}).get("dimensions") or []
                if item.get("id") == dimension_id
            )["status"]
            for card in strict_core
        ]
        present_count = sum(1 for status in statuses if status == "present")
        partial_count = sum(1 for status in statuses if status == "partial")
        missing_count = sum(1 for status in statuses if status == "missing")
        if strict_core and present_count == len(strict_core):
            classification = "consistent-core-expectation"
            required_dimensions.append(dimension_id)
        elif strict_core and present_count + partial_count == len(strict_core):
            classification = "strong-but-variable"
            strong_dimensions.append(dimension_id)
        else:
            classification = "variable-or-weaker"
            variable_dimensions.append(dimension_id)
        coverage[dimension_id] = {
            "label": dimension["label"],
            "strictCorePresentCount": present_count,
            "strictCorePartialCount": partial_count,
            "strictCoreMissingCount": missing_count,
            "strictCoreSourceCount": len(strict_core),
            "classification": classification,
        }

    prioritized_targets = []
    for priority, dimension_id in enumerate(STRICT_CORE_GAP_PRIORITY, start=1):
        prioritized_targets.append(
            {
                "priority": priority,
                "dimensionId": dimension_id,
                "label": MCP_GAP_PRIORITIES[dimension_id],
                "why": (
                    "This dimension is part of the documentation/reproducibility bar implied by the fetched "
                    "regulatory benchmark corpus and should be clearer in MCP trust/reporting surfaces."
                ),
                "barClassification": coverage[dimension_id]["classification"],
            }
        )

    return {
        "barVersion": "pbpk-regulatory-goldset-bar.v1",
        "strictCoreSourceIds": [item.get("id") for item in strict_core],
        "adjunctSourceIds": adjunct,
        "documentationReferenceIds": documentation,
        "requiredDimensions": required_dimensions,
        "strongButVariableDimensions": strong_dimensions,
        "weakerOrVariableDimensions": variable_dimensions,
        "dimensionCoverage": coverage,
        "summary": (
            "The strict-core regulatory packages consistently emphasize context of use, runnable artifacts, "
            "software specificity, provenance depth, uncertainty treatment, reproducibility packaging, and "
            "hash-linked traceability. Challenge sets add stress-testing value, while documentation-only references "
            "mainly calibrate the confidence language."
        ),
        "prioritizedMcpImprovementTargets": prioritized_targets,
    }


def analyze_regulatory_goldset(
    *,
    source_manifest_path: Path = DEFAULT_SOURCE_MANIFEST,
    fetched_lock_path: Path = DEFAULT_FETCHED_LOCK,
) -> dict[str, Any]:
    source_manifest = _load_json(source_manifest_path)
    fetched_lock = _load_json(fetched_lock_path)
    fetched_sources = {
        str(item.get("id")): item
        for item in (fetched_lock.get("sources") or [])
        if isinstance(item, Mapping)
    }

    source_cards = [
        _source_card(source, fetched_sources.get(str(source.get("id"))))
        for source in (source_manifest.get("sources") or [])
        if isinstance(source, Mapping)
    ]

    return {
        "summaryVersion": "pbpk-regulatory-goldset-scorecard.v1",
        "sourceManifestPath": _workspace_relative(source_manifest_path),
        "sourceManifestSha256": _sha256(source_manifest_path),
        "fetchedLockPath": _workspace_relative(fetched_lock_path),
        "fetchedLockSha256": _sha256(fetched_lock_path),
        "dimensionDefinitions": list(DIMENSIONS),
        "sources": source_cards,
        "benchmarkBar": _aggregate_benchmark_bar(source_cards),
    }


def _section_present(manifest: Mapping[str, Any], name: str) -> bool:
    return bool(((manifest.get("sections") or {}).get(name) or {}).get("present"))


def _supplemental_count(manifest: Mapping[str, Any], key: str) -> int:
    return int(((manifest.get("supplementalEvidence") or {}).get(key) or 0))


def _supplemental_metadata_present(manifest: Mapping[str, Any], key: str) -> bool:
    return bool((manifest.get("supplementalEvidence") or {}).get(key))


def _hook_present(manifest: Mapping[str, Any], key: str) -> bool:
    return bool((manifest.get("hooks") or {}).get(key))


def _manifest_dimension_statuses(manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    profile_source = _safe_text(manifest.get("profileSource")) or "unknown"
    risk_assessment_ready = bool(((manifest.get("qualificationState") or {}).get("riskAssessmentReady")))
    perf_coverage = (manifest.get("supplementalEvidence") or {}).get(
        "performanceEvidenceProfileSupplementCoverage"
    ) or {}
    performance_rows = _supplemental_count(manifest, "performanceEvidenceRowCount")
    uncertainty_rows = _supplemental_count(manifest, "uncertaintyEvidenceRowCount")
    parameter_rows = _supplemental_count(manifest, "parameterTableRowCount")

    statuses: list[dict[str, Any]] = []

    context_present = _section_present(manifest, "contextOfUse")
    statuses.append(
        {
            "id": "contextOfUseClarity",
            "status": "present" if context_present else "missing",
            "reason": (
                "The manifest declares a structured contextOfUse section."
                if context_present
                else "The manifest does not expose a structured contextOfUse section."
            ),
        }
    )

    runnable_status = "present" if _safe_text(manifest.get("manifestStatus")) == "valid" else "missing"
    statuses.append(
        {
            "id": "runnableCodeModelAvailability",
            "status": runnable_status,
            "reason": (
                "The model file is in a supported runtime format and passes static manifest validation."
                if runnable_status == "present"
                else "The model file does not currently validate as a supported runnable artifact."
            ),
        }
    )

    if _section_present(manifest, "implementationVerification") and _section_present(manifest, "platformQualification"):
        software_status = (
            "present"
            if profile_source == "sidecar"
            or risk_assessment_ready
            else "partial"
        )
    elif _section_present(manifest, "implementationVerification") or _section_present(manifest, "platformQualification"):
        software_status = "partial"
    else:
        software_status = "missing"
    statuses.append(
        {
            "id": "softwarePlatformSpecificity",
            "status": software_status,
            "reason": (
                "Implementation verification and platform-qualification declarations are present."
                if software_status == "present"
                else "The model declares some software/runtime details, but not to benchmark-grade depth."
                if software_status == "partial"
                else "The manifest does not declare software/platform specifics clearly."
            ),
        }
    )

    if _section_present(manifest, "parameterProvenance"):
        provenance_status = (
            "present"
            if parameter_rows > 0 or _supplemental_metadata_present(manifest, "parameterTableBundleMetadata")
            else "partial"
        )
    else:
        provenance_status = "missing"
    statuses.append(
        {
            "id": "parameterProvenanceDepth",
            "status": provenance_status,
            "reason": (
                "Parameter provenance is backed by a parameter table hook or bundled rows."
                if provenance_status == "present"
                else "Parameter provenance is declared, but without benchmark-grade tabular provenance evidence."
                if provenance_status == "partial"
                else "Parameter provenance is not declared."
            ),
        }
    )

    calibration_signal = bool(
        performance_rows > 0
        or bool(perf_coverage.get("predictiveDatasetRecordCount"))
        or bool(perf_coverage.get("evaluationDatasetRecordCount"))
        or bool(perf_coverage.get("acceptanceCriterionCount"))
    )
    if _section_present(manifest, "modelPerformance"):
        calibration_status = "present" if calibration_signal else "partial"
    else:
        calibration_status = "missing"
    statuses.append(
        {
            "id": "calibrationVsEvaluationSeparation",
            "status": calibration_status,
            "reason": (
                "Model-performance evidence includes predictive/evaluation structure or acceptance criteria."
                if calibration_status == "present"
                else "Model performance is declared, but benchmark-style evaluation structure is still thin."
                if calibration_status == "partial"
                else "The manifest does not declare model-performance evidence."
            ),
        }
    )

    if _section_present(manifest, "uncertainty"):
        uncertainty_status = (
            "present"
            if uncertainty_rows > 0 or _supplemental_metadata_present(manifest, "uncertaintyEvidenceBundleMetadata")
            else "partial"
        )
    else:
        uncertainty_status = "missing"
    statuses.append(
        {
            "id": "uncertaintySensitivityVariability",
            "status": uncertainty_status,
            "reason": (
                "Uncertainty is backed by an uncertainty-evidence hook or bundled rows."
                if uncertainty_status == "present"
                else "Uncertainty is declared, but benchmark-style quantified evidence is still thin."
                if uncertainty_status == "partial"
                else "The manifest does not declare uncertainty evidence."
            ),
        }
    )

    present_like = {
        item["id"]: item["status"]
        for item in statuses
    }
    reproducibility_support = sum(
        1
        for dimension_id in (
            "contextOfUseClarity",
            "runnableCodeModelAvailability",
            "softwarePlatformSpecificity",
            "parameterProvenanceDepth",
            "calibrationVsEvaluationSeparation",
            "uncertaintySensitivityVariability",
        )
        if present_like.get(dimension_id) in {"present", "partial"}
    )
    if reproducibility_support >= 6 and (_safe_text(manifest.get("profileSource")) == "sidecar" or risk_assessment_ready):
        reproducibility_status = "present"
    elif reproducibility_support >= 4:
        reproducibility_status = "partial"
    else:
        reproducibility_status = "missing"
    statuses.append(
        {
            "id": "reproducibilityPackCompleteness",
            "status": reproducibility_status,
            "reason": (
                "The model exposes a coherent runnable/validation/evidence structure."
                if reproducibility_status == "present"
                else "The model is inspectable and runnable, but it is not packaged like the strongest public regulatory bundles."
                if reproducibility_status == "partial"
                else "The model does not expose a coherent reproducibility pack."
            ),
        }
    )

    traceability_status = (
        "present"
        if _supplemental_metadata_present(manifest, "performanceEvidenceBundleMetadata")
        or _supplemental_metadata_present(manifest, "parameterTableBundleMetadata")
        or _supplemental_metadata_present(manifest, "uncertaintyEvidenceBundleMetadata")
        else "partial"
        if _safe_text(manifest.get("manifestStatus")) == "valid"
        else "missing"
    )
    statuses.append(
        {
            "id": "publicTraceabilityHashability",
            "status": traceability_status,
            "reason": (
                "The model exposes bundle-style metadata that can travel with the evidence."
                if traceability_status == "present"
                else "The manifest is traceable in-repo, but it does not yet resemble a hash-linked public benchmark package."
                if traceability_status == "partial"
                else "The model is not traceable enough for benchmark comparison."
            ),
        }
    )

    for item in statuses:
        item["label"] = next(defn["label"] for defn in DIMENSIONS if defn["id"] == item["id"])
        guidance = DIMENSION_GUIDANCE[item["id"]]
        item["evaluatedFrom"] = list(guidance["evaluatedFrom"])
        item["observedManifestFields"] = [
            field
            for field in guidance["evaluatedFrom"]
            if _path_present(manifest, field)
        ]
        item["recommendedNextArtifacts"] = list(guidance["recommendedNextArtifacts"])
        item["benchmarkExampleIds"] = list(guidance["benchmarkExampleIds"])
    return statuses


def _benchmark_bar_source(
    *,
    source_manifest_path: Path,
    fetched_lock_path: Path,
) -> dict[str, Any]:
    source_manifest_relative = _workspace_relative(source_manifest_path)
    fetched_lock_relative = _workspace_relative(fetched_lock_path)
    source_manifest_sha = _sha256(source_manifest_path) if source_manifest_path.exists() else None
    fetched_lock_sha = _sha256(fetched_lock_path) if fetched_lock_path.exists() else None
    resolution = "direct-lock-files" if source_manifest_sha and fetched_lock_sha else "unresolved"

    if DEFAULT_AUDIT_MANIFEST.exists():
        try:
            audit_manifest = _load_json(DEFAULT_AUDIT_MANIFEST)
        except json.JSONDecodeError:
            audit_manifest = {}
        source_entry = dict(audit_manifest.get("sourceManifest") or {})
        fetched_entry = dict(audit_manifest.get("fetchedLock") or {})
        source_manifest_relative = source_entry.get("relativePath") or source_manifest_relative
        fetched_lock_relative = fetched_entry.get("relativePath") or fetched_lock_relative
        source_manifest_sha = source_manifest_sha or source_entry.get("sha256")
        fetched_lock_sha = fetched_lock_sha or fetched_entry.get("sha256")
        if resolution != "direct-lock-files" and source_manifest_sha and fetched_lock_sha:
            resolution = "audit-manifest-fallback"

    if not source_manifest_sha or not fetched_lock_sha:
        try:
            from mcp_bridge.contract import contract_manifest_document
        except Exception:  # pragma: no cover - defensive fallback for packaging edge cases
            contract_manifest_document = None
        if contract_manifest_document is not None:
            try:
                contract_manifest = contract_manifest_document()
            except Exception:  # pragma: no cover - defensive fallback for packaging edge cases
                contract_manifest = {}
            supporting = {
                entry.get("relativePath"): entry
                for entry in (contract_manifest.get("supportingArtifacts") or [])
                if isinstance(entry, Mapping) and entry.get("relativePath")
            }
            source_entry = dict(supporting.get(source_manifest_relative) or {})
            fetched_entry = dict(supporting.get(fetched_lock_relative) or {})
            source_manifest_sha = source_manifest_sha or source_entry.get("sha256")
            fetched_lock_sha = fetched_lock_sha or fetched_entry.get("sha256")
            if resolution == "unresolved" and source_manifest_sha and fetched_lock_sha:
                resolution = "packaged-contract-fallback"

    return {
        "sourceManifestPath": source_manifest_relative,
        "fetchedLockPath": fetched_lock_relative,
        "sourceManifestSha256": source_manifest_sha,
        "fetchedLockSha256": fetched_lock_sha,
        "sourceResolution": resolution,
        "dimensionIds": list(DIMENSION_IDS),
    }


def derive_manifest_benchmark_readiness(
    manifest: Mapping[str, Any] | None,
    *,
    source_manifest_path: Path = DEFAULT_SOURCE_MANIFEST,
    fetched_lock_path: Path = DEFAULT_FETCHED_LOCK,
) -> dict[str, Any]:
    manifest_payload = dict(manifest or {})
    profile_source = _safe_text(manifest_payload.get("profileSource")) or "unknown"
    statuses = _manifest_dimension_statuses(manifest_payload)
    present = [item["id"] for item in statuses if item["status"] == "present"]
    partial = [item["id"] for item in statuses if item["status"] == "partial"]
    missing = [item["id"] for item in statuses if item["status"] == "missing"]
    qualification_state = _safe_text(((manifest_payload.get("qualificationState") or {}).get("state"))) or "undeclared"
    risk_assessment_ready = bool(((manifest_payload.get("qualificationState") or {}).get("riskAssessmentReady")))

    if risk_assessment_ready and not missing:
        overall_status = "benchmark-aligned-documentation"
    elif len(present) >= 4 and len(missing) <= 2:
        overall_status = "approaching-benchmark-bar"
    else:
        overall_status = "below-benchmark-bar"

    if qualification_state in {"qualified-within-context", "regulatory-use", "qualified", "externally-qualified"}:
        resemblance = "regulatory-candidate"
    elif qualification_state == "illustrative-example":
        resemblance = "research-example"
    else:
        resemblance = "research-example"

    prioritized_gaps = []
    for priority, dimension_id in enumerate(STRICT_CORE_GAP_PRIORITY, start=1):
        if dimension_id in missing or dimension_id in partial:
            current = next(item for item in statuses if item["id"] == dimension_id)
            prioritized_gaps.append(
                {
                    "priority": priority,
                    "dimensionId": dimension_id,
                    "label": MCP_GAP_PRIORITIES[dimension_id],
                    "currentStatus": current["status"],
                    "reason": current["reason"],
                    "evaluatedFrom": list(current.get("evaluatedFrom") or []),
                    "observedManifestFields": list(current.get("observedManifestFields") or []),
                    "recommendedNextArtifacts": list(current.get("recommendedNextArtifacts") or []),
                    "benchmarkExampleIds": list(current.get("benchmarkExampleIds") or []),
                }
            )

    recommended_artifacts = _unique(
        [
            artifact
            for item in prioritized_gaps
            for artifact in (item.get("recommendedNextArtifacts") or [])
            if _safe_text(artifact)
        ]
    )

    return {
        "sectionVersion": "pbpk-regulatory-benchmark-readiness.v1",
        "advisoryOnly": True,
        "benchmarkBarSource": _benchmark_bar_source(
            source_manifest_path=source_manifest_path,
            fetched_lock_path=fetched_lock_path,
        ),
        "modelResemblance": resemblance,
        "overallStatus": overall_status,
        "plainLanguageSummary": (
            "This benchmark-readiness summary is advisory only. It compares the current model dossier to the "
            "documentation and reproducibility bar implied by the fetched regulatory gold set; it does not change "
            "qualification state or release gating."
        ),
        "presentDimensions": present,
        "partialDimensions": partial,
        "missingDimensions": missing,
        "dimensionStatuses": statuses,
        "prioritizedGaps": prioritized_gaps,
        "recommendedNextArtifacts": recommended_artifacts,
        "notes": [
            f"Qualification state remains {qualification_state}; benchmark readiness is a separate descriptive surface.",
            (
                "The strongest public benchmark bar is represented by the fetched TCE and VOC template packages."
            ),
            (
                "PFAS and PFOS remain useful challenge sets for transparency and reproducibility, not automatic regulatory templates."
            ),
            f"Current profile source: {profile_source}.",
        ],
    }


def render_regulatory_goldset_summary(report: Mapping[str, Any]) -> str:
    benchmark_bar = dict(report.get("benchmarkBar") or {})
    sources = list(report.get("sources") or [])
    internal_use_cases = list(report.get("referenceModelComparisons") or [])
    lines = [
        "# Regulatory Gold-Set Benchmark Summary",
        "",
        "This dossier distills the documentation and reproducibility bar implied by the fetched public-code PBPK benchmark packages.",
        "",
        "## Benchmark Bar",
        "",
        f"- Source manifest: `{report.get('sourceManifestPath')}`",
        f"- Source manifest SHA-256: `{report.get('sourceManifestSha256')}`",
        f"- Fetched lock: `{report.get('fetchedLockPath')}`",
        f"- Fetched lock SHA-256: `{report.get('fetchedLockSha256')}`",
        f"- Strict-core sources: {', '.join(benchmark_bar.get('strictCoreSourceIds') or [])}",
        f"- Challenge-set sources: {', '.join(benchmark_bar.get('adjunctSourceIds') or [])}",
        f"- Documentation-only references: {', '.join(benchmark_bar.get('documentationReferenceIds') or [])}",
        "",
        benchmark_bar.get("summary") or "",
        "",
        "### Consistent core expectations",
        "",
    ]
    for dimension_id in benchmark_bar.get("requiredDimensions") or []:
        label = next(item["label"] for item in DIMENSIONS if item["id"] == dimension_id)
        lines.append(f"- `{dimension_id}`: {label}")
    lines.extend(
        [
            "",
            "### Strong but more variable dimensions",
            "",
        ]
    )
    for dimension_id in benchmark_bar.get("strongButVariableDimensions") or []:
        label = next(item["label"] for item in DIMENSIONS if item["id"] == dimension_id)
        lines.append(f"- `{dimension_id}`: {label}")

    lines.extend(
        [
            "",
            "## Per-Source Findings",
            "",
        ]
    )
    for source in sources:
        scorecard = source.get("scorecard") or {}
        counts = scorecard.get("dimensionCounts") or {}
        lines.extend(
            [
                f"### {source.get('title')}",
                "",
                f"- Role: `{source.get('benchmarkRole')}`",
                f"- Result: `{source.get('result')}`",
                f"- Overall tier: `{scorecard.get('overallTier')}`",
                (
                    f"- Dimension counts: {counts.get('present', 0)} present, "
                    f"{counts.get('partial', 0)} partial, {counts.get('missing', 0)} missing, "
                    f"{counts.get('notApplicable', 0)} not applicable"
                ),
            ]
        )
        if source.get("notes"):
            lines.append(f"- Notes: {' '.join(str(item) for item in source.get('notes') or [])}")
        strongest = [
            item["label"]
            for item in (scorecard.get("dimensions") or [])
            if item.get("status") == "present"
        ][:4]
        if strongest:
            lines.append(f"- Strongest signals: {', '.join(strongest)}")
        lines.append("")

    lines.extend(
        [
            "## Internal Non-Benchmark Use-Case Comparison",
            "",
        ]
    )
    if internal_use_cases:
        comparison = dict(internal_use_cases[0])
        readiness = dict(comparison.get("regulatoryBenchmarkReadiness") or {})
        lines.extend(
            [
                f"- Internal use case: `{comparison.get('modelPath')}`",
                f"- Qualification state: `{comparison.get('qualificationState')}`",
                f"- Benchmark resemblance: `{readiness.get('modelResemblance')}`",
                f"- Overall benchmark-readiness status: `{readiness.get('overallStatus')}`",
                f"- Present dimensions: {', '.join(readiness.get('presentDimensions') or []) or 'none'}",
                f"- Partial dimensions: {', '.join(readiness.get('partialDimensions') or []) or 'none'}",
                f"- Missing dimensions: {', '.join(readiness.get('missingDimensions') or []) or 'none'}",
                f"- Benchmark source manifest SHA-256: `{((readiness.get('benchmarkBarSource') or {}).get('sourceManifestSha256'))}`",
                f"- Benchmark fetched-lock SHA-256: `{((readiness.get('benchmarkBarSource') or {}).get('fetchedLockSha256'))}`",
                f"- Benchmark source resolution: `{((readiness.get('benchmarkBarSource') or {}).get('sourceResolution'))}`",
                "",
                "The synthetic reference model remains a `research-use` internal MCP use case. It is useful for smoke testing, audit rehearsal, and trust-surface validation, but it is not part of the regulatory benchmark corpus.",
                "",
                "### Top dossier-improvement signals",
                "",
            ]
        )
        for item in (readiness.get("prioritizedGaps") or [])[:4]:
            lines.append(
                f"- `{item.get('dimensionId')}`: {item.get('label')}. "
                f"Evaluated from {', '.join(item.get('evaluatedFrom') or []) or 'n/a'}. "
                f"Suggested next artifacts: {' '.join(item.get('recommendedNextArtifacts') or [])}"
            )
        lines.append("")

    lines.extend(
        [
            "## Prioritized MCP Improvement Targets",
            "",
        ]
    )
    for item in benchmark_bar.get("prioritizedMcpImprovementTargets") or []:
        lines.append(
            f"- `{item.get('dimensionId')}`: {item.get('label')}. {item.get('why')}"
        )

    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


__all__ = [
    "DEFAULT_FETCHED_LOCK",
    "DEFAULT_GOLDSET_ROOT",
    "DEFAULT_SOURCE_MANIFEST",
    "DIMENSIONS",
    "analyze_regulatory_goldset",
    "derive_manifest_benchmark_readiness",
    "render_regulatory_goldset_summary",
]
