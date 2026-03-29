from __future__ import annotations

import json
import unittest
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = WORKSPACE_ROOT / "benchmarks" / "regulatory_goldset" / "sources.lock.json"


class RegulatoryGoldsetManifestTests(unittest.TestCase):
    def test_source_manifest_has_expected_core_sources(self) -> None:
        payload = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(payload["formatVersion"], 1)
        sources = {entry["id"]: entry for entry in payload["sources"]}

        self.assertIn("tce_tsca_package", sources)
        self.assertIn("epa_voc_template", sources)
        self.assertIn("epa_pfas_template", sources)
        self.assertIn("pfos_ges_lac", sources)
        self.assertIn("two_butoxyethanol_reference", sources)

        self.assertEqual(sources["tce_tsca_package"]["status"], "retrievable")
        self.assertEqual(sources["epa_voc_template"]["status"], "retrievable")
        self.assertEqual(sources["epa_pfas_template"]["status"], "retrievable")
        self.assertEqual(sources["pfos_ges_lac"]["status"], "retrievable")
        self.assertEqual(sources["two_butoxyethanol_reference"]["status"], "unresolved")

    def test_voc_template_covers_strict_core_solvents(self) -> None:
        payload = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        sources = {entry["id"]: entry for entry in payload["sources"]}
        coverage = set(sources["epa_voc_template"]["coverageModels"])

        self.assertTrue(
            {"dichloromethane", "vinyl chloride", "carbon tetrachloride", "methanol"}.issubset(coverage)
        )

