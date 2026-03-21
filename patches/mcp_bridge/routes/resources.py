"""Patch-only MCP resource extensions for the model catalog."""

from __future__ import annotations

from typing import Optional

from fastapi import Depends, Query, Request, Response, status
from pydantic import Field

from mcp.session_registry import SessionRegistry
from mcp_bridge.routes.resources_base import CamelModel
from mcp_bridge.routes.resources_base import _http_error, _paginate, _should_offload, _weak_etag, router

from ..dependencies import get_session_registry
from ..errors import ErrorCode
from ..model_catalog import discover_models as discover_model_entries
from ..model_catalog import model_catalog_fingerprint
from ..util.concurrency import maybe_to_thread


class ModelResource(CamelModel):
    id: str
    model_id: str = Field(alias="modelId")
    suggested_simulation_id: str = Field(alias="suggestedSimulationId")
    file_path: str = Field(alias="filePath")
    relative_path: str = Field(alias="relativePath")
    root_path: str = Field(alias="rootPath")
    backend: str
    runtime_format: str = Field(alias="runtimeFormat")
    display_name: Optional[str] = Field(default=None, alias="displayName")
    model_version: Optional[str] = Field(default=None, alias="modelVersion")
    scientific_profile: Optional[bool] = Field(default=None, alias="scientificProfile")
    profile_source: Optional[str] = Field(default=None, alias="profileSource")
    population_simulation: Optional[bool] = Field(default=None, alias="populationSimulation")
    validation_hook: Optional[bool] = Field(default=None, alias="validationHook")
    discovery_state: str = Field(alias="discoveryState")
    is_loaded: bool = Field(alias="isLoaded")
    loaded_simulation_ids: list[str] = Field(default_factory=list, alias="loadedSimulationIds")
    modified_at: str = Field(alias="modifiedAt")
    metadata: dict[str, object] = Field(default_factory=dict)


class ModelResourcePage(CamelModel):
    items: list[ModelResource]
    page: int
    limit: int
    total: int


@router.get("/models", response_model=ModelResourcePage)
async def list_model_resources(
    request: Request,
    response: Response,
    session_store: SessionRegistry = Depends(get_session_registry),
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(default=None),
    backend: Optional[str] = Query(default=None),
    loaded_only: bool = Query(default=False, alias="loadedOnly"),
) -> ModelResourcePage:
    offload = _should_offload(request)
    snapshot = await maybe_to_thread(offload, session_store.snapshot)

    try:
        all_items = await maybe_to_thread(
            offload,
            discover_model_entries,
            search=search,
            backend=backend,
            loaded_records=snapshot,
            loaded_only=loaded_only,
        )
    except ValueError as exc:
        raise _http_error(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
            code=ErrorCode.INVALID_INPUT,
            field="backend",
            hint="Use 'ospsuite' or 'rxode2'.",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive
        raise _http_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Unexpected error discovering models",
            code=ErrorCode.INTERNAL_ERROR,
        ) from exc

    total = len(all_items)
    page_items = list(_paginate(all_items, page=page, limit=limit))
    items = [ModelResource.model_validate(item) for item in page_items]

    fingerprint = model_catalog_fingerprint(page_items)
    etag = _weak_etag(
        [fingerprint, str(page), str(limit), search or "", backend or "", str(loaded_only)]
    )
    headers = {"ETag": etag}
    if page_items:
        headers["Last-Modified"] = max(item["modifiedAt"] for item in page_items)

    if request.headers.get("if-none-match") == etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=headers)

    response.headers.update(headers)
    return ModelResourcePage(items=items, page=page, limit=limit, total=total)


__all__ = [
    "ModelResource",
    "ModelResourcePage",
    "list_model_resources",
    "router",
]
