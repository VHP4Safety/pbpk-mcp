from __future__ import annotations

import sys
import unittest
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = WORKSPACE_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

try:  # pragma: no cover - exercised in the full contract env
    from mcp_bridge.routes.resources import router  # noqa: E402
except ModuleNotFoundError as exc:  # pragma: no cover - local lightweight envs
    missing_name = exc.name or ""
    if missing_name != "fastapi" and missing_name != "mcp" and not missing_name.startswith("mcp_bridge"):
        raise
    router = None


class PackagedResourceRouteTests(unittest.TestCase):
    @unittest.skipIf(router is None, "fastapi is required for packaged route import checks")
    def test_packaged_router_exposes_full_generic_resource_surface(self) -> None:
        paths = {route.path for route in router.routes}
        expected = {
            "/mcp/resources/models",
            "/mcp/resources/simulations",
            "/mcp/resources/parameters",
            "/mcp/resources/schemas",
            "/mcp/resources/schemas/{schema_id}",
            "/mcp/resources/capability-matrix",
            "/mcp/resources/contract-manifest",
        }
        self.assertTrue(expected.issubset(paths))


if __name__ == "__main__":
    unittest.main()
