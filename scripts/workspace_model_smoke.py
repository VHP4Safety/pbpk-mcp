#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from uuid import uuid4

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = WORKSPACE_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mcp_bridge.security.simple_jwt import jwt  # noqa: E402


DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_OUTPUT = Path("var") / "workspace_model_smoke_report.json"
RUNTIME_FORMATS = {"pkml", "r"}


def build_auth_headers(
    *,
    bearer_token: str | None,
    auth_dev_secret: str | None,
    auth_role: str,
) -> dict[str, str]:
    if bearer_token:
        return {"authorization": f"Bearer {bearer_token}"}
    if auth_dev_secret:
        token = jwt.encode(
            {
                "sub": "workspace-model-smoke",
                "roles": [auth_role],
                "iat": int(time.time()),
                "exp": int(time.time()) + 3600,
            },
            auth_dev_secret,
            algorithm="HS256",
        )
        return {"authorization": f"Bearer {token}"}
    return {}


def append_auth_hint(error: str, *, has_auth_headers: bool) -> str:
    if has_auth_headers or "HTTP 403" not in error:
        return error
    return (
        f"{error} Hint: provide --auth-dev-secret or --bearer-token because "
        "load/run smoke operations require operator or admin access on hardened runtimes."
    )


def http_json(
    url: str,
    payload: dict | None = None,
    *,
    timeout: int = 60,
    headers: dict[str, str] | None = None,
) -> dict:
    data = None
    request_headers: dict[str, str] = dict(headers or {})
    if payload is not None:
        data = json.dumps(payload).encode()
        request_headers["content-type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=request_headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"raw": body}
        raise RuntimeError(f"{url} returned HTTP {exc.code}: {json.dumps(parsed)}") from exc


def call_tool(
    base_url: str,
    tool: str,
    arguments: dict,
    *,
    critical: bool = False,
    timeout: int = 60,
    headers: dict[str, str] | None = None,
) -> dict:
    response = http_json(
        f"{base_url.rstrip('/')}/mcp/call_tool",
        payload={"tool": tool, "arguments": arguments, **({"critical": True} if critical else {})},
        timeout=timeout,
        headers=headers,
    )
    return response["structuredContent"]


def list_models(
    base_url: str,
    *,
    search: str | None = None,
    backends: set[str] | None = None,
    limit: int | None = None,
    headers: dict[str, str] | None = None,
) -> list[dict]:
    page = 1
    page_size = 200
    items: list[dict] = []

    while True:
        query = {"page": page, "limit": page_size}
        if search:
            query["search"] = search
        if backends and len(backends) == 1:
            query["backend"] = next(iter(backends))
        url = f"{base_url.rstrip('/')}/mcp/resources/models?{urllib.parse.urlencode(query)}"
        payload = http_json(url, timeout=60, headers=headers)
        batch = payload.get("items", [])
        if backends and len(backends) > 1:
            batch = [item for item in batch if str(item.get("backend")) in backends]
        items.extend(batch)
        total = int(payload.get("total", len(items)))
        if len(items) >= total or not batch:
            break
        if limit and len(items) >= limit:
            break
        page += 1

    if limit:
        items = items[:limit]

    return [item for item in items if str(item.get("runtimeFormat", "")).lower() in RUNTIME_FORMATS]


def poll_job(
    base_url: str,
    job_id: str,
    *,
    timeout_seconds: int = 300,
    headers: dict[str, str] | None = None,
) -> dict:
    deadline = time.time() + timeout_seconds
    last_status: dict | None = None
    while time.time() < deadline:
        payload = call_tool(
            base_url,
            "get_job_status",
            {"jobId": job_id},
            timeout=30,
            headers=headers,
        )
        last_status = payload
        if payload["status"] in {"succeeded", "failed", "cancelled", "timeout"}:
            return payload
        time.sleep(2)
    raise RuntimeError(f"Timed out waiting for job {job_id}: {json.dumps(last_status)}")


def make_simulation_id(prefix: str, backend: str) -> str:
    compact_prefix = prefix.lower().replace(" ", "-")[:24]
    return f"smoke-{backend}-{compact_prefix}-{uuid4().hex[:8]}"


def maybe_population_smoke(
    base_url: str,
    simulation_id: str,
    timeout_seconds: int,
    *,
    headers: dict[str, str] | None = None,
) -> dict | None:
    response = call_tool(
        base_url,
        "run_population_simulation",
        {
            "simulationId": simulation_id,
            "cohort": {"size": 10, "seed": 42},
            "outputs": {"aggregates": ["meanCmax", "sdCmax", "meanAUC", "sdAUC"]},
        },
        critical=True,
        timeout=60,
        headers=headers,
    )
    job = poll_job(
        base_url,
        response["jobId"],
        timeout_seconds=timeout_seconds,
        headers=headers,
    )
    result = {
        "jobId": response["jobId"],
        "status": job["status"],
        "resultId": job.get("resultId"),
        "error": job.get("error"),
    }
    if job["status"] == "succeeded" and job.get("resultId"):
        payload = call_tool(
            base_url,
            "get_population_results",
            {"resultsId": job["resultId"]},
            timeout=60,
            headers=headers,
        )
        result["aggregateKeys"] = sorted((payload.get("aggregates") or {}).keys())
        result["chunkCount"] = len(payload.get("chunks") or [])
    return result


def smoke_model(
    base_url: str,
    entry: dict,
    *,
    include_population: bool,
    timeout_seconds: int,
    headers: dict[str, str] | None = None,
) -> dict:
    file_path = str(entry["filePath"])
    backend = str(entry["backend"])
    simulation_id = make_simulation_id(Path(file_path).stem, backend)

    report: dict[str, object] = {
        "filePath": file_path,
        "backend": backend,
        "runtimeFormat": entry.get("runtimeFormat"),
        "simulationId": simulation_id,
        "discoveryState": entry.get("discoveryState"),
        "loadedBeforeSmoke": bool(entry.get("isLoaded")),
    }

    manifest = call_tool(
        base_url,
        "validate_model_manifest",
        {"filePath": file_path},
        timeout=60,
        headers=headers,
    )
    report["manifestStatus"] = manifest["manifest"]["manifestStatus"]
    report["manifestQualificationState"] = manifest["manifest"]["qualificationState"]["state"]

    loaded = call_tool(
        base_url,
        "load_simulation",
        {"filePath": file_path, "simulationId": simulation_id},
        critical=True,
        timeout=180,
        headers=headers,
    )
    report["loadBackend"] = loaded.get("backend")
    report["scientificProfile"] = bool((loaded.get("capabilities") or {}).get("scientificProfile"))
    report["qualificationState"] = (
        (loaded.get("qualificationState") or {}).get("state")
        if isinstance(loaded.get("qualificationState"), dict)
        else None
    )

    submitted = call_tool(
        base_url,
        "run_simulation",
        {"simulationId": simulation_id, "runId": f"{simulation_id}-run"},
        critical=True,
        timeout=60,
        headers=headers,
    )
    job = poll_job(
        base_url,
        submitted["jobId"],
        timeout_seconds=timeout_seconds,
        headers=headers,
    )
    report["deterministicJobId"] = submitted["jobId"]
    report["deterministicStatus"] = job["status"]
    report["deterministicResultId"] = job.get("resultId")
    report["deterministicError"] = job.get("error")

    if job["status"] == "succeeded" and job.get("resultId"):
        result = call_tool(
            base_url,
            "get_results",
            {"resultsId": job["resultId"]},
            timeout=60,
            headers=headers,
        )
        report["seriesCount"] = len(result.get("series") or [])
        validation = ((result.get("metadata") or {}).get("validation") or {}).get("assessment") or {}
        report["resultDecision"] = validation.get("decision")

    capabilities = loaded.get("capabilities") or {}
    if include_population and backend == "rxode2" and capabilities.get("populationSimulation"):
        report["population"] = maybe_population_smoke(
            base_url,
            simulation_id,
            timeout_seconds=timeout_seconds,
            headers=headers,
        )

    return report


def summarize(results: list[dict]) -> dict:
    deterministic_ok = sum(1 for row in results if row.get("deterministicStatus") == "succeeded")
    population_runs = [row.get("population") for row in results if isinstance(row.get("population"), dict)]
    population_ok = sum(1 for row in population_runs if row.get("status") == "succeeded")
    return {
        "totalModels": len(results),
        "deterministicSucceeded": deterministic_ok,
        "deterministicFailed": len(results) - deterministic_ok,
        "populationAttempted": len(population_runs),
        "populationSucceeded": population_ok,
        "backends": sorted({str(row.get("backend")) for row in results}),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a discovery-first smoke test across workspace PBPK models through the live MCP API."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--search", default=None, help="Optional search filter passed to model discovery.")
    parser.add_argument(
        "--backend",
        action="append",
        default=[],
        help="Optional backend filter. Repeat for multiple values.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Optional maximum number of models to test.")
    parser.add_argument(
        "--include-population",
        action="store_true",
        help="Also run a small population smoke for rxode2 models that declare population support.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=300,
        help="Per-job timeout while polling deterministic or population jobs.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path to write the JSON smoke report.",
    )
    parser.add_argument(
        "--bearer-token",
        default=None,
        help="Optional bearer token for operator/admin access while running live smoke actions.",
    )
    parser.add_argument(
        "--auth-dev-secret",
        default=None,
        help="Optional local HS256 development secret used to mint an operator smoke token.",
    )
    parser.add_argument(
        "--auth-role",
        default="operator",
        help="Role to encode in the development smoke token when --auth-dev-secret is set.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    backends = set(args.backend) if args.backend else None
    auth_headers = build_auth_headers(
        bearer_token=args.bearer_token,
        auth_dev_secret=args.auth_dev_secret,
        auth_role=args.auth_role,
    )
    models = list_models(
        args.base_url,
        search=args.search,
        backends=backends,
        limit=args.limit,
        headers=auth_headers,
    )

    if not models:
        raise SystemExit("No runtime-supported models matched the requested filters.")

    results = []
    for entry in models:
        try:
            results.append(
                smoke_model(
                    args.base_url,
                    entry,
                    include_population=args.include_population,
                    timeout_seconds=args.timeout_seconds,
                    headers=auth_headers,
                )
            )
        except Exception as exc:  # pragma: no cover - operational smoke path
            results.append(
                {
                    "filePath": entry.get("filePath"),
                    "backend": entry.get("backend"),
                    "runtimeFormat": entry.get("runtimeFormat"),
                    "deterministicStatus": "failed-before-run",
                    "error": append_auth_hint(str(exc), has_auth_headers=bool(auth_headers)),
                }
            )

    payload = {
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "baseUrl": args.base_url,
        "authConfigured": bool(auth_headers),
        "filters": {
            "search": args.search,
            "backends": sorted(backends) if backends else [],
            "limit": args.limit,
            "includePopulation": args.include_population,
        },
        "summary": summarize(results),
        "results": results,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(output_path)
    print(json.dumps(payload["summary"], indent=2))
    return 0 if payload["summary"]["deterministicFailed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
