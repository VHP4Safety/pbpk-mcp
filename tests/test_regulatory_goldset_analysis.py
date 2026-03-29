from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = WORKSPACE_ROOT / "src"
SCRIPT_PATH = WORKSPACE_ROOT / "scripts" / "generate_regulatory_goldset_audit.py"
MODEL_MANIFEST_PATH = SRC_ROOT / "mcp_bridge" / "model_manifest.py"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mcp_bridge.benchmarking.regulatory_goldset import (  # noqa: E402
    analyze_regulatory_goldset,
    derive_manifest_benchmark_readiness,
    render_regulatory_goldset_summary,
)


spec = importlib.util.spec_from_file_location("pbpk_packaged_model_manifest_for_goldset", MODEL_MANIFEST_PATH)
if spec is None or spec.loader is None:  # pragma: no cover - import guard
    raise RuntimeError(f"Unable to load packaged module from {MODEL_MANIFEST_PATH}")
module = importlib.util.module_from_spec(spec)
sys.modules.setdefault("pbpk_packaged_model_manifest_for_goldset", module)
spec.loader.exec_module(module)
validate_model_manifest = module.validate_model_manifest

REFERENCE_MODEL = (
    WORKSPACE_ROOT / "var" / "models" / "rxode2" / "reference_compound" / "reference_compound_population_rxode2_model.R"
)
TRACKED_SCORECARD = WORKSPACE_ROOT / "benchmarks" / "regulatory_goldset" / "regulatory_goldset_scorecard.json"
TRACKED_SUMMARY = WORKSPACE_ROOT / "benchmarks" / "regulatory_goldset" / "regulatory_goldset_summary.md"


class RegulatoryGoldsetAnalysisTests(unittest.TestCase):
    def _analysis_with_reference_model(self) -> dict:
        analysis = analyze_regulatory_goldset()
        manifest = validate_model_manifest(REFERENCE_MODEL)["manifest"]
        analysis["referenceModelComparisons"] = [
            {
                "id": "reference_workspace_model",
                "title": "Workspace synthetic reference model",
                "modelPath": "var/models/rxode2/reference_compound/reference_compound_population_rxode2_model.R",
                "qualificationState": manifest["qualificationState"]["state"],
                "regulatoryBenchmarkReadiness": derive_manifest_benchmark_readiness(manifest),
            }
        ]
        return analysis

    def test_analysis_reports_expected_source_ids(self) -> None:
        analysis = analyze_regulatory_goldset()

        source_ids = [item["id"] for item in analysis["sources"]]
        self.assertEqual(
            source_ids,
            [
                "tce_tsca_package",
                "epa_voc_template",
                "epa_pfas_template",
                "pfos_ges_lac",
                "two_butoxyethanol_reference",
            ],
        )
        self.assertEqual(
            analysis["benchmarkBar"]["strictCoreSourceIds"],
            ["tce_tsca_package", "epa_voc_template"],
        )

    def test_analysis_scores_strict_core_and_documentation_reference_conservatively(self) -> None:
        analysis = analyze_regulatory_goldset()
        sources = {item["id"]: item for item in analysis["sources"]}

        tce = sources["tce_tsca_package"]["scorecard"]
        self.assertEqual(tce["overallTier"], "benchmark-grade")
        self.assertEqual(tce["dimensionCounts"]["present"], 8)

        butoxy = sources["two_butoxyethanol_reference"]["scorecard"]
        self.assertEqual(butoxy["overallTier"], "documentation-only-reference")
        self.assertEqual(butoxy["dimensionCounts"]["partial"], 1)
        self.assertEqual(butoxy["dimensionCounts"]["notApplicable"], 7)

    def test_reference_model_benchmark_readiness_stays_advisory_and_non_regulatory(self) -> None:
        manifest = validate_model_manifest(REFERENCE_MODEL)["manifest"]
        readiness = derive_manifest_benchmark_readiness(manifest)

        self.assertTrue(readiness["advisoryOnly"])
        self.assertEqual(readiness["modelResemblance"], "research-example")
        self.assertEqual(readiness["overallStatus"], "below-benchmark-bar")
        self.assertIn("parameterProvenanceDepth", readiness["partialDimensions"])
        self.assertIn("publicTraceabilityHashability", readiness["partialDimensions"])
        self.assertEqual(readiness["missingDimensions"], [])
        self.assertTrue(readiness["benchmarkBarSource"]["sourceManifestSha256"])
        self.assertTrue(readiness["benchmarkBarSource"]["fetchedLockSha256"])
        self.assertIn(
            readiness["benchmarkBarSource"]["sourceResolution"],
            {"direct-lock-files", "audit-manifest-fallback", "packaged-contract-fallback"},
        )
        self.assertTrue(readiness["recommendedNextArtifacts"])
        top_gap = readiness["prioritizedGaps"][0]
        self.assertEqual(top_gap["dimensionId"], "parameterProvenanceDepth")
        self.assertTrue(top_gap["evaluatedFrom"])
        self.assertTrue(top_gap["recommendedNextArtifacts"])
        self.assertIn("tce_tsca_package", top_gap["benchmarkExampleIds"])

    def test_tracked_scorecard_and_summary_match_regenerated_outputs(self) -> None:
        analysis = self._analysis_with_reference_model()

        self.assertEqual(
            json.loads(TRACKED_SCORECARD.read_text(encoding="utf-8")),
            analysis,
        )
        self.assertEqual(
            TRACKED_SUMMARY.read_text(encoding="utf-8"),
            render_regulatory_goldset_summary(analysis),
        )
        self.assertIn("## Internal Non-Benchmark Use-Case Comparison", TRACKED_SUMMARY.read_text(encoding="utf-8"))
        self.assertIn("internal MCP use case", TRACKED_SUMMARY.read_text(encoding="utf-8"))

    def test_script_generates_and_verifies_hash_linked_audit_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pbpk_goldset_audit_") as temp_dir:
            root = Path(temp_dir)
            scorecard = root / "scorecard.json"
            summary = root / "summary.md"
            manifest = root / "audit_manifest.json"

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--scorecard-output",
                    str(scorecard),
                    "--summary-output",
                    str(summary),
                    "--manifest-output",
                    str(manifest),
                ],
                cwd=str(WORKSPACE_ROOT),
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            generated_manifest = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(
                generated_manifest["sourceManifest"]["relativePath"],
                "benchmarks/regulatory_goldset/sources.lock.json",
            )
            self.assertEqual(
                generated_manifest["fetchedLock"]["relativePath"],
                "benchmarks/regulatory_goldset/fetched.lock.json",
            )
            self.assertEqual(len(generated_manifest["trackedOutputs"]), 2)

            verified = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--verify-only",
                    "--manifest-output",
                    str(manifest),
                ],
                cwd=str(WORKSPACE_ROOT),
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)
            verification_payload = json.loads(verified.stdout)
            self.assertEqual(verification_payload["status"], "passed")


if __name__ == "__main__":
    unittest.main()
