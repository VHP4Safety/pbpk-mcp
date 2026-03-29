#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = WORKSPACE_ROOT / "src"
PATCH_ROOT = WORKSPACE_ROOT / "patches"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
if str(PATCH_ROOT) not in sys.path:
    sys.path.insert(0, str(PATCH_ROOT))

from mcp_bridge.curated_publication import curated_publication_model_paths  # noqa: E402
from mcp_bridge.model_manifest import validate_model_manifest  # noqa: E402

SUPPORTED_MODEL_EXTENSIONS = {".pkml", ".r"}
MODEL_PATH_ENV = "ADAPTER_MODEL_PATHS"
MODEL_PATH_ENV_ALIASES = ("ADAPTER_MODEL_PATHS", "MCP_MODEL_SEARCH_PATHS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate static PBPK model manifests for supported .pkml and MCP-ready .R files."
    )
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Model file to validate. Repeat to validate multiple paths. Defaults to all discovered models.",
    )
    parser.add_argument(
        "--backend",
        choices=("ospsuite", "rxode2"),
        default=None,
        help="Restrict validation to a single backend when scanning discovery roots.",
    )
    parser.add_argument(
        "--curated-publication-set",
        action="store_true",
        help=(
            "Validate the bundled curated publication models used by release-prep gating. "
            "May be combined with repeated --path arguments."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 when any validated model is not manifestStatus='valid'.",
    )
    parser.add_argument(
        "--require-explicit-ngra",
        action="store_true",
        help=(
            "Exit with code 1 when any validated model still relies on implicit NGRA boundary "
            "declarations in curationSummary."
        ),
    )
    return parser.parse_args()


def resolve_model_roots() -> tuple[Path, ...]:
    raw = next((os.getenv(name) for name in MODEL_PATH_ENV_ALIASES if os.getenv(name)), "")
    if raw.strip():
        roots = [Path(chunk.strip()).expanduser() for chunk in raw.split(os.pathsep) if chunk.strip()]
    else:
        roots = [
            WORKSPACE_ROOT / "var",
            WORKSPACE_ROOT / "reference" / "models" / "standard",
            WORKSPACE_ROOT / "tests" / "fixtures",
        ]
    resolved = []
    seen = set()
    for root in roots:
        candidate = root.resolve()
        if not candidate.exists():
            continue
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        resolved.append(candidate)
    return tuple(resolved)


def _collect_targets(paths: list[str], backend: str | None) -> list[Path]:
    if paths:
        resolved = [Path(path).expanduser().resolve() for path in paths]
        deduped: list[Path] = []
        seen: set[str] = set()
        for path in resolved:
            key = str(path)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(path)
        return deduped

    targets: list[Path] = []
    for root in resolve_model_roots():
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            suffix = path.suffix.lower()
            if suffix not in SUPPORTED_MODEL_EXTENSIONS:
                continue
            if backend == "ospsuite" and suffix != ".pkml":
                continue
            if backend == "rxode2" and suffix != ".r":
                continue
            targets.append(path.resolve())
    targets.sort()
    return targets


def collect_targets(paths: list[str], backend: str | None, *, curated_publication_set: bool) -> list[Path]:
    selection = list(paths)
    if curated_publication_set:
        selection.extend(str(path) for path in curated_publication_model_paths(WORKSPACE_ROOT))
    return _collect_targets(selection, backend)


def _summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    statuses = [str(item["manifest"].get("manifestStatus", "unknown")) for item in items]
    qualification_states = [
        str((item["manifest"].get("qualificationState") or {}).get("state", "unknown"))
        for item in items
    ]
    curation_summaries = [dict(item.get("curationSummary") or {}) for item in items]
    return {
        "total": len(items),
        "valid": sum(1 for status in statuses if status == "valid"),
        "partial": sum(1 for status in statuses if status == "partial"),
        "missing": sum(1 for status in statuses if status == "missing"),
        "explicitNgraDeclarations": sum(
            1 for summary in curation_summaries if bool(summary.get("ngraDeclarationsExplicit"))
        ),
        "riskAssessmentReady": sum(
            1 for summary in curation_summaries if bool(summary.get("riskAssessmentReady"))
        ),
        "withMissingSections": sum(
            1 for summary in curation_summaries if bool(summary.get("missingSections"))
        ),
        "withImplicitNgraBoundaries": sum(
            1 for summary in curation_summaries if bool(summary.get("missingNgraDeclarations"))
        ),
        "states": {
            state: qualification_states.count(state)
            for state in sorted(set(qualification_states))
        },
    }


def _evaluate_gates(
    items: list[dict[str, Any]],
    *,
    strict: bool,
    require_explicit_ngra: bool,
) -> dict[str, Any]:
    applied_checks: list[str] = []
    if strict:
        applied_checks.append("manifestStatus=valid")
    if require_explicit_ngra:
        applied_checks.append("curationSummary.ngraDeclarationsExplicit=true")

    failures: list[dict[str, Any]] = []
    for item in items:
        manifest = dict(item.get("manifest") or {})
        curation_summary = dict(item.get("curationSummary") or {})
        failure_codes: list[str] = []

        if strict and manifest.get("manifestStatus") != "valid":
            failure_codes.append("manifest_status_invalid")
        if require_explicit_ngra and not bool(curation_summary.get("ngraDeclarationsExplicit")):
            failure_codes.append("implicit_ngra_boundaries")

        if not failure_codes:
            continue

        failures.append(
            {
                "filePath": item.get("filePath"),
                "backend": item.get("backend"),
                "runtimeFormat": item.get("runtimeFormat"),
                "failureCodes": failure_codes,
                "manifestStatus": manifest.get("manifestStatus"),
                "qualificationState": (manifest.get("qualificationState") or {}).get("state"),
                "reviewLabel": curation_summary.get("reviewLabel"),
                "missingSections": list(curation_summary.get("missingSections") or []),
                "missingNgraDeclarations": list(
                    curation_summary.get("missingNgraDeclarations") or []
                ),
            }
        )

    return {
        "appliedChecks": applied_checks,
        "failed": bool(failures),
        "failureCount": len(failures),
        "failures": failures,
    }


def main() -> int:
    args = parse_args()
    targets = collect_targets(
        args.path,
        args.backend,
        curated_publication_set=args.curated_publication_set,
    )
    items = [validate_model_manifest(path) for path in targets]
    gating = _evaluate_gates(
        items,
        strict=args.strict,
        require_explicit_ngra=args.require_explicit_ngra,
    )
    payload = {
        "summary": _summary(items),
        "gating": gating,
        "items": items,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))

    if gating["failed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
