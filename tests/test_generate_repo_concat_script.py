from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = WORKSPACE_ROOT / "scripts" / "generate_repo_concat.py"

spec = importlib.util.spec_from_file_location("pbpk_generate_repo_concat_test", SCRIPT_PATH)
if spec is None or spec.loader is None:  # pragma: no cover - import guard
    raise RuntimeError(f"Unable to load repo concat generator from {SCRIPT_PATH}")
module = importlib.util.module_from_spec(spec)
sys.modules.setdefault("pbpk_generate_repo_concat_test", module)
spec.loader.exec_module(module)

iter_concat_paths = module.iter_concat_paths
render_repo_concat = module.render_repo_concat


class GenerateRepoConcatScriptTests(unittest.TestCase):
    def test_iter_concat_paths_filters_runtime_and_binary_content(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pbpk_repo_concat_") as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("readme\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "note.md").write_text("note\n", encoding="utf-8")
            (root / "output").mkdir()
            (root / "output" / "report.txt").write_text("skip\n", encoding="utf-8")
            (root / "var").mkdir()
            (root / "var" / "state.json").write_text("skip\n", encoding="utf-8")
            (root / "tmp").mkdir()
            (root / "tmp" / "scratch.txt").write_text("skip\n", encoding="utf-8")
            (root / "benchmarks" / "regulatory_goldset" / "downloads").mkdir(parents=True)
            (root / "benchmarks" / "regulatory_goldset" / "downloads" / "archive.zip").write_bytes(b"zip")
            (root / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")

            selected = [path.relative_to(root).as_posix() for path in iter_concat_paths(root)]

        self.assertEqual(selected, ["README.md", "docs/note.md"])

    def test_render_repo_concat_includes_inventory_and_file_delimiters(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pbpk_repo_concat_") as temp_dir:
            root = Path(temp_dir)
            first = root / "README.md"
            second = root / "docs" / "note.md"
            second.parent.mkdir()
            first.write_text("readme\n", encoding="utf-8")
            second.write_text("note\n", encoding="utf-8")

            rendered = render_repo_concat(root, [first, second])

        self.assertIn("# PBPK MCP Repository Concat", rendered)
        self.assertIn("- README.md", rendered)
        self.assertIn("- docs/note.md", rendered)
        self.assertIn("===== BEGIN FILE: README.md =====", rendered)
        self.assertIn("===== END FILE: docs/note.md =====", rendered)


if __name__ == "__main__":
    unittest.main()
