#!/usr/bin/env python3
from __future__ import annotations

import importlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path


CHECK_SNIPPET = r"""
from __future__ import annotations

import json
import os
from importlib import metadata
from pathlib import Path

from mcp_bridge.contract import (
    capability_matrix_document,
    contract_manifest_document,
    schema_documents,
    schema_examples,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


repo_root = Path(os.environ["PBPK_CONTRACT_REPO_ROOT"])
schema_root = repo_root / "schemas"
examples_root = schema_root / "examples"
expected_capability_matrix = load_json(
    repo_root / "docs" / "architecture" / "capability_matrix.json"
)
expected_contract_manifest = load_json(
    repo_root / "docs" / "architecture" / "contract_manifest.json"
)
expected_schema_documents = {
    path.stem: load_json(path) for path in sorted(schema_root.glob("*.v*.json"))
}
expected_schema_examples = {
    path.name.replace(".example.json", ""): load_json(path)
    for path in sorted(examples_root.glob("*.json"))
}

if capability_matrix_document() != expected_capability_matrix:
    raise SystemExit("Installed package capability matrix does not match published JSON.")
if contract_manifest_document() != expected_contract_manifest:
    raise SystemExit("Installed package contract manifest does not match published JSON.")
if schema_documents() != expected_schema_documents:
    raise SystemExit("Installed package schema documents do not match published JSON.")
if schema_examples() != expected_schema_examples:
    raise SystemExit("Installed package schema examples do not match published JSON.")

print("Installed package contract check passed.")
print(f"- mcp-bridge {metadata.version('mcp-bridge')}")
print(f"- contract manifest schemas {expected_contract_manifest['artifactCounts']['schemas']}")
print(f"- schemas {len(expected_schema_documents)}")
print(f"- examples {len(expected_schema_examples)}")
"""


def _run(command: list[str], *, env: dict[str, str] | None = None, cwd: Path | None = None) -> None:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd) if cwd is not None else None,
    )
    if completed.returncode == 0:
        if completed.stdout.strip():
            print(completed.stdout.strip())
        return

    if completed.stdout.strip():
        print(completed.stdout.strip(), file=sys.stderr)
    if completed.stderr.strip():
        print(completed.stderr.strip(), file=sys.stderr)
    raise SystemExit(completed.returncode)


def main() -> int:
    workspace_root = Path(__file__).resolve().parents[1]
    missing_build_modules: list[tuple[str, str]] = []

    for module_name, purpose in (
        ("setuptools.build_meta", "local wheel build backend"),
        ("pip", "local package installer"),
    ):
        try:
            importlib.import_module(module_name)
        except Exception:
            missing_build_modules.append((module_name, purpose))

    if missing_build_modules:
        print("Installed package contract check failed.", file=sys.stderr)
        print("", file=sys.stderr)
        print(
            "The following Python modules are required to validate the non-editable install boundary:",
            file=sys.stderr,
        )
        for module_name, purpose in missing_build_modules:
            print(f"- {module_name}: {purpose}", file=sys.stderr)
        print("", file=sys.stderr)
        print(
            "Install the project dependencies first, for example with `python -m pip install -e '.[dev]'`.",
            file=sys.stderr,
        )
        return 1

    with tempfile.TemporaryDirectory(prefix="pbpk_installed_contract_") as temp_dir:
        target_root = Path(temp_dir) / "site-packages"
        target_root.mkdir(parents=True, exist_ok=True)

        _run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-deps",
                "--no-build-isolation",
                "--target",
                str(target_root),
                str(workspace_root),
            ]
        )

        env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        env["PBPK_CONTRACT_REPO_ROOT"] = str(workspace_root)
        env["PYTHONPATH"] = str(target_root)

        _run([sys.executable, "-c", CHECK_SNIPPET], env=env, cwd=Path(temp_dir))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
