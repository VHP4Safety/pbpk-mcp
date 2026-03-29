#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = WORKSPACE_ROOT / "output" / "review" / "pbpk_mcp_external_review_repoconcat.txt"

EXCLUDED_DIR_NAMES = {
    ".git",
    ".venv",
    ".pytest_cache",
    ".mypy_cache",
    "__pycache__",
    "build",
    "dist",
    "tmp",
    "output",
    "var",
}
EXCLUDED_PATH_PREFIXES = (
    "benchmarks/regulatory_goldset/downloads/",
    "benchmarks/regulatory_goldset/extracted/",
    "src/mcp_bridge.egg-info/",
)
EXCLUDED_SUFFIXES = {
    ".7z",
    ".csv",
    ".doc",
    ".docx",
    ".gif",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".tar",
    ".tgz",
    ".whl",
    ".zip",
}
TEXT_SUFFIXES = {
    ".c",
    ".cfg",
    ".css",
    ".dockerfile",
    ".env",
    ".example",
    ".gitignore",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".r",
    ".rst",
    ".sh",
    ".sql",
    ".svg",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
TEXT_FILENAMES = {
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "Dockerfile",
    "LICENSE",
    "MANIFEST.in",
    "Makefile",
    "README.md",
    "SECURITY.md",
}


def _is_excluded(relative_path: str) -> bool:
    parts = Path(relative_path).parts
    if any(part in EXCLUDED_DIR_NAMES for part in parts[:-1]):
        return True
    return any(relative_path.startswith(prefix) for prefix in EXCLUDED_PATH_PREFIXES)


def _looks_textual(path: Path) -> bool:
    if path.name in TEXT_FILENAMES:
        return True
    suffix = path.suffix.lower()
    if suffix in EXCLUDED_SUFFIXES:
        return False
    if suffix in TEXT_SUFFIXES:
        return True
    try:
        chunk = path.read_bytes()[:4096]
    except OSError:
        return False
    if b"\x00" in chunk:
        return False
    try:
        chunk.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def iter_concat_paths(root: Path) -> list[Path]:
    selected: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root).as_posix()
        if _is_excluded(relative_path):
            continue
        if not _looks_textual(path):
            continue
        selected.append(path)
    return selected


def render_repo_concat(root: Path, paths: list[Path]) -> str:
    lines: list[str] = [
        "# PBPK MCP Repository Concat",
        "",
        f"Root: {root}",
        f"Included text files: {len(paths)}",
        "",
        "## Included Files",
        "",
    ]
    lines.extend(f"- {path.relative_to(root).as_posix()}" for path in paths)
    lines.extend(["", "## File Contents", ""])
    for path in paths:
        relative_path = path.relative_to(root).as_posix()
        lines.extend(
            [
                f"===== BEGIN FILE: {relative_path} =====",
                path.read_text(encoding="utf-8"),
                f"===== END FILE: {relative_path} =====",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a text-only repository concat for external review.")
    parser.add_argument(
        "--root",
        type=Path,
        default=WORKSPACE_ROOT,
        help="Repository root to snapshot.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output .txt file.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    output_path = args.output.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    paths = iter_concat_paths(root)
    output_path.write_text(render_repo_concat(root, paths), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
