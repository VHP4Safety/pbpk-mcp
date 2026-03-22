from __future__ import annotations

import sys
import unittest
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = WORKSPACE_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

try:  # pragma: no cover - exercised in the full contract env
    from mcp_bridge.tools.registry import get_tool_registry  # noqa: E402
except ModuleNotFoundError as exc:  # pragma: no cover - lightweight local envs
    missing_name = exc.name or ""
    if missing_name not in {"pydantic", "mcp"} and not missing_name.startswith("mcp_bridge"):
        raise
    get_tool_registry = None


class PackagedToolRegistryTests(unittest.TestCase):
    @unittest.skipIf(get_tool_registry is None, "packaged tool registry dependencies are not installed")
    def test_packaged_registry_exposes_base_tool_surface(self) -> None:
        registry = get_tool_registry()
        expected = {
            "discover_models",
            "load_simulation",
            "list_parameters",
            "get_parameter_value",
            "set_parameter_value",
            "run_simulation",
            "get_job_status",
            "get_results",
            "calculate_pk_parameters",
            "run_population_simulation",
            "validate_model_manifest",
            "validate_simulation_request",
            "run_verification_checks",
            "get_population_results",
            "cancel_job",
            "run_sensitivity_analysis",
            "export_oecd_report",
            "ingest_external_pbpk_bundle",
        }
        self.assertTrue(expected.issubset(set(registry)))

    @unittest.skipIf(get_tool_registry is None, "packaged tool registry dependencies are not installed")
    def test_packaged_registry_uses_generic_pbpk_load_description(self) -> None:
        registry = get_tool_registry()
        self.assertEqual(
            registry["load_simulation"].description,
            "Load a PBPK model (.pkml or MCP-ready .R) into the active session registry.",
        )


if __name__ == "__main__":
    unittest.main()
