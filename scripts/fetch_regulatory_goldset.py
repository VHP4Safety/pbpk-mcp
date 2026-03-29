#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import Any


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_MANIFEST = WORKSPACE_ROOT / "benchmarks" / "regulatory_goldset" / "sources.lock.json"
DEFAULT_GOLDSET_ROOT = WORKSPACE_ROOT / "benchmarks" / "regulatory_goldset"
DEFAULT_FETCHED_LOCK = DEFAULT_GOLDSET_ROOT / "fetched.lock.json"
DOWNLOAD_ROOT = DEFAULT_GOLDSET_ROOT / "downloads"
EXTRACT_ROOT = DEFAULT_GOLDSET_ROOT / "extracted"
MODEL_SUFFIXES = {".model", ".r", ".pkml", ".txt", ".csv", ".tsv", ".xlsx", ".pdf", ".docx", ".json", ".m"}


def _json_text(payload: object) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _safe_rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(WORKSPACE_ROOT))
    except ValueError:
        return str(path.resolve())


def _download(url: str, destination: Path) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "pbpk-mcp-goldset-fetch/1.0"})
    hasher = hashlib.sha256()
    total_bytes = 0
    content_type = None

    with urllib.request.urlopen(request, timeout=300) as response, destination.open("wb") as handle:
        content_type = response.headers.get("Content-Type")
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
            hasher.update(chunk)
            total_bytes += len(chunk)

    return {
        "sha256": hasher.hexdigest(),
        "bytes": total_bytes,
        "contentType": content_type,
    }


def _local_file_metadata(path: Path) -> dict[str, Any]:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
    return {
        "sha256": hasher.hexdigest(),
        "bytes": path.stat().st_size,
    }


def _extract_zip(archive_path: Path, destination: Path) -> dict[str, Any]:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(destination)
        entries = archive.infolist()

    extracted_files = [path for path in destination.rglob("*") if path.is_file()]
    candidate_files = [
        _safe_rel(path)
        for path in extracted_files
        if path.suffix.lower() in MODEL_SUFFIXES
    ]
    candidate_files.sort()
    return {
        "archiveEntryCount": len(entries),
        "extractedFileCount": len(extracted_files),
        "candidateFileCount": len(candidate_files),
        "candidateFilesSample": candidate_files[:40],
    }


def _summarize_extracted_tree(destination: Path) -> dict[str, Any] | None:
    if not destination.exists():
        return None
    extracted_files = [path for path in destination.rglob("*") if path.is_file()]
    candidate_files = [
        _safe_rel(path)
        for path in extracted_files
        if path.suffix.lower() in MODEL_SUFFIXES
    ]
    candidate_files.sort()
    return {
        "archiveEntryCount": None,
        "extractedFileCount": len(extracted_files),
        "candidateFileCount": len(candidate_files),
        "candidateFilesSample": candidate_files[:40],
    }


def _should_skip_large(source: dict[str, Any], include_large: bool) -> bool:
    return str(source.get("sizeClass")) == "large" and not include_large


def fetch_goldset(
    source_manifest_path: Path,
    goldset_root: Path,
    *,
    include_large: bool,
    selected_ids: set[str] | None,
) -> dict[str, Any]:
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    downloads_root = goldset_root / "downloads"
    extract_root = goldset_root / "extracted"
    downloads_root.mkdir(parents=True, exist_ok=True)
    extract_root.mkdir(parents=True, exist_ok=True)

    fetched_sources: list[dict[str, Any]] = []
    for source in source_manifest.get("sources") or []:
        source_id = str(source.get("id"))
        if selected_ids and source_id not in selected_ids:
            continue

        source_record: dict[str, Any] = {
            "id": source_id,
            "title": source.get("title"),
            "benchmarkRole": source.get("benchmarkRole"),
            "coverageModels": source.get("coverageModels") or [],
            "status": source.get("status"),
            "notes": source.get("notes") or [],
            "artifacts": [],
        }

        if source.get("status") != "retrievable":
            source_record["result"] = "unresolved-source"
            fetched_sources.append(source_record)
            continue

        if _should_skip_large(source, include_large):
            source_record["result"] = "skipped-large-source"
            fetched_sources.append(source_record)
            continue

        source_download_root = downloads_root / source_id
        source_extract_root = extract_root / source_id
        source_download_root.mkdir(parents=True, exist_ok=True)
        source_extract_root.mkdir(parents=True, exist_ok=True)

        source_result = "fetched"
        for artifact in source.get("artifacts") or []:
            artifact_id = str(artifact.get("id"))
            url = str(artifact.get("url"))
            filename = Path(url.split("?")[0]).name or f"{artifact_id}.bin"
            download_path = source_download_root / filename
            artifact_record: dict[str, Any] = {
                "id": artifact_id,
                "label": artifact.get("label"),
                "url": url,
                "downloadPath": _safe_rel(download_path),
            }
            try:
                if download_path.exists():
                    download_meta = _local_file_metadata(download_path)
                    download_meta["contentType"] = None
                    artifact_record["usedCachedDownload"] = True
                else:
                    download_meta = _download(url, download_path)
                    artifact_record["usedCachedDownload"] = False
                artifact_record.update(download_meta)
                if artifact.get("archive") and artifact.get("extract"):
                    extract_path = source_extract_root / artifact_id
                    extract_meta = _summarize_extracted_tree(extract_path)
                    if extract_meta is None:
                        extract_meta = _extract_zip(download_path, extract_path)
                        artifact_record["usedCachedExtraction"] = False
                    else:
                        artifact_record["usedCachedExtraction"] = True
                    artifact_record["extractPath"] = _safe_rel(extract_path)
                    artifact_record.update(extract_meta)
            except Exception as exc:  # pragma: no cover - network/runtime failure path
                artifact_record["error"] = str(exc)
                source_result = "partial-fetch-failure"
            source_record["artifacts"].append(artifact_record)

        source_record["result"] = source_result
        fetched_sources.append(source_record)

    summary = {
        "formatVersion": 1,
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sourceManifestPath": _safe_rel(source_manifest_path),
        "goldsetRoot": _safe_rel(goldset_root),
        "includeLarge": include_large,
        "fetchedSourceCount": len(fetched_sources),
        "sources": fetched_sources,
    }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-manifest", type=Path, default=DEFAULT_SOURCE_MANIFEST)
    parser.add_argument("--goldset-root", type=Path, default=DEFAULT_GOLDSET_ROOT)
    parser.add_argument("--output-lock", type=Path, default=DEFAULT_FETCHED_LOCK)
    parser.add_argument(
        "--benchmark",
        action="append",
        default=[],
        help="Only fetch the given benchmark id. Repeat to fetch multiple ids.",
    )
    parser.add_argument(
        "--include-large",
        action="store_true",
        help="Allow fetching large sources such as the EPA TCE package.",
    )
    args = parser.parse_args()

    selected_ids = {item for item in args.benchmark if item}
    summary = fetch_goldset(
        args.source_manifest,
        args.goldset_root,
        include_large=args.include_large,
        selected_ids=selected_ids or None,
    )
    args.output_lock.parent.mkdir(parents=True, exist_ok=True)
    args.output_lock.write_text(_json_text(summary), encoding="utf-8")
    print(_json_text(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
