from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence
from pathlib import Path


@dataclass(frozen=True)
class RuntimePatch:
    source: str
    target: str


PATCHES: tuple[RuntimePatch, ...] = (
    RuntimePatch(
        "scripts/runtime_src_overlay.pth",
        "/usr/local/lib/python3.11/site-packages/pbpk_mcp_runtime_src.pth",
    ),
    RuntimePatch("scripts/ospsuite_bridge.R", "/app/scripts/ospsuite_bridge.R"),
    RuntimePatch(
        "cisplatin_models/cisplatin_population_rxode2_model.R",
        "/app/var/models/rxode2/cisplatin/cisplatin_population_rxode2_model.R",
    ),
)

HOT_PATCHES: tuple[RuntimePatch, ...] = (
    RuntimePatch(
        "scripts/runtime_src_overlay.pth",
        "/usr/local/lib/python3.11/site-packages/pbpk_mcp_runtime_src.pth",
    ),
)

DEFAULT_PATCH_CONTAINERS: tuple[str, ...] = ("pbpk_mcp-api-1", "pbpk_mcp-worker-1")


def iter_patch_mappings(workspace_root: Path) -> Iterable[tuple[Path, str]]:
    for patch in PATCHES:
        yield workspace_root / patch.source, patch.target


def iter_hot_patch_mappings(workspace_root: Path) -> Iterable[tuple[Path, str]]:
    for patch in HOT_PATCHES:
        yield workspace_root / patch.source, patch.target


def target_directories(patches: Sequence[RuntimePatch] | None = None) -> tuple[str, ...]:
    active_patches = tuple(patches or PATCHES)
    directories = {str(Path(patch.target).parent) for patch in active_patches}
    directories = sorted(directories)
    return tuple(directories)


def python_target_paths(patches: Sequence[RuntimePatch] | None = None) -> tuple[str, ...]:
    active_patches = tuple(patches or PATCHES)
    return tuple(patch.target for patch in active_patches if patch.target.endswith(".py"))


def r_target_paths(patches: Sequence[RuntimePatch] | None = None) -> tuple[str, ...]:
    active_patches = tuple(patches or PATCHES)
    return tuple(patch.target for patch in active_patches if patch.target.endswith(".R"))


def pth_target_paths(patches: Sequence[RuntimePatch] | None = None) -> tuple[str, ...]:
    active_patches = tuple(patches or PATCHES)
    return tuple(patch.target for patch in active_patches if patch.target.endswith(".pth"))


__all__ = [
    "DEFAULT_PATCH_CONTAINERS",
    "HOT_PATCHES",
    "PATCHES",
    "RuntimePatch",
    "iter_hot_patch_mappings",
    "iter_patch_mappings",
    "pth_target_paths",
    "python_target_paths",
    "r_target_paths",
    "target_directories",
]
