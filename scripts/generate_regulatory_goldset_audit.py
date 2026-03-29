#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = WORKSPACE_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mcp_bridge.benchmarking.regulatory_goldset import (  # noqa: E402
    DEFAULT_FETCHED_LOCK,
    DEFAULT_GOLDSET_ROOT,
    DEFAULT_SOURCE_MANIFEST,
    analyze_regulatory_goldset,
    derive_manifest_benchmark_readiness,
    render_regulatory_goldset_summary,
)
from mcp_bridge.model_manifest import validate_model_manifest  # noqa: E402


DEFAULT_SCORECARD_OUTPUT = DEFAULT_GOLDSET_ROOT / "regulatory_goldset_scorecard.json"
DEFAULT_SUMMARY_OUTPUT = DEFAULT_GOLDSET_ROOT / "regulatory_goldset_summary.md"
DEFAULT_MANIFEST_OUTPUT = DEFAULT_GOLDSET_ROOT / "regulatory_goldset_audit_manifest.json"
DEFAULT_REFERENCE_MODEL = (
    WORKSPACE_ROOT / "var" / "models" / "rxode2" / "reference_compound" / "reference_compound_population_rxode2_model.R"
)


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def _workspace_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(WORKSPACE_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_path(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _build_audit_manifest(
    *,
    analysis: dict,
    scorecard_output: Path,
    summary_output: Path,
    source_manifest_path: Path,
    fetched_lock_path: Path,
) -> dict[str, object]:
    sources = []
    for source in analysis.get("sources") or []:
        artifacts = []
        for artifact in source.get("artifacts") or []:
            entry = {
                "id": artifact.get("id"),
                "downloadPath": artifact.get("downloadPath"),
                "downloadSha256": artifact.get("sha256"),
                "extractPath": artifact.get("extractPath"),
                "extractedFileCount": artifact.get("extractedFileCount"),
            }
            artifacts.append(entry)
        sources.append(
            {
                "id": source.get("id"),
                "benchmarkRole": source.get("benchmarkRole"),
                "result": source.get("result"),
                "rootPath": (source.get("scanSummary") or {}).get("rootPath"),
                "artifacts": artifacts,
            }
        )

    tracked_outputs = [
        {
            "relativePath": _workspace_relative(scorecard_output),
            "sha256": _sha256_path(scorecard_output),
        },
        {
            "relativePath": _workspace_relative(summary_output),
            "sha256": _sha256_path(summary_output),
        },
    ]
    bundle_payload = "\n".join(
        f"{item['relativePath']}:{item['sha256']}"
        for item in tracked_outputs
    ) + "\n"

    return {
        "id": "pbpk-regulatory-goldset-audit-manifest.v1",
        "analysisVersion": analysis["summaryVersion"],
        "sourceManifest": {
            "relativePath": _workspace_relative(source_manifest_path),
            "sha256": _sha256_path(source_manifest_path),
        },
        "fetchedLock": {
            "relativePath": _workspace_relative(fetched_lock_path),
            "sha256": _sha256_path(fetched_lock_path),
        },
        "trackedOutputs": tracked_outputs,
        "trackedOutputBundleSha256": _sha256_bytes(bundle_payload.encode("utf-8")),
        "sources": sources,
        "referenceModelComparisons": analysis.get("referenceModelComparisons") or [],
    }


def _verify_manifest(manifest_path: Path) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mismatches: list[str] = []
    checked_files = 0

    for entry in [manifest.get("sourceManifest") or {}, manifest.get("fetchedLock") or {}]:
        relative_path = entry.get("relativePath")
        expected_sha = entry.get("sha256")
        if not relative_path or not expected_sha:
            mismatches.append(f"incomplete source entry: {entry!r}")
            continue
        path = WORKSPACE_ROOT / relative_path
        if not path.exists():
            mismatches.append(f"missing source file: {relative_path}")
            continue
        checked_files += 1
        if _sha256_path(path) != expected_sha:
            mismatches.append(f"sha256 mismatch for {relative_path}")

    tracked_outputs = list(manifest.get("trackedOutputs") or [])
    bundle_payload = []
    for entry in tracked_outputs:
        relative_path = entry.get("relativePath")
        expected_sha = entry.get("sha256")
        if not relative_path or not expected_sha:
            mismatches.append(f"incomplete tracked output entry: {entry!r}")
            continue
        path = WORKSPACE_ROOT / relative_path
        if not path.exists():
            mismatches.append(f"missing tracked output: {relative_path}")
            continue
        checked_files += 1
        actual_sha = _sha256_path(path)
        if actual_sha != expected_sha:
            mismatches.append(f"sha256 mismatch for {relative_path}")
        bundle_payload.append(f"{relative_path}:{expected_sha}")

    actual_bundle_sha = _sha256_bytes(("\n".join(bundle_payload) + "\n").encode("utf-8"))
    if actual_bundle_sha != manifest.get("trackedOutputBundleSha256"):
        mismatches.append("trackedOutputBundleSha256 does not match listed outputs")

    return {
        "status": "passed" if not mismatches else "failed",
        "manifestPath": _workspace_relative(manifest_path),
        "checkedFileCount": checked_files,
        "manifestSha256": _sha256_path(manifest_path),
        "mismatches": mismatches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-manifest", type=Path, default=DEFAULT_SOURCE_MANIFEST)
    parser.add_argument("--fetched-lock", type=Path, default=DEFAULT_FETCHED_LOCK)
    parser.add_argument("--reference-model", type=Path, default=DEFAULT_REFERENCE_MODEL)
    parser.add_argument("--scorecard-output", type=Path, default=DEFAULT_SCORECARD_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--manifest-output", type=Path, default=DEFAULT_MANIFEST_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the tracked audit outputs differ from a regenerated benchmark analysis.",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Verify the existing benchmark audit manifest and outputs without regenerating them.",
    )
    args = parser.parse_args()

    if args.verify_only:
        verification = _verify_manifest(args.manifest_output)
        print(json.dumps(verification, indent=2))
        return 0 if verification["status"] == "passed" else 1

    analysis = analyze_regulatory_goldset(
        source_manifest_path=args.source_manifest,
        fetched_lock_path=args.fetched_lock,
    )
    reference_payload = validate_model_manifest(args.reference_model.resolve())
    comparison = {
        "id": "reference_workspace_model",
        "title": "Workspace synthetic reference model",
        "modelPath": _workspace_relative(args.reference_model),
        "qualificationState": ((reference_payload.get("manifest") or {}).get("qualificationState") or {}).get("state"),
        "regulatoryBenchmarkReadiness": derive_manifest_benchmark_readiness(
            reference_payload.get("manifest") or {},
            source_manifest_path=args.source_manifest,
            fetched_lock_path=args.fetched_lock,
        ),
    }
    analysis["referenceModelComparisons"] = [comparison]

    scorecard_text = _json_text(analysis)
    summary_text = render_regulatory_goldset_summary(analysis)

    if args.check:
        mismatches = []
        if args.scorecard_output.read_text(encoding="utf-8") != scorecard_text:
            mismatches.append(_workspace_relative(args.scorecard_output))
        if args.summary_output.read_text(encoding="utf-8") != summary_text:
            mismatches.append(_workspace_relative(args.summary_output))
        if mismatches:
            print(json.dumps({"status": "failed", "mismatches": mismatches}, indent=2))
            return 1
        verification = _verify_manifest(args.manifest_output)
        print(json.dumps(verification, indent=2))
        return 0 if verification["status"] == "passed" else 1

    _write(args.scorecard_output, scorecard_text)
    _write(args.summary_output, summary_text)
    manifest = _build_audit_manifest(
        analysis=analysis,
        scorecard_output=args.scorecard_output,
        summary_output=args.summary_output,
        source_manifest_path=args.source_manifest,
        fetched_lock_path=args.fetched_lock,
    )
    _write(args.manifest_output, _json_text(manifest))
    verification = _verify_manifest(args.manifest_output)

    print(
        json.dumps(
            {
                "scorecard": _workspace_relative(args.scorecard_output),
                "summary": _workspace_relative(args.summary_output),
                "manifest": _workspace_relative(args.manifest_output),
                "verification": verification,
            },
            indent=2,
        )
    )
    return 0 if verification["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
