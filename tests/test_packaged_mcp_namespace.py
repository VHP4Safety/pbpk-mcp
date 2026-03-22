from __future__ import annotations

import sys
import unittest
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = WORKSPACE_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

try:  # pragma: no cover - exercised in full contract env
    import mcp as mcp_namespace  # noqa: E402
except ModuleNotFoundError as exc:  # pragma: no cover - lightweight local envs
    missing_name = exc.name or ""
    if missing_name not in {"pydantic", "mcp_bridge"} and not missing_name.startswith("mcp"):
        raise
    mcp_namespace = None


class PackagedMcpNamespaceTests(unittest.TestCase):
    @unittest.skipIf(mcp_namespace is None, "packaged mcp namespace dependencies are not installed")
    def test_packaged_mcp_namespace_exports_generic_pbpk_tools(self) -> None:
        expected = {
            "DiscoverableModelModel",
            "LoadSimulationRequest",
            "LoadSimulationResponse",
            "discover_models",
            "get_results",
            "ingest_external_pbpk_bundle",
            "load_simulation",
        }
        for name in expected:
            self.assertTrue(hasattr(mcp_namespace, name), name)


if __name__ == "__main__":
    unittest.main()
