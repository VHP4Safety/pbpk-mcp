from __future__ import annotations

from .artifacts import contract_manifest_document


RELEASE_PROBE_REQUIRED_TOOLS = (
    "discover_models",
    "export_oecd_report",
    "get_job_status",
    "get_population_results",
    "get_results",
    "ingest_external_pbpk_bundle",
    "load_simulation",
    "run_population_simulation",
    "run_simulation",
    "run_verification_checks",
    "validate_model_manifest",
    "validate_simulation_request",
)


def release_probe_required_tools() -> tuple[str, ...]:
    return RELEASE_PROBE_REQUIRED_TOOLS


def published_schema_ids() -> tuple[str, ...]:
    manifest = contract_manifest_document()
    schema_ids = [
        str(entry["schemaId"])
        for entry in manifest.get("schemas") or []
        if isinstance(entry, dict) and entry.get("schemaId")
    ]
    return tuple(sorted(dict.fromkeys(schema_ids)))
