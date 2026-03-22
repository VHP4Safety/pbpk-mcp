from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
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
)

DEFAULT_PATCH_CONTAINERS: tuple[str, ...] = ("pbpk_mcp-api-1", "pbpk_mcp-worker-1")


def iter_patch_mappings(workspace_root: Path) -> Iterable[tuple[Path, str]]:
    for patch in PATCHES:
        yield workspace_root / patch.source, patch.target


def target_directories() -> tuple[str, ...]:
    directories = {str(Path(patch.target).parent) for patch in PATCHES}
    directories = sorted(directories)
    return tuple(directories)


def python_target_paths() -> tuple[str, ...]:
    return tuple(patch.target for patch in PATCHES if patch.target.endswith(".py"))


def r_target_paths() -> tuple[str, ...]:
    return tuple(patch.target for patch in PATCHES if patch.target.endswith(".R"))


def pth_target_paths() -> tuple[str, ...]:
    return tuple(patch.target for patch in PATCHES if patch.target.endswith(".pth"))


__all__ = [
    "DEFAULT_PATCH_CONTAINERS",
    "PATCHES",
    "RuntimePatch",
    "iter_patch_mappings",
    "pth_target_paths",
    "python_target_paths",
    "r_target_paths",
    "target_directories",
]
