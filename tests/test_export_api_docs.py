from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ExportApiDocsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]
        self.script = self.repo_root / "scripts" / "export_api_docs.py"

    def test_help_succeeds_in_dev_environment(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(self.script), "--help"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"stdout:\n{completed.stdout}\n\nstderr:\n{completed.stderr}",
        )
        self.assertIn("Export OpenAPI and MCP tool schemas", completed.stdout)

    def test_export_includes_patch_extended_tool_schemas(self) -> None:
        if importlib.util.find_spec("pydantic") is None:
            self.skipTest("pydantic is required for export_api_docs schema generation")
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            contracts_dir = tmp / "contracts"
            schemas_dir = tmp / "schemas"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(self.script),
                    "--contracts-dir",
                    str(contracts_dir),
                    "--schemas-dir",
                    str(schemas_dir),
                ],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                completed.returncode,
                0,
                msg=f"stdout:\n{completed.stdout}\n\nstderr:\n{completed.stderr}",
            )
            self.assertTrue((contracts_dir / "openapi.json").exists())
            self.assertTrue((schemas_dir / "discover_models-request.json").exists())
            self.assertTrue((schemas_dir / "validate_model_manifest-response.json").exists())


if __name__ == "__main__":
    unittest.main()
