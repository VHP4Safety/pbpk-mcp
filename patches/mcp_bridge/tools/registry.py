"""Central registry describing the patched MCP tool surface exposed by the bridge."""

from __future__ import annotations

from typing import Dict

from mcp.tools.discover_models import (
    DiscoverModelsRequest,
    DiscoverModelsResponse,
    discover_models,
)
from mcp.tools.export_oecd_report import (
    ExportOecdReportRequest,
    ExportOecdReportResponse,
    export_oecd_report,
)
from mcp.tools.get_results import (
    GetResultsRequest,
    GetResultsResponse,
    get_results,
)
from mcp.tools.ingest_external_pbpk_bundle import (
    IngestExternalPbpkBundleRequest,
    IngestExternalPbpkBundleResponse,
    ingest_external_pbpk_bundle,
)
from mcp.tools.run_verification_checks import (
    RunVerificationChecksRequest,
    RunVerificationChecksResponse,
    run_verification_checks,
)
from mcp.tools.validate_model_manifest import (
    ValidateModelManifestRequest,
    ValidateModelManifestResponse,
    validate_model_manifest,
)
from mcp.tools.validate_simulation_request import (
    ValidateSimulationRequestRequest,
    ValidateSimulationRequestResponse,
    validate_simulation_request,
)
from mcp_bridge.tools.registry_base import ToolDescriptor, get_base_tool_registry, standard_roles


def get_tool_registry() -> Dict[str, ToolDescriptor]:
    """Return the patched MCP tool registry keyed by tool name."""

    registry = get_base_tool_registry(
        load_simulation_description="Load a PBPK model (.pkml or MCP-ready .R) into the active session registry."
    )
    registry.update(
        {
            "discover_models": ToolDescriptor(
                name="discover_models",
                description="Discover supported PBPK model files under MCP_MODEL_SEARCH_PATHS, including unloaded workspace models.",
                request_model=DiscoverModelsRequest,
                response_model=DiscoverModelsResponse,
                handler=discover_models,
                dependencies=(),
                roles=standard_roles("viewer", "operator", "admin"),
            ),
            "validate_simulation_request": ToolDescriptor(
                name="validate_simulation_request",
                description="Run a preflight OECD-style applicability and guardrail assessment for a loaded model.",
                request_model=ValidateSimulationRequestRequest,
                response_model=ValidateSimulationRequestResponse,
                handler=validate_simulation_request,
                dependencies=("adapter",),
                roles=standard_roles("viewer", "operator", "admin"),
            ),
            "run_verification_checks": ToolDescriptor(
                name="run_verification_checks",
                description="Run executable verification checks for a loaded model, including deterministic smoke tests and optional population smoke where supported.",
                request_model=RunVerificationChecksRequest,
                response_model=RunVerificationChecksResponse,
                handler=run_verification_checks,
                dependencies=("adapter",),
                roles=standard_roles("viewer", "operator", "admin"),
            ),
            "validate_model_manifest": ToolDescriptor(
                name="validate_model_manifest",
                description="Run a static manifest check for a supported model file before loading it, including qualification-state and metadata coverage hints.",
                request_model=ValidateModelManifestRequest,
                response_model=ValidateModelManifestResponse,
                handler=validate_model_manifest,
                dependencies=(),
                roles=standard_roles("viewer", "operator", "admin"),
            ),
            "export_oecd_report": ToolDescriptor(
                name="export_oecd_report",
                description="Export an OECD-style model dossier/report for a loaded simulation, including profile, assessment, and parameter provenance.",
                request_model=ExportOecdReportRequest,
                response_model=ExportOecdReportResponse,
                handler=export_oecd_report,
                dependencies=("adapter",),
                roles=standard_roles("viewer", "operator", "admin"),
            ),
            "get_results": ToolDescriptor(
                name="get_results",
                description="Retrieve stored deterministic simulation results by handle.",
                request_model=GetResultsRequest,
                response_model=GetResultsResponse,
                handler=get_results,
                dependencies=("adapter", "job_service"),
                roles=standard_roles("viewer", "operator", "admin"),
            ),
            "ingest_external_pbpk_bundle": ToolDescriptor(
                name="ingest_external_pbpk_bundle",
                description="Normalize externally generated PBPK outputs, qualification metadata, and optional PoD references into PBPK-side NGRA-ready objects without executing the upstream engine.",
                request_model=IngestExternalPbpkBundleRequest,
                response_model=IngestExternalPbpkBundleResponse,
                handler=ingest_external_pbpk_bundle,
                dependencies=(),
                roles=standard_roles("viewer", "operator", "admin"),
            ),
        }
    )
    return registry


__all__ = ["ToolDescriptor", "get_tool_registry"]
