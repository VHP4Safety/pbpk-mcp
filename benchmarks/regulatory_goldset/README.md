# Regulatory Gold Set

This folder is the local staging area for external benchmark PBPK/PBK packages that are public, regulatory-relevant, and useful for benchmarking the MCP against a stricter documentation and reproducibility bar.

The source manifest is `benchmarks/regulatory_goldset/sources.lock.json`. Downloaded archives and extracted third-party contents are kept under `downloads/` and `extracted/`, which are intentionally ignored from git.

Why this folder exists:

- keep the repo's own MCP code separate from third-party benchmark packages
- make external benchmark retrieval reproducible
- record hashes and extraction metadata for traceability
- allow live benchmarking against real public-code PBPK models without pretending the repo authored them

Current benchmark intent:

- `tce_tsca_package`: primary regulatory completeness benchmark
- `epa_voc_template`: core reproducibility package covering dichloromethane, vinyl chloride, carbon tetrachloride, and methanol
- `epa_pfas_template`: modern transparency and reproducibility challenge set
- `pfos_ges_lac`: open PFOS model adjunct
- `two_butoxyethanol_reference`: tracked as a prose/documentation benchmark only until a clean public executable package is confirmed

Fetch and lock the current public artifacts with:

```bash
python scripts/fetch_regulatory_goldset.py --include-large
```

That command writes a local retrieval record to `benchmarks/regulatory_goldset/fetched.lock.json`.

Generate the tracked benchmark dossier from the lock files with:

```bash
python scripts/generate_regulatory_goldset_audit.py
python scripts/generate_regulatory_goldset_audit.py --check
```

Tracked outputs:

- `benchmarks/regulatory_goldset/regulatory_goldset_scorecard.json`
- `benchmarks/regulatory_goldset/regulatory_goldset_summary.md`
- `benchmarks/regulatory_goldset/regulatory_goldset_audit_manifest.json`

Confirmed local entry points after fetch:

- TCE TSCA package:
  - `benchmarks/regulatory_goldset/extracted/tce_tsca_package/tce_package_zip/TCE.1.2.3.3/TCE.evaluation.1.2.3.3.pop.model`
  - `benchmarks/regulatory_goldset/extracted/tce_tsca_package/tce_package_zip/TCE.1.2.3.3/TCE.risk5.1.2.3.3.pop.model`
  - `benchmarks/regulatory_goldset/extracted/tce_tsca_package/tce_package_zip/TCE.1.2.3.3/ModelResults.R`
  - `benchmarks/regulatory_goldset/extracted/tce_tsca_package/tce_package_zip/TCE.1.2.3.3/funcdefs.R`
  - `benchmarks/regulatory_goldset/extracted/tce_tsca_package/tce_package_zip/TCE.1.2.3.3/README.docx`

- VOC template:
  - `benchmarks/regulatory_goldset/extracted/epa_voc_template/voc_template_zip/Code_revised/PBPK_template.model`
  - `benchmarks/regulatory_goldset/extracted/epa_voc_template/voc_template_zip/Code_revised/run_template_model.R`
  - `benchmarks/regulatory_goldset/extracted/epa_voc_template/voc_template_zip/Code_revised/DCM_IRIS_scripts.R`
  - `benchmarks/regulatory_goldset/extracted/epa_voc_template/voc_template_zip/Code_revised/methanol_scripts.R`
  - `benchmarks/regulatory_goldset/extracted/epa_voc_template/voc_template_zip/Code_revised/Yoon_scripts.R`
- PFAS template:
  - `benchmarks/regulatory_goldset/extracted/epa_pfas_template/pfas_template_zip/Bernstein_PFAS_pbpk_template_code/PFAS_template.model`
  - `benchmarks/regulatory_goldset/extracted/epa_pfas_template/pfas_template_zip/Bernstein_PFAS_pbpk_template_code/run_PFAS_template_model.R`
- PFOS-Ges-Lac:
  - `benchmarks/regulatory_goldset/extracted/pfos_ges_lac/pfos_ges_lac_zip/PFOS-Ges-Lac-master/README.md`
  - `benchmarks/regulatory_goldset/extracted/pfos_ges_lac/pfos_ges_lac_zip/PFOS-Ges-Lac-master/Additional files/ModFit/Human/HMod.R`
  - `benchmarks/regulatory_goldset/extracted/pfos_ges_lac/pfos_ges_lac_zip/PFOS-Ges-Lac-master/Additional files/ModFit/Rat/RMod.R`

Current gap:

- `2-butoxyethanol` still remains documentation-only until a direct public executable or source-model package is confirmed.
