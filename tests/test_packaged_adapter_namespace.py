from __future__ import annotations

import sys
import unittest
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = WORKSPACE_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

try:  # pragma: no cover - exercised in full contract env
    from mcp_bridge import adapter as adapter_namespace  # noqa: E402
except ModuleNotFoundError as exc:  # pragma: no cover - lightweight local envs
    missing_name = exc.name or ""
    if missing_name not in {"pydantic", "mcp"} and not missing_name.startswith("mcp_bridge"):
        raise
    adapter_namespace = None


class PackagedAdapterNamespaceTests(unittest.TestCase):
    @unittest.skipIf(adapter_namespace is None, "packaged adapter namespace dependencies are not installed")
    def test_packaged_adapter_namespace_exports_subprocess_adapter(self) -> None:
        expected = {
            "AdapterConfig",
            "AdapterError",
            "AdapterErrorCode",
            "OspsuiteAdapter",
            "SubprocessOspsuiteAdapter",
        }
        for name in expected:
            self.assertTrue(hasattr(adapter_namespace, name), name)


if __name__ == "__main__":
    unittest.main()
