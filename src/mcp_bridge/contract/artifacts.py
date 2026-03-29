from __future__ import annotations

import json

_CAPABILITY_MATRIX_JSON = r"""
{
  "contractVersion": "pbpk-mcp.v1",
  "entries": [
    {
      "backend": "ospsuite",
      "catalogDiscovery": "yes",
      "deterministicExecution": "yes",
      "deterministicResults": "yes",
      "id": "pkml-transfer-file",
      "label": "PK-Sim / MoBi transfer file (.pkml)",
      "loadIntoSession": "yes",
      "notes": [
        "Optional sidecars can enrich qualification metadata and parameter provenance.",
        "Population simulation is not exposed as a generic OSPSuite .pkml capability in the current public contract."
      ],
      "oecdDossierExport": "yes",
      "policy": "runtime-supported",
      "populationExecution": "no",
      "populationResults": "no",
      "requestValidation": "yes",
      "runtimeFormat": "pkml",
      "staticManifestValidation": "yes",
      "verification": "yes"
    },
    {
      "backend": "rxode2",
      "catalogDiscovery": "yes",
      "deterministicExecution": "yes",
      "deterministicResults": "yes",
      "id": "contract-complete-r-model",
      "label": "Contract-complete MCP-ready R model (.R)",
      "loadIntoSession": "yes",
      "notes": [
        "Population workflows depend on the model declaring the population capability and implementing the required runtime hook.",
        "Richer OECD-oriented evidence can be supplied through module hooks and companion bundles."
      ],
      "oecdDossierExport": "yes",
      "policy": "runtime-supported",
      "populationExecution": "conditional",
      "populationResults": "conditional",
      "requestValidation": "yes",
      "runtimeFormat": "r",
      "staticManifestValidation": "yes",
      "verification": "yes"
    },
    {
      "backend": "rxode2",
      "catalogDiscovery": "yes",
      "deterministicExecution": "no",
      "deterministicResults": "no",
      "id": "discoverable-incomplete-r-model",
      "label": "Discoverable but incomplete R module (.R)",
      "loadIntoSession": "no",
      "notes": [
        "An .R file may still appear in discovery before it satisfies the expected PBPK MCP hook contract.",
        "validate_model_manifest is the intended pre-load surface for diagnosing missing hooks and dossier gaps."
      ],
      "oecdDossierExport": "no",
      "policy": "discoverable-but-not-runnable",
      "populationExecution": "no",
      "populationResults": "no",
      "requestValidation": "no",
      "runtimeFormat": "r",
      "staticManifestValidation": "yes",
      "verification": "no"
    },
    {
      "backend": null,
      "catalogDiscovery": "no",
      "deterministicExecution": "no",
      "deterministicResults": "no",
      "id": "pksim5-project",
      "label": "PK-Sim project file (.pksim5)",
      "loadIntoSession": "no",
      "notes": [
        "Direct .pksim5 loading is rejected early.",
        "Export the project to .pkml before runtime use."
      ],
      "oecdDossierExport": "no",
      "policy": "conversion-only",
      "populationExecution": "no",
      "populationResults": "no",
      "requestValidation": "no",
      "runtimeFormat": "pksim5",
      "staticManifestValidation": "no",
      "verification": "no"
    },
    {
      "backend": null,
      "catalogDiscovery": "no",
      "deterministicExecution": "no",
      "deterministicResults": "no",
      "id": "berkeley-madonna-source",
      "label": "Berkeley Madonna source model (.mmd)",
      "loadIntoSession": "no",
      "notes": [
        "Direct .mmd loading is rejected early.",
        "Convert the model to .pkml or an MCP-ready .R module before runtime use."
      ],
      "oecdDossierExport": "no",
      "policy": "conversion-only",
      "populationExecution": "no",
      "populationResults": "no",
      "requestValidation": "no",
      "runtimeFormat": "mmd",
      "staticManifestValidation": "no",
      "verification": "no"
    }
  ],
  "statusLegend": {
    "conditional": "Supported only when the model or request satisfies declared capability conditions.",
    "no": "Not part of the published workflow for this input class.",
    "yes": "Supported directly by the published PBPK MCP workflow."
  }
}
"""

_CONTRACT_MANIFEST_JSON = r"""
{
  "artifactClasses": {
    "legacy-excluded": {
      "description": "Historical or non-PBPK-side artifacts that are intentionally outside pbpk-mcp.v1."
    },
    "normative": {
      "description": "Machine-readable artifacts that define the published pbpk-mcp.v1 contract."
    },
    "supporting": {
      "description": "Human-facing or release-facing artifacts that support the contract without defining it."
    }
  },
  "artifactCounts": {
    "examples": 8,
    "schemas": 8,
    "supporting": 33
  },
  "capabilityMatrix": {
    "classification": "normative",
    "relativePath": "docs/architecture/capability_matrix.json",
    "sha256": "bdc2169d99343f38c5a7dea91306d46704104d488442e4161812dfb63ac6da03"
  },
  "contractManifest": {
    "classification": "normative",
    "relativePath": "docs/architecture/contract_manifest.json"
  },
  "contractVersion": "pbpk-mcp.v1",
  "id": "pbpk-contract-manifest.v1",
  "legacyArtifactPolicy": [
    {
      "classification": "legacy-excluded",
      "reason": "Legacy literature extraction schema retained outside the PBPK-side pbpk-mcp.v1 object family.",
      "relativePath": "schemas/extraction-record.json"
    }
  ],
  "legacyArtifactsExcluded": [
    "schemas/extraction-record.json"
  ],
  "resourceEndpoints": {
    "capabilityMatrix": "/mcp/resources/capability-matrix",
    "contractManifest": "/mcp/resources/contract-manifest",
    "releaseBundleManifest": "/mcp/resources/release-bundle-manifest",
    "schemaCatalog": "/mcp/resources/schemas"
  },
  "schemas": [
    {
      "classification": "normative",
      "exampleRelativePath": "schemas/examples/assessmentContext.v1.example.json",
      "exampleSha256": "774828884b6705892187768b505b1c3f5e36ebe83d2a2f570847145297bf3d0c",
      "relativePath": "schemas/assessmentContext.v1.json",
      "schemaId": "assessmentContext.v1",
      "sha256": "2849beb31892bce04753f732e5bf538595a2a060b9c2c25d291f317640eda20c"
    },
    {
      "classification": "normative",
      "exampleRelativePath": "schemas/examples/berInputBundle.v1.example.json",
      "exampleSha256": "64399ce683596314bf9d32df20f8c42ffa02673830f477e7e78ea3a0bfa845ff",
      "relativePath": "schemas/berInputBundle.v1.json",
      "schemaId": "berInputBundle.v1",
      "sha256": "a46c842bfc6dd6f1e1ef4d0f5f65371182c830d478cafae3eef9a599899e9cae"
    },
    {
      "classification": "normative",
      "exampleRelativePath": "schemas/examples/internalExposureEstimate.v1.example.json",
      "exampleSha256": "559f0118d012d14275141d11dbb0d968ed74a0ce39002ad1094bfe87a034009e",
      "relativePath": "schemas/internalExposureEstimate.v1.json",
      "schemaId": "internalExposureEstimate.v1",
      "sha256": "830b2cf73661b67dfd0e8493c5e410e276555c05f71221db8e36722bf6cb4857"
    },
    {
      "classification": "normative",
      "exampleRelativePath": "schemas/examples/pbpkQualificationSummary.v1.example.json",
      "exampleSha256": "66bd8b255e52c125e72b18eaf36ea49ed95d0af5c6f4a050d483b5bb0e3697eb",
      "relativePath": "schemas/pbpkQualificationSummary.v1.json",
      "schemaId": "pbpkQualificationSummary.v1",
      "sha256": "20eb7f265c12d406d453614e8c3a704d19fb8ae6527390d9a9ed6f401cdec2d3"
    },
    {
      "classification": "normative",
      "exampleRelativePath": "schemas/examples/pointOfDepartureReference.v1.example.json",
      "exampleSha256": "11185de168163409fb9c22dcfbf7b10c322ff8eddf521d02d1842ee7c4994dbc",
      "relativePath": "schemas/pointOfDepartureReference.v1.json",
      "schemaId": "pointOfDepartureReference.v1",
      "sha256": "58a0e04e48ed716637aae12e972e0f92b858ff6f0cfde918942b97a1daa695aa"
    },
    {
      "classification": "normative",
      "exampleRelativePath": "schemas/examples/uncertaintyHandoff.v1.example.json",
      "exampleSha256": "ef372636efb1a13dd26151618eaf440bbde90fad5e600b0ab13945187fb0a03c",
      "relativePath": "schemas/uncertaintyHandoff.v1.json",
      "schemaId": "uncertaintyHandoff.v1",
      "sha256": "4547fbcd1014e439abbf5f98ce1e19e0320be8e81eb30102d6a0099fce32d86e"
    },
    {
      "classification": "normative",
      "exampleRelativePath": "schemas/examples/uncertaintyRegisterReference.v1.example.json",
      "exampleSha256": "652fd3674c30263e5da3e299418327ec4d06811f75f661deff63b2d152b1841f",
      "relativePath": "schemas/uncertaintyRegisterReference.v1.json",
      "schemaId": "uncertaintyRegisterReference.v1",
      "sha256": "38808ece8fa55cc3b233f5b3966d480616983d953d0f8f7290cb6191e7222bb6"
    },
    {
      "classification": "normative",
      "exampleRelativePath": "schemas/examples/uncertaintySummary.v1.example.json",
      "exampleSha256": "9cb008aadd06a2fb4f12dae6ea46023e6f30f30011d851ad76ad9f0f2c9bd181",
      "relativePath": "schemas/uncertaintySummary.v1.json",
      "schemaId": "uncertaintySummary.v1",
      "sha256": "ea1f95e8bd2786468c0a946f0c2dbbba0045411024292affb052efd33c9e00c3"
    }
  ],
  "supportingArtifacts": [
    {
      "classification": "supporting",
      "relativePath": "benchmarks/regulatory_goldset/README.md",
      "role": "regulatory benchmark corpus guide",
      "sha256": "3da4d18c8a96049148b26bcd17f37e14e853481b3974e21b4ab8a8dcd9baef14"
    },
    {
      "classification": "supporting",
      "relativePath": "benchmarks/regulatory_goldset/sources.lock.json",
      "role": "regulatory gold-set source lock",
      "sha256": "ba24143cfe7ddd976779d7c60d24754b35f8ecf0d361e15c8ad247e488af337b"
    },
    {
      "classification": "supporting",
      "relativePath": "benchmarks/regulatory_goldset/fetched.lock.json",
      "role": "regulatory gold-set fetch lock",
      "sha256": "949db5491f40406ab4a0fc185952795bb88f1243ac5c4a3ead1b4fda7661ddca"
    },
    {
      "classification": "supporting",
      "relativePath": "benchmarks/regulatory_goldset/regulatory_goldset_scorecard.json",
      "role": "regulatory gold-set scorecard",
      "sha256": "212987469243e7b32a06f41cdab74c21b931f4540b12ab6a492baeff6dcd967a"
    },
    {
      "classification": "supporting",
      "relativePath": "benchmarks/regulatory_goldset/regulatory_goldset_summary.md",
      "role": "regulatory gold-set benchmark summary",
      "sha256": "9bb0eb45eb571d57a30622665b8caeeaaca0e31114edf83554facbe11083d944"
    },
    {
      "classification": "supporting",
      "relativePath": "benchmarks/regulatory_goldset/regulatory_goldset_audit_manifest.json",
      "role": "regulatory gold-set audit manifest",
      "sha256": "21af57a4b41416ab79cfa86bd58c4582f5834218adad033b8c4b3bb65967931e"
    },
    {
      "classification": "supporting",
      "relativePath": "docs/architecture/capability_matrix.md",
      "role": "human-readable capability guide",
      "sha256": "ed587abf32181ca8cd530c73b6deb64655cb34473eee9b1cc450becc8a237589"
    },
    {
      "classification": "supporting",
      "relativePath": "docs/architecture/mcp_payload_conventions.md",
      "role": "payload contract reference",
      "sha256": "2bd79754995a99b2f7c679b336a5b9e4e91373714d3e64ddc933da4edcd0ee02"
    },
    {
      "classification": "supporting",
      "relativePath": "docs/architecture/exposure_led_ngra_role.md",
      "role": "exposure-led NGRA boundary guide",
      "sha256": "25a56d32680e62e8bd99d995c00606fa31e815f0655a31c7bc227122bf298e5a"
    },
    {
      "classification": "supporting",
      "relativePath": "docs/architecture/release_bundle_manifest.json",
      "role": "whole release bundle hash inventory",
      "sha256": "688031a03631e0281bb83a4b22c52e6ba03548ce0a2c7508e78941fe30d6846f"
    },
    {
      "classification": "supporting",
      "relativePath": "docs/hardening_migration_notes.md",
      "role": "hardening migration notes",
      "sha256": "a6b09925902b20e45f15c7e0a703468162cef5bbf1a966eee90aff397130fa88"
    },
    {
      "classification": "supporting",
      "relativePath": "docs/pbpk_model_onboarding_checklist.md",
      "role": "PBPK model onboarding checklist",
      "sha256": "c3ac775a33d357fceac2d74ecd65d1e7d9f3dafa2166fa71f969217b02d56185"
    },
    {
      "classification": "supporting",
      "relativePath": "docs/github_publication_checklist.md",
      "role": "publication checklist",
      "sha256": "7e54a09ce8d5055dc940d85aebae60074681ad01d41bcee7c16c8a3e7e6af75b"
    },
    {
      "classification": "supporting",
      "relativePath": "docs/pbk_reviewer_signoff_checklist.md",
      "role": "PBK reviewer sign-off checklist",
      "sha256": "12c8ff065ae36a0ae1f3a94b635d6635ad2b237ecf4755eb2ab2a457dccb336c"
    },
    {
      "classification": "supporting",
      "relativePath": "docs/post_release_audit_plan.md",
      "role": "post-release audit plan",
      "sha256": "cfedfabd7a0943f94b8afba4d2d0f9b85c8b9225f955bea7e3c331bd316583f5"
    },
    {
      "classification": "supporting",
      "relativePath": "schemas/README.md",
      "role": "schema usage guide",
      "sha256": "2f58bea343ec1a49d9c25dbaadc3d36bfa87cebb483f280e776034d0927f4339"
    },
    {
      "classification": "supporting",
      "relativePath": "scripts/check_distribution_artifacts.py",
      "role": "distribution artifact validation script",
      "sha256": "12934c81c14241f6fb28705c97e9eb443e29c75b5c71005cc0dbb394c57f6084"
    },
    {
      "classification": "supporting",
      "relativePath": "scripts/check_release_metadata.py",
      "role": "release metadata consistency check",
      "sha256": "971bf6472a31e184ac1e55fc17886a69154dd83ac9adb7e1cfef0579ebaf896b"
    },
    {
      "classification": "supporting",
      "relativePath": "scripts/check_installed_package_contract.py",
      "role": "installed package contract validation script",
      "sha256": "e63b48f3f0b7d0f5093f31f157e1b656c62a207b23021f3dd127801094a177ea"
    },
    {
      "classification": "supporting",
      "relativePath": "scripts/check_runtime_contract_env.py",
      "role": "contract dependency preflight script",
      "sha256": "82cbd13b4c7c4fef29b06cac4d9552f7db236985c1e7c348391e7f929b35d9a0"
    },
    {
      "classification": "supporting",
      "relativePath": "scripts/release_readiness_check.py",
      "role": "live release readiness gate",
      "sha256": "0b91d767dc00cfa0df83773d4082f2918278dd3b27783b4485863754df42f225"
    },
    {
      "classification": "supporting",
      "relativePath": "scripts/wait_for_runtime_ready.py",
      "role": "runtime readiness probe",
      "sha256": "fa18ce884ba790f7d208fde156709b2735e4678e68dc75461a4cbe04569364be"
    },
    {
      "classification": "supporting",
      "relativePath": "scripts/workspace_model_smoke.py",
      "role": "workspace live smoke script",
      "sha256": "c9f201b0958028473a5434a8704130492021f7fffc8cb42e28b3b9d357257684"
    },
    {
      "classification": "supporting",
      "relativePath": "scripts/generate_contract_artifacts.py",
      "role": "contract artifact generator",
      "sha256": "d279e12ce72fc682088403fb515460990e90e2311752d6573d42aa0ce0f606ee"
    },
    {
      "classification": "supporting",
      "relativePath": "scripts/generate_regulatory_goldset_audit.py",
      "role": "regulatory gold-set audit generator",
      "sha256": "ef244652dad5862ad46c25e1dd6b844a148389dcf7697c242577b3b268e6a0e2"
    },
    {
      "classification": "supporting",
      "relativePath": "src/mcp_bridge/trust_surface.py",
      "role": "thin-client trust-surface contract helper",
      "sha256": "bd41076e5234f4f584deefaf8174162e0e482fba53a8f3c63ea7c0efa01d42d1"
    },
    {
      "classification": "supporting",
      "relativePath": "src/mcp_bridge/benchmarking/regulatory_goldset.py",
      "role": "regulatory gold-set benchmark helper",
      "sha256": "6760efa0d01df3e79250c095d6d07d59e2bff3dd3868f8f0740728dc1eaa6420"
    },
    {
      "classification": "supporting",
      "relativePath": "tests/test_release_readiness_script.py",
      "role": "release readiness regression test",
      "sha256": "a4f7451b444a4383784f7dbda2382f54b66350c5e968fdc2321b906deada9670"
    },
    {
      "classification": "supporting",
      "relativePath": "tests/test_regulatory_goldset_analysis.py",
      "role": "regulatory gold-set analysis regression test",
      "sha256": "54e6d77912b949efdd2c5f029cb37e7322f3852b5390e6a5349c4bf3d0b790f2"
    },
    {
      "classification": "supporting",
      "relativePath": "tests/test_trust_surface.py",
      "role": "trust-surface contract regression test",
      "sha256": "ead682cb9cc72deacc0719d8e6c620323146f3e06b5b3ddea4e4d64855ada709"
    },
    {
      "classification": "supporting",
      "relativePath": "tests/test_runtime_security_live_stack.py",
      "role": "live runtime security regression test",
      "sha256": "f13a7de9ab4f78285d14eb39311f22a1e51b051b91a2f44f0d4384a2e708b5b2"
    },
    {
      "classification": "supporting",
      "relativePath": "tests/test_model_discovery_live_stack.py",
      "role": "live model discovery regression test",
      "sha256": "afc5b11232387daf63fe0829a99c05d26a6c3e204d593941f8cbba7d7411f8cc"
    },
    {
      "classification": "supporting",
      "relativePath": "tests/test_oecd_live_stack.py",
      "role": "live OECD workflow regression test",
      "sha256": "4ce7e7e6f38caffd4761b52422e9bcbb2d9925ae86a349fa0c87647bcf39540f"
    }
  ]
}
"""

_RELEASE_BUNDLE_MANIFEST_JSON = r"""
{
  "bundleSha256": "90b3ce941586e17eb3abf6d8f23099658a42a7a7f97bb2a428ec54ee7865868e",
  "contractVersion": "pbpk-mcp.v1",
  "fileCount": 265,
  "files": [
    {
      "group": "root",
      "relativePath": ".DS_Store",
      "sha256": "b2137c2c942e4f0230409e63e7207f151f49cbbec6bdbdaae314c6bae8ae909e",
      "sizeBytes": 6148
    },
    {
      "group": "root",
      "relativePath": ".env.example",
      "sha256": "2e48cd0627895459183ea8a76edc7e7a27a33150b41db0b19115499ce7d84e74",
      "sizeBytes": 3324
    },
    {
      "group": "root",
      "relativePath": ".gitignore",
      "sha256": "f3d7e00741deb461a46968475242580344c5a1dc449d6f5c182db4f7b6f5030d",
      "sizeBytes": 693
    },
    {
      "group": "root",
      "relativePath": "CHANGELOG.md",
      "sha256": "1fcbc9db06b9f735d8592e01e32f14a841128f417f2de0a730ab65233bd3749b",
      "sizeBytes": 23607
    },
    {
      "group": "root",
      "relativePath": "CODE_OF_CONDUCT.md",
      "sha256": "d8d33f5302c9e29f79a0d7251963ab96cfa4dc2c5ac08f2639531eb38d3bd453",
      "sizeBytes": 851
    },
    {
      "group": "root",
      "relativePath": "CONTRIBUTING.md",
      "sha256": "dd0e0547afaced2fcabaf5e2424017ba8716390cb080eeb303c1b01fff983c65",
      "sizeBytes": 1677
    },
    {
      "group": "root",
      "relativePath": "LICENSE",
      "sha256": "63145120ee00b23a582679276e00d8815f992bfc188341490e310eb872b30a59",
      "sizeBytes": 9156
    },
    {
      "group": "root",
      "relativePath": "MANIFEST.in",
      "sha256": "3cb265618639771711bbde5214984357f186e39536768bacc28f6519bc7f9cbf",
      "sizeBytes": 1795
    },
    {
      "group": "root",
      "relativePath": "Makefile",
      "sha256": "6a65e3663af5d32ac6afb60a5398885c495332af5a4ade146d6889cdb13ae0ab",
      "sizeBytes": 6524
    },
    {
      "group": "root",
      "relativePath": "OECD_PBPK_guidelines.pdf",
      "sha256": "8624df7a04bef600b325fed55f1fe70ac5af1ffdee77d6283d9dfba73d7b4ab6",
      "sizeBytes": 8122921
    },
    {
      "group": "root",
      "relativePath": "README.md",
      "sha256": "7854e1cbe653e5dac23aabbe1fc9db9e691f3393753101edaf180894eece5663",
      "sizeBytes": 52193
    },
    {
      "group": "root",
      "relativePath": "SECURITY.md",
      "sha256": "68caf30aeb8889be9ac68579a18eeab31bb9801a2eddb1d11e67e2713c5baadc",
      "sizeBytes": 1415
    },
    {
      "group": "root",
      "relativePath": "docker-compose.celery.yml",
      "sha256": "8634542cace9f71f8f7408ce7a96f547c4519f9da2a18a6c541af8af327dbc62",
      "sizeBytes": 2110
    },
    {
      "group": "root",
      "relativePath": "docker-compose.hardened.yml",
      "sha256": "1e44968b62925cc64f664a7111a81e6f80c297d0c82e2f17d165b772934b898b",
      "sizeBytes": 771
    },
    {
      "group": "root",
      "relativePath": "docker-compose.overlay.yml",
      "sha256": "5a8252b127cfd1173f7af2f7f83fbe5dc507b63d878a4ccbd89b4a1499549d66",
      "sizeBytes": 538
    },
    {
      "group": "root",
      "relativePath": "pyproject.toml",
      "sha256": "917cf75ad4421c9b2e6e0bf459f18512f4e55e273642e6d46149c8d1d7fe55ce",
      "sizeBytes": 2530
    },
    {
      "group": "root",
      "relativePath": "v0.3.4.md",
      "sha256": "840a858c5abdc942c540af2876612311d6939d269218cdaeb81af8802ba27c09",
      "sizeBytes": 2339
    },
    {
      "group": "governance",
      "relativePath": ".github/workflows/model-smoke.yml",
      "sha256": "da86f8673cad4ee2d1dc66193e7392a1128213c253da56c1433fc029b3e3f9f5",
      "sizeBytes": 2868
    },
    {
      "group": "governance",
      "relativePath": ".github/workflows/release-artifacts.yml",
      "sha256": "8568d1e668844f199b409e7f1b610baee3a33f034459e97e3f313941e2aad1cd",
      "sizeBytes": 1465
    },
    {
      "group": "root",
      "relativePath": "benchmarks/regulatory_goldset/.gitignore",
      "sha256": "86532d2a1590a157435fe3c5bde20ea6f64aba8bfbf694858b6de8c48d702a0e",
      "sizeBytes": 22
    },
    {
      "group": "root",
      "relativePath": "benchmarks/regulatory_goldset/README.md",
      "sha256": "3da4d18c8a96049148b26bcd17f37e14e853481b3974e21b4ab8a8dcd9baef14",
      "sizeBytes": 3890
    },
    {
      "group": "root",
      "relativePath": "benchmarks/regulatory_goldset/fetched.lock.json",
      "sha256": "949db5491f40406ab4a0fc185952795bb88f1243ac5c4a3ead1b4fda7661ddca",
      "sizeBytes": 26593
    },
    {
      "group": "root",
      "relativePath": "benchmarks/regulatory_goldset/regulatory_goldset_audit_manifest.json",
      "sha256": "21af57a4b41416ab79cfa86bd58c4582f5834218adad033b8c4b3bb65967931e",
      "sizeBytes": 24492
    },
    {
      "group": "root",
      "relativePath": "benchmarks/regulatory_goldset/regulatory_goldset_scorecard.json",
      "sha256": "212987469243e7b32a06f41cdab74c21b931f4540b12ab6a492baeff6dcd967a",
      "sizeBytes": 84980
    },
    {
      "group": "root",
      "relativePath": "benchmarks/regulatory_goldset/regulatory_goldset_summary.md",
      "sha256": "9bb0eb45eb571d57a30622665b8caeeaaca0e31114edf83554facbe11083d944",
      "sizeBytes": 8415
    },
    {
      "group": "root",
      "relativePath": "benchmarks/regulatory_goldset/sources.lock.json",
      "sha256": "ba24143cfe7ddd976779d7c60d24754b35f8ecf0d361e15c8ad247e488af337b",
      "sizeBytes": 4225
    },
    {
      "group": "container",
      "relativePath": "docker/rxode2-worker.Dockerfile",
      "sha256": "df5dc72543840410c9b0bcc66f6332169269e6bd94f0e6d5979a69c632b4ec4e",
      "sizeBytes": 2794
    },
    {
      "group": "documentation",
      "relativePath": "docs/github_publication_checklist.md",
      "sha256": "7e54a09ce8d5055dc940d85aebae60074681ad01d41bcee7c16c8a3e7e6af75b",
      "sizeBytes": 4283
    },
    {
      "group": "documentation",
      "relativePath": "docs/hardening_migration_notes.md",
      "sha256": "a6b09925902b20e45f15c7e0a703468162cef5bbf1a966eee90aff397130fa88",
      "sizeBytes": 4155
    },
    {
      "group": "documentation",
      "relativePath": "docs/pbk_reviewer_signoff_checklist.md",
      "sha256": "12c8ff065ae36a0ae1f3a94b635d6635ad2b237ecf4755eb2ab2a457dccb336c",
      "sizeBytes": 3372
    },
    {
      "group": "documentation",
      "relativePath": "docs/pbpk_model_onboarding_checklist.md",
      "sha256": "c3ac775a33d357fceac2d74ecd65d1e7d9f3dafa2166fa71f969217b02d56185",
      "sizeBytes": 5727
    },
    {
      "group": "documentation",
      "relativePath": "docs/post_release_audit_plan.md",
      "sha256": "cfedfabd7a0943f94b8afba4d2d0f9b85c8b9225f955bea7e3c331bd316583f5",
      "sizeBytes": 2831
    },
    {
      "group": "documentation",
      "relativePath": "docs/architecture/capability_matrix.json",
      "sha256": "bdc2169d99343f38c5a7dea91306d46704104d488442e4161812dfb63ac6da03",
      "sizeBytes": 4092
    },
    {
      "group": "documentation",
      "relativePath": "docs/architecture/capability_matrix.md",
      "sha256": "ed587abf32181ca8cd530c73b6deb64655cb34473eee9b1cc450becc8a237589",
      "sizeBytes": 2535
    },
    {
      "group": "documentation",
      "relativePath": "docs/architecture/dual_backend_pbpk_mcp.md",
      "sha256": "4a68ce06000174ba1e2379fc4f008ceb7a1f1cba8d4cd418ba8a72adb3e567ab",
      "sizeBytes": 19578
    },
    {
      "group": "documentation",
      "relativePath": "docs/architecture/exposure_led_ngra_role.md",
      "sha256": "25a56d32680e62e8bd99d995c00606fa31e815f0655a31c7bc227122bf298e5a",
      "sizeBytes": 4478
    },
    {
      "group": "documentation",
      "relativePath": "docs/architecture/mcp_payload_conventions.md",
      "sha256": "2bd79754995a99b2f7c679b336a5b9e4e91373714d3e64ddc933da4edcd0ee02",
      "sizeBytes": 18585
    },
    {
      "group": "documentation",
      "relativePath": "docs/deployment/runtime_patch_flow.md",
      "sha256": "dedde45d40263a9e98a68ef4e20e972a760a56a37eb62046eb0a7a3bbea3de4d",
      "sizeBytes": 9279
    },
    {
      "group": "documentation",
      "relativePath": "docs/deployment/rxode2_worker_image.md",
      "sha256": "efb9fbea509203e07628f3f79b6fa24c68b7ee8243fdc2a97ada73253f1b6a0d",
      "sizeBytes": 4305
    },
    {
      "group": "documentation",
      "relativePath": "docs/integration_guides/ospsuite_profile_sidecars.md",
      "sha256": "f968f67bf69baf08ee70ee2a62997d915b744f280056f61dfb80e67e9bbde1a4",
      "sizeBytes": 6952
    },
    {
      "group": "documentation",
      "relativePath": "docs/integration_guides/parameter_table_bundles.md",
      "sha256": "82a258a35db32a4b5e7fa15177510af0f593e8fa0756eea425f2e3b411d7fcd6",
      "sizeBytes": 5055
    },
    {
      "group": "documentation",
      "relativePath": "docs/integration_guides/performance_evidence_bundles.md",
      "sha256": "5d217cf711892ce068e2d51e15a9b4462cd2c6d54f19568f6789145d9920d2e0",
      "sizeBytes": 8081
    },
    {
      "group": "documentation",
      "relativePath": "docs/integration_guides/rxode2_adapter.md",
      "sha256": "2e8e2ea0e9d941944d1b0c1db34e517734ec1c7cfb2af715413703d1bcca7bcd",
      "sizeBytes": 11871
    },
    {
      "group": "documentation",
      "relativePath": "docs/integration_guides/uncertainty_evidence_bundles.md",
      "sha256": "1627966c2fb0563e2414b9e41f486d736084113fd8e5649cb30455488ebf7801",
      "sizeBytes": 5649
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/contracts/openapi.json",
      "sha256": "2cdae40512efcf0bdf7b4ba5c4d4c73a2f4e869a5ecd8f6622fcf8e5a0ada760",
      "sizeBytes": 94687
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/calculate_pk_parameters-request.json",
      "sha256": "53bc6546fecbc109503114d5f6d4116662029cb3e9a7412d87350b4b68ddf1ce",
      "sizeBytes": 549
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/calculate_pk_parameters-response.json",
      "sha256": "516594800d45f66e9fae9ce4002697e21bc4780821b2ce941511cdaf5d261501",
      "sizeBytes": 1663
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/cancel_job-request.json",
      "sha256": "38087c662de0e590325e7a27d6fa0deb51bd00b0a2ef2a21d261fcfbefe29a95",
      "sizeBytes": 284
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/cancel_job-response.json",
      "sha256": "40dd3e67d820a36d8651dc28c548a1f08567940075af9c4d90f1feb66ebe5bcc",
      "sizeBytes": 340
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/discover_models-request.json",
      "sha256": "512cf5053040f4135baf995eacbae45e23ed1a2463d8cb85227db74a05519ea9",
      "sizeBytes": 808
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/discover_models-response.json",
      "sha256": "863fbaf60dbcda0a2286d4a6abd16c3730d55fa631de27ad1c172bdea8dccef7",
      "sizeBytes": 4563
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/export_oecd_report-request.json",
      "sha256": "4199086589f008ee4349f38811cee0ced8222033db1317221bca8c86ecddb425",
      "sizeBytes": 847
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/export_oecd_report-response.json",
      "sha256": "a19e5356449f312428360ebef7abeb89e661505f76f0abfb7c3697aebf4c25ce",
      "sizeBytes": 1301
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/get_job_status-request.json",
      "sha256": "46e5bc645478335701270a57c5da4008fe55c0ba688638eeef9e15f9bb03b6d4",
      "sizeBytes": 299
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/get_job_status-response.json",
      "sha256": "e4c56f74273c647ed2801ca5bde0a13341f34423130ec08f57a016e2b60c8831",
      "sizeBytes": 5481
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/get_parameter_value-request.json",
      "sha256": "7f3a3600f53e2e732df1ef3e6dc6dbd804b91dd994853bf9274d179cabd16139",
      "sizeBytes": 460
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/get_parameter_value-response.json",
      "sha256": "1444cec6cbe77ccec792d9488597573e230799801647228aafb0e8ab0e6bface",
      "sizeBytes": 1405
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/get_population_results-request.json",
      "sha256": "a83920edef8ed8832427e000626fe3ade4ae5352b8f2f3f62fb810a8793aab9d",
      "sizeBytes": 223
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/get_population_results-response.json",
      "sha256": "f7a7020ed2d09acb7ca0c8a330cfbc59a1c06744c8cd953b45e0fed3eb7f99bb",
      "sizeBytes": 3220
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/get_results-request.json",
      "sha256": "8334a906b4ad83ee61c0caec3c771b629a5ad320f4e47fb65429040fb8d98435",
      "sizeBytes": 213
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/get_results-response.json",
      "sha256": "a99e5213a855c30652506c9f9614d606f74564515815f780843516be4647da9d",
      "sizeBytes": 1683
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/ingest_external_pbpk_bundle-request.json",
      "sha256": "f42bffd5b82818a3337a1c7ac93434a279afc94238eb6d525322ed07932722e2",
      "sizeBytes": 3549
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/ingest_external_pbpk_bundle-response.json",
      "sha256": "b7d994d11d8e30887a5e7b385ae2e9cdfcbdd137f68cf9d5ae97e14d5c9c0b45",
      "sizeBytes": 687
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/list_parameters-request.json",
      "sha256": "4ed8c6e1000ee09fe407e6c22e4cb5d38bd6a3e9303ad8f2c84aa4cb9928ffb7",
      "sizeBytes": 526
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/list_parameters-response.json",
      "sha256": "8b9adf0a7dd87fbe0c738fe8ce90262ddd43cc8821e71ab0b3ee75df7069a7c8",
      "sizeBytes": 249
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/load_simulation-request.json",
      "sha256": "197fbd57ae6ceb69cd34f48a743c5efdce93fade2da930aa644f3422debd4ac6",
      "sizeBytes": 520
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/load_simulation-response.json",
      "sha256": "9ed7b601da30445eeb003e88f300434bc47f9a0a85bb62c3c1fc6fc6fdd606db",
      "sizeBytes": 3053
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/run_population_simulation-request.json",
      "sha256": "481138e4899a2af49f16808d923561d7fa151096ad4f728ddba4ad4007495e1e",
      "sizeBytes": 2568
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/run_population_simulation-response.json",
      "sha256": "665e8dc109ca3ed3988f603685afecc3f25cf170973ed9f7ff6ad43a131bb91b",
      "sizeBytes": 679
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/run_sensitivity_analysis-request.json",
      "sha256": "b9d08583f1e14eeee447f60266c28edb10d36d9b11c15a37a3fdafe3df448b55",
      "sizeBytes": 2928
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/run_sensitivity_analysis-response.json",
      "sha256": "8b42ee6faf2b9ca44b2527e758939b33beead1dc0f7bc2d1af08ccd973d52302",
      "sizeBytes": 1185
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/run_simulation-request.json",
      "sha256": "ff03a7cefeeee0d92ff622e7e955a496ae04c29a309856916aa83a5285ea3308",
      "sizeBytes": 1015
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/run_simulation-response.json",
      "sha256": "8b245623a4a09ab8b9f30ad0961b7e9124005601ab5e133f6f3e166b774f4e7a",
      "sizeBytes": 664
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/run_verification_checks-request.json",
      "sha256": "205175d9fd5ff698008e88873465a92e0dbca06f0a31911d6685160ffce69f8f",
      "sizeBytes": 749
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/run_verification_checks-response.json",
      "sha256": "d99d6d5c25e5830cb521528fdc06a41c63c981d7169089b07a07c50ed9904e88",
      "sizeBytes": 1674
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/set_parameter_value-request.json",
      "sha256": "41460671bc3d43af3f1452af273a0f19846078f62c736bae924eae229b2edf38",
      "sizeBytes": 1118
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/set_parameter_value-response.json",
      "sha256": "ecd3427dc4917ecc60427cec0b7091add47699286fdad8582577fea08aaada81",
      "sizeBytes": 1405
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/validate_model_manifest-request.json",
      "sha256": "a70aa3370b9b613b03649361d16070e313640605d64288110c13c3b874c2dd43",
      "sizeBytes": 221
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/validate_model_manifest-response.json",
      "sha256": "8edf8a60261baf85ef3209e2d084858b97d260b4ec3912117e96b01ca029a4d3",
      "sizeBytes": 862
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/validate_simulation_request-request.json",
      "sha256": "ee45460b69048dadcf9c5f1e3c20af31027a743f9fbb7b54cbe123a90f4cf2f2",
      "sizeBytes": 556
    },
    {
      "group": "documentation",
      "relativePath": "docs/mcp-bridge/reference/schemas/validate_simulation_request-response.json",
      "sha256": "d119131d7c6352355f0b69a41dfe28e34def4fc5f1041507e4c3a03336345d41",
      "sizeBytes": 1481
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.2.0.md",
      "sha256": "215480cd86234f2814ea69048fed36cbe0f10868693d24fe3bdc4b255d0acdce",
      "sizeBytes": 2847
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.2.1.md",
      "sha256": "26621b1c5f33eac681d2feb9ef09cbb4e028dcf80d5e6aef60c83dcf8d170326",
      "sizeBytes": 1463
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.2.2.md",
      "sha256": "53bee37d11dfe7225644f612fa00ff80e363d1c6ad9e5544c079bf164b14386f",
      "sizeBytes": 3047
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.2.3.md",
      "sha256": "d1bbffe9959df7058764a60d589af660bf32469d9ff7dd2e00620f0a85bbec06",
      "sizeBytes": 1720
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.2.4.md",
      "sha256": "54b77ec32e1e53995335d242f8ebeb775b8790976463a4be1de8d02e9c8db59f",
      "sizeBytes": 3080
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.3.0.md",
      "sha256": "4f3c93838d27cc42ae24f46a4548ee5d9aa3355f1465ae2ecddeb5ea83fa9ab3",
      "sizeBytes": 3225
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.3.1.md",
      "sha256": "46ba36a2b5266b48c2fa1eea3957b5b5046f5422368530ebf6b6a66383f3ba15",
      "sizeBytes": 3298
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.3.3.md",
      "sha256": "374b8a2b53012acb969778a9d25c1f52faba34e276e6b59aa495db319ac83068",
      "sizeBytes": 2199
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.3.5.md",
      "sha256": "5a8e179425d42a8d62f5ee2bf748cc8ae7ca8b996406e3ef40e550ed34ba8d4e",
      "sizeBytes": 2635
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.4.0.md",
      "sha256": "fc1ae6194fba91e39b586c4de1105a3130b606e8573d9cb230c9a462408530d9",
      "sizeBytes": 3891
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.4.1.md",
      "sha256": "658d7a25178aa0dddfc0bd4c5e1dd24f9b4fc26186f8aa741752c83555c5912c",
      "sizeBytes": 2336
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.4.2.md",
      "sha256": "fa0d6eb9eeabbf715bb673a2fd43bc057d479e9be7ff5d29c9f2cbd3fde46108",
      "sizeBytes": 1884
    },
    {
      "group": "documentation",
      "relativePath": "docs/releases/v0.4.3.md",
      "sha256": "48265243ab0123bcc3b12b270492bdaa98ae4a73de8d43adb704ac329b68ca95",
      "sizeBytes": 2974
    },
    {
      "group": "documentation",
      "relativePath": "docs/security/hardening_baseline.md",
      "sha256": "6da1916d95bf5884362e33393a5b73a46ea0ed401ac183c929e89a0f4ea5b00a",
      "sizeBytes": 4713
    },
    {
      "group": "root",
      "relativePath": "examples/parameter_table_bundle.template.json",
      "sha256": "aab70959a1d5a5d86b27d0d78ca450c9774331926dda7d21ae2878c9635f62ee",
      "sizeBytes": 2567
    },
    {
      "group": "root",
      "relativePath": "examples/performance_evidence_bundle.template.json",
      "sha256": "dc5d8d4cd09b801f6edd8656cb3ed6838893df5120517bd373e2d90e0c44f134",
      "sizeBytes": 3632
    },
    {
      "group": "root",
      "relativePath": "examples/uncertainty_evidence_bundle.template.json",
      "sha256": "8acb3b54c24d447d237255acc20fb115b46d7fdf385ddd14c68e850f3246985d",
      "sizeBytes": 2402
    },
    {
      "group": "root",
      "relativePath": "reference_models/reference_compound_population_rxode2_model.R",
      "sha256": "89b6c44e75ebf77f66906e910c2118bfa33475b7b8b0a03ca43c6f3d9c773e22",
      "sizeBytes": 58551
    },
    {
      "group": "contract",
      "relativePath": "schemas/README.md",
      "sha256": "2f58bea343ec1a49d9c25dbaadc3d36bfa87cebb483f280e776034d0927f4339",
      "sizeBytes": 1143
    },
    {
      "group": "contract",
      "relativePath": "schemas/assessmentContext.v1.json",
      "sha256": "2849beb31892bce04753f732e5bf538595a2a060b9c2c25d291f317640eda20c",
      "sizeBytes": 5466
    },
    {
      "group": "contract",
      "relativePath": "schemas/berInputBundle.v1.json",
      "sha256": "a46c842bfc6dd6f1e1ef4d0f5f65371182c830d478cafae3eef9a599899e9cae",
      "sizeBytes": 5212
    },
    {
      "group": "contract",
      "relativePath": "schemas/internalExposureEstimate.v1.json",
      "sha256": "830b2cf73661b67dfd0e8493c5e410e276555c05f71221db8e36722bf6cb4857",
      "sizeBytes": 5480
    },
    {
      "group": "contract",
      "relativePath": "schemas/pbpkQualificationSummary.v1.json",
      "sha256": "20eb7f265c12d406d453614e8c3a704d19fb8ae6527390d9a9ed6f401cdec2d3",
      "sizeBytes": 10701
    },
    {
      "group": "contract",
      "relativePath": "schemas/pointOfDepartureReference.v1.json",
      "sha256": "58a0e04e48ed716637aae12e972e0f92b858ff6f0cfde918942b97a1daa695aa",
      "sizeBytes": 3625
    },
    {
      "group": "contract",
      "relativePath": "schemas/uncertaintyHandoff.v1.json",
      "sha256": "4547fbcd1014e439abbf5f98ce1e19e0320be8e81eb30102d6a0099fce32d86e",
      "sizeBytes": 2955
    },
    {
      "group": "contract",
      "relativePath": "schemas/uncertaintyRegisterReference.v1.json",
      "sha256": "38808ece8fa55cc3b233f5b3966d480616983d953d0f8f7290cb6191e7222bb6",
      "sizeBytes": 2655
    },
    {
      "group": "contract",
      "relativePath": "schemas/uncertaintySummary.v1.json",
      "sha256": "ea1f95e8bd2786468c0a946f0c2dbbba0045411024292affb052efd33c9e00c3",
      "sizeBytes": 4735
    },
    {
      "group": "contract",
      "relativePath": "schemas/examples/assessmentContext.v1.example.json",
      "sha256": "774828884b6705892187768b505b1c3f5e36ebe83d2a2f570847145297bf3d0c",
      "sizeBytes": 2771
    },
    {
      "group": "contract",
      "relativePath": "schemas/examples/berInputBundle.v1.example.json",
      "sha256": "64399ce683596314bf9d32df20f8c42ffa02673830f477e7e78ea3a0bfa845ff",
      "sizeBytes": 1602
    },
    {
      "group": "contract",
      "relativePath": "schemas/examples/internalExposureEstimate.v1.example.json",
      "sha256": "559f0118d012d14275141d11dbb0d968ed74a0ce39002ad1094bfe87a034009e",
      "sizeBytes": 1300
    },
    {
      "group": "contract",
      "relativePath": "schemas/examples/pbpkQualificationSummary.v1.example.json",
      "sha256": "66bd8b255e52c125e72b18eaf36ea49ed95d0af5c6f4a050d483b5bb0e3697eb",
      "sizeBytes": 6962
    },
    {
      "group": "contract",
      "relativePath": "schemas/examples/pointOfDepartureReference.v1.example.json",
      "sha256": "11185de168163409fb9c22dcfbf7b10c322ff8eddf521d02d1842ee7c4994dbc",
      "sizeBytes": 1140
    },
    {
      "group": "contract",
      "relativePath": "schemas/examples/uncertaintyHandoff.v1.example.json",
      "sha256": "ef372636efb1a13dd26151618eaf440bbde90fad5e600b0ab13945187fb0a03c",
      "sizeBytes": 1682
    },
    {
      "group": "contract",
      "relativePath": "schemas/examples/uncertaintyRegisterReference.v1.example.json",
      "sha256": "652fd3674c30263e5da3e299418327ec4d06811f75f661deff63b2d152b1841f",
      "sizeBytes": 829
    },
    {
      "group": "contract",
      "relativePath": "schemas/examples/uncertaintySummary.v1.example.json",
      "sha256": "9cb008aadd06a2fb4f12dae6ea46023e6f30f30011d851ad76ad9f0f2c9bd181",
      "sizeBytes": 2021
    },
    {
      "group": "operations",
      "relativePath": "scripts/build_cimetidine_cross_system_demo.py",
      "sha256": "3d837b3905526ed252020120e3ae0d8d03ec6005f20461ea944a4a4d85d96a9f",
      "sizeBytes": 27768
    },
    {
      "group": "operations",
      "relativePath": "scripts/build_rxode2_worker_image.sh",
      "sha256": "5174a4bc04a96f68cbcfdf6e45729f987875eb3df0d918cebeb8d366284cad2f",
      "sizeBytes": 702
    },
    {
      "group": "operations",
      "relativePath": "scripts/check_distribution_artifacts.py",
      "sha256": "12934c81c14241f6fb28705c97e9eb443e29c75b5c71005cc0dbb394c57f6084",
      "sizeBytes": 12404
    },
    {
      "group": "operations",
      "relativePath": "scripts/check_installed_package_contract.py",
      "sha256": "e63b48f3f0b7d0f5093f31f157e1b656c62a207b23021f3dd127801094a177ea",
      "sizeBytes": 7169
    },
    {
      "group": "operations",
      "relativePath": "scripts/check_release_metadata.py",
      "sha256": "971bf6472a31e184ac1e55fc17886a69154dd83ac9adb7e1cfef0579ebaf896b",
      "sizeBytes": 5670
    },
    {
      "group": "operations",
      "relativePath": "scripts/check_runtime_contract_env.py",
      "sha256": "82cbd13b4c7c4fef29b06cac4d9552f7db236985c1e7c348391e7f929b35d9a0",
      "sizeBytes": 1515
    },
    {
      "group": "operations",
      "relativePath": "scripts/contract_stage_utils.py",
      "sha256": "56e4c7236e5a343ffddc5cfce5b52ca48ffaf13b28325b4d29cb8c2ec5b63c3c",
      "sizeBytes": 1208
    },
    {
      "group": "operations",
      "relativePath": "scripts/deploy_hardened_stack.sh",
      "sha256": "5fe576c30a4c527048d0d09a700c1c13d94d81eb464316ebb6c080c80add4473",
      "sizeBytes": 586
    },
    {
      "group": "operations",
      "relativePath": "scripts/deploy_rxode2_stack.sh",
      "sha256": "7fd181fb078b42415b4a256d6495daa5ddcdea725268845e5f6a0cbdf6d920ac",
      "sizeBytes": 391
    },
    {
      "group": "operations",
      "relativePath": "scripts/deploy_source_overlay_stack.sh",
      "sha256": "7c202c7aa9f36eb6c8c5e9accbf838493f38e63626581cb3d927c2f4c419b55b",
      "sizeBytes": 482
    },
    {
      "group": "operations",
      "relativePath": "scripts/esqlabs_models.py",
      "sha256": "c7927973573b2d5ecb955b8eba1db6c14088d532c0fb32d3ddc68f3d5c9d194e",
      "sizeBytes": 18084
    },
    {
      "group": "operations",
      "relativePath": "scripts/export_api_docs.py",
      "sha256": "27c9b60cb4f2e9d3f595935c8598eacf7a9507d7597806ead31b55659ce12783",
      "sizeBytes": 13848
    },
    {
      "group": "operations",
      "relativePath": "scripts/fetch_regulatory_goldset.py",
      "sha256": "fc76b285b99b7308c617bd7e3444ab2676d580fccc708b5104b7dda7b0aec5fd",
      "sizeBytes": 8909
    },
    {
      "group": "operations",
      "relativePath": "scripts/generate_contract_artifacts.py",
      "sha256": "d279e12ce72fc682088403fb515460990e90e2311752d6573d42aa0ce0f606ee",
      "sizeBytes": 16201
    },
    {
      "group": "operations",
      "relativePath": "scripts/generate_reference_model_live_audit_pdf.py",
      "sha256": "04848fbe20a293c668cad4fea7eccfbc585d29f14b7bfac90146205c9ab6f5c7",
      "sizeBytes": 44697
    },
    {
      "group": "operations",
      "relativePath": "scripts/generate_regulatory_goldset_audit.py",
      "sha256": "ef244652dad5862ad46c25e1dd6b844a148389dcf7697c242577b3b268e6a0e2",
      "sizeBytes": 9701
    },
    {
      "group": "operations",
      "relativePath": "scripts/generate_repo_concat.py",
      "sha256": "3d79fc32d44a44377aa4e02abe7b430ff1015663e226199a1a8788fa9d86a40c",
      "sizeBytes": 3921
    },
    {
      "group": "operations",
      "relativePath": "scripts/ospsuite_bridge.R",
      "sha256": "104bf3c7e96810207d8f319d03f8cc95aa8106277f7a75f11dc08e9d5bc56301",
      "sizeBytes": 326898
    },
    {
      "group": "operations",
      "relativePath": "scripts/release_readiness_check.py",
      "sha256": "0b91d767dc00cfa0df83773d4082f2918278dd3b27783b4485863754df42f225",
      "sizeBytes": 72441
    },
    {
      "group": "operations",
      "relativePath": "scripts/render_cimetidine_case_study_figures.py",
      "sha256": "f2a07162ee682206a6b7f457846621f5397ea3558223c44f17086d81529c11e6",
      "sizeBytes": 15113
    },
    {
      "group": "operations",
      "relativePath": "scripts/runtime_src_overlay.pth",
      "sha256": "716b898bb8a6ff3a5b1661741d9d174363dc9ace877544bee0f18d9882965ab7",
      "sizeBytes": 240
    },
    {
      "group": "operations",
      "relativePath": "scripts/validate_model_manifests.py",
      "sha256": "773d26392adcae0e748a3f5c3738e61ec7798eb6a0a8da779f9535f8985f6001",
      "sizeBytes": 7954
    },
    {
      "group": "operations",
      "relativePath": "scripts/wait_for_runtime_ready.py",
      "sha256": "fa18ce884ba790f7d208fde156709b2735e4678e68dc75461a4cbe04569364be",
      "sizeBytes": 5658
    },
    {
      "group": "operations",
      "relativePath": "scripts/workspace_model_smoke.py",
      "sha256": "c9f201b0958028473a5434a8704130492021f7fffc8cb42e28b3b9d357257684",
      "sizeBytes": 13656
    },
    {
      "group": "source",
      "relativePath": "src/mcp/__init__.py",
      "sha256": "cfbacb4d06b9ceed2339304629ba0a8bb80ed9e69ea1e9e0ad93a82ae77a39dd",
      "sizeBytes": 3832
    },
    {
      "group": "source",
      "relativePath": "src/mcp/session_registry.py",
      "sha256": "3a893ea7ccc06ac68c22b816cf699847ae536414910ea96474d40d42b9a62d9a",
      "sizeBytes": 10862
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/__init__.py",
      "sha256": "72198d5ebbf0cf6d84ca132423d71aeaf4ab16257c0701796d247d899b7808f0",
      "sizeBytes": 68
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/calculate_pk_parameters.py",
      "sha256": "a007c58049168a6fc5b6d49f6eadc5c09d1835fc6bc18f00dc4bdf9c536d6b97",
      "sizeBytes": 4409
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/cancel_job.py",
      "sha256": "4c2ab92e5be22018a1749fc4dfd9ecd3ad08cd1d3968a0249dbc6fe1a5626eeb",
      "sizeBytes": 1449
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/discover_models.py",
      "sha256": "162ace13e0473220d683350b6bcf9656d6ecdc8ab02a0ad25c6d0a0aaa45b8f5",
      "sizeBytes": 3836
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/export_oecd_report.py",
      "sha256": "eb8d7cc6884cffa9306f7cd549afb6b7961754da9fc4a9d735b3e7ec1f9d1030",
      "sizeBytes": 3508
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/get_job_status.py",
      "sha256": "7fe92f3a91290eebf52b8dcc6d4e5eb8a6a005cfd848b8e73729d21d1222a1b9",
      "sizeBytes": 4735
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/get_parameter_value.py",
      "sha256": "c57e1e8279f10bea11d9c09dabb3e8ec61f0a597e1cf6009b8b798fccf08932d",
      "sizeBytes": 2358
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/get_population_results.py",
      "sha256": "4575abe1dd23eb3b16f57cd7cf025f6c22a3f8165d8468a2f496916eb8bc0b73",
      "sizeBytes": 2164
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/get_results.py",
      "sha256": "527a367817f9db29a20b8445fa4dbf801ea3ea2cbab0b2a7cf4077949190e0f0",
      "sizeBytes": 2779
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/ingest_external_pbpk_bundle.py",
      "sha256": "84464a598002def7fc5e47b9f4a7caf4ad3d0190dc8879c66b88927469e1eebc",
      "sizeBytes": 83376
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/list_parameters.py",
      "sha256": "60c56e65594164e5a8d3627d6bc112930b735397b076e22db1868cf3954f1515",
      "sizeBytes": 2277
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/load_simulation.py",
      "sha256": "f428a9f666873071df351ea97f93e6166a5e59b67b505c5f03428e316717b1f3",
      "sizeBytes": 8993
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/run_population_simulation.py",
      "sha256": "4d3fd94b48999529c624ea4fe472b10fd0761255966689847ecf16b80fa9189b",
      "sizeBytes": 5962
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/run_sensitivity_analysis.py",
      "sha256": "93712be99e085f1d0245acaa8b79e1915b4284a665bcb11077886ebe81ea75b9",
      "sizeBytes": 9094
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/run_simulation.py",
      "sha256": "2e2ef4f467f50a28e64e7812dcca50fe0caa21c1e27dae0e25cb588b65fdedc9",
      "sizeBytes": 2917
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/run_verification_checks.py",
      "sha256": "48147c4fc4a3213f6c3f6f57b56e293692b63d4ec98d9ba9d3651166a3201a69",
      "sizeBytes": 5141
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/set_parameter_value.py",
      "sha256": "9276791c26e38ff0cf7531dc631320a8d5296f4d50815e9329c47bc6ada174f0",
      "sizeBytes": 2809
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/validate_model_manifest.py",
      "sha256": "7711e3542cb7e4794f331013495e62d032bf28ac20f1c786e2d3efc32ca327b9",
      "sizeBytes": 2060
    },
    {
      "group": "source",
      "relativePath": "src/mcp/tools/validate_simulation_request.py",
      "sha256": "336504a9e7561d55e64693606123a05f2e60b53871d69872214690a298830425",
      "sizeBytes": 3908
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/__init__.py",
      "sha256": "bce750f66a62d916be3ff8db800031ed88895e8a9deea9f45322b5263fb7024f",
      "sizeBytes": 311
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/app.py",
      "sha256": "5c31439c0d012e3516b04041d20977caf012e2b1468edc793d2e48a4e27da0cd",
      "sizeBytes": 12998
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/config.py",
      "sha256": "3933285ca637aa14886464166daa2932ac4db8789b76e7151d2636c80ddb4389",
      "sizeBytes": 23454
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/constants.py",
      "sha256": "cbc357731d7dc67082c32f79d91d0a253cc3fc47ff41fb86dc0a9ffde838bdd6",
      "sizeBytes": 158
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/curated_publication.py",
      "sha256": "03d4e07c141b61f096a7ef163f40cab62931dbd47c8b4a63831f9f1bb909ded9",
      "sizeBytes": 909
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/dependencies.py",
      "sha256": "96314468193cafe3274c414edf601429e5619fcc3de85a4da7aba15d36623e0b",
      "sizeBytes": 1731
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/errors.py",
      "sha256": "8a8a661e3b82c9688414622a8e46e073275a710cb78f1b99572da2fe1010bc0e",
      "sizeBytes": 7816
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/logging.py",
      "sha256": "d3da2da31d7d5a97cc22ca53e4c505a4f308b2ccb6729e9e89e0d1b4f6358208",
      "sizeBytes": 1490
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/main.py",
      "sha256": "f8dbbc8f378d29755fd8309b5adaf966a48b93277036451f9379dac881490edd",
      "sizeBytes": 499
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/model_catalog.py",
      "sha256": "3bf0233bb16ae8e5715a2294e01e733aca8b78b7036a2d6ebf1af98312b1e6dd",
      "sizeBytes": 12143
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/model_manifest.py",
      "sha256": "e2d1b9732edc940a21021341ee99f6f9e9fbd7e02862eb58a7bb3e389e6adfdc",
      "sizeBytes": 89457
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/review_signoff.py",
      "sha256": "54ff53d7458391017d97d0df7c5ff22e2990bf8a17214cae306326e35e7d8866",
      "sizeBytes": 16539
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/trust_surface.py",
      "sha256": "bd41076e5234f4f584deefaf8174162e0e482fba53a8f3c63ea7c0efa01d42d1",
      "sizeBytes": 12866
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/adapter/__init__.py",
      "sha256": "50e2c0841f419c57390b1628eb49ab209db08740aac3b609de2302cafbe7fbf6",
      "sizeBytes": 331
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/adapter/environment.py",
      "sha256": "4483a37cfbf991800b33cc38e538f8f9ec7dc80ece9e208e05a350756252ec04",
      "sizeBytes": 3254
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/adapter/errors.py",
      "sha256": "3a17fd6b38082aad8f59bba11dedd1a374a7c3e846e42c03a1c7b8f091fb67ff",
      "sizeBytes": 776
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/adapter/interface.py",
      "sha256": "51ac8394124b55880339db9b0a028ff7599c34c61ab05a0ca47077e1e3a40e93",
      "sizeBytes": 4977
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/adapter/mock.py",
      "sha256": "788ac05af8d37d6c1368d09cc2ab079ab4e0333c6d7bc0ed700ca6dc3249b91c",
      "sizeBytes": 12656
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/adapter/ospsuite.py",
      "sha256": "3778e7bba63b0b2cb723bfca19c666581c30c6d9c31704bf1d7708a7711cba84",
      "sizeBytes": 27156
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/adapter/schema.py",
      "sha256": "ccb81a3f8cf72fa0b925c9c190df6a7ca94023e1efa89b6a0eaace7d598cb0d4",
      "sizeBytes": 3089
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/agent/__init__.py",
      "sha256": "876f3a768c80a05466b89ffb12a170926adecc44e6a00d054c1c83cf60971ac5",
      "sizeBytes": 1851
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/agent/langchain_scaffolding.py",
      "sha256": "34521de49a73b769215f91e6318dfaf8590f86815168a1d4365fb44780af287c",
      "sizeBytes": 39647
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/agent/prompts.py",
      "sha256": "4042448017bad80c6773b1c179ea423c38327acb263ab194ea38e5e1a2aad2a4",
      "sizeBytes": 6782
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/agent/sensitivity.py",
      "sha256": "5b2d41ffb1572495ad02d5bbecefb92292734aedf04ee79dd271e3c4acaf313f",
      "sizeBytes": 12480
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/audit/__init__.py",
      "sha256": "04e06d76195136b39241234502c39ecb90d349f0216ab35bcbee06edd8f759d4",
      "sizeBytes": 290
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/audit/jobs.py",
      "sha256": "6425ac551bddd29701bb9efdf2a55e3bd5ad18ea114895e240f380f3386506cd",
      "sizeBytes": 2357
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/audit/middleware.py",
      "sha256": "794e3b5d3bccefb61f0be184e9aa98faccde67babc6d438fd2b19ae25dd62d19",
      "sizeBytes": 3020
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/audit/trail.py",
      "sha256": "4a812794c447db0102d8abbc59c2d5f23a3103a601fa4f6179e6e17b35b88bae",
      "sizeBytes": 10206
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/audit/verify.py",
      "sha256": "e2279714b305eff7caeafde6cfbe8e9c29bc912f562a04af313abbe508c16683",
      "sizeBytes": 10454
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/benchmarking/__init__.py",
      "sha256": "62fb79a3b8b4eabf773ea302301011084c74fc08dea65cd77904639c407c0c9b",
      "sizeBytes": 201
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/benchmarking/__main__.py",
      "sha256": "c51470c373ced0958343482c6adfb1ae30841974138d31374d21b1f35d6af8df",
      "sizeBytes": 172
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/benchmarking/cli.py",
      "sha256": "6f89071c568e8ee596a135fd2564741ff2daa25895932844e760ad3a060710bd",
      "sizeBytes": 31789
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/benchmarking/regulatory_goldset.py",
      "sha256": "6760efa0d01df3e79250c095d6d07d59e2bff3dd3868f8f0740728dc1eaa6420",
      "sizeBytes": 53551
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/contract/__init__.py",
      "sha256": "4243ff28761358c0d031c13e9246f368c23198fc6ed1ba6289419838182fba31",
      "sizeBytes": 537
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/contract/publication_inventory.py",
      "sha256": "60339a923f15b3f51888c7a756b0ba117c05421980d15e212c8b63ce48e5f189",
      "sizeBytes": 863
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/literature/actions.py",
      "sha256": "857b82b61127013c3479566aec2a980c76847aba3c4115ac66b259c2a103ac68",
      "sizeBytes": 5502
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/literature/evaluation.py",
      "sha256": "8064e40f7d175b3c473468a99365ffc437585d3d2045b2415b51e5dc0766914b",
      "sizeBytes": 4196
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/literature/extractors.py",
      "sha256": "17e9af7f0fb75d1b63e5a40cf1c4e5dd61063e28f32afdcfd42aa3a900a8e193",
      "sizeBytes": 6374
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/literature/interfaces.py",
      "sha256": "9ffc28959709f4cf590109030d079e1c1f9aef5971ed610b2c0911a19294ab3f",
      "sizeBytes": 1251
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/literature/models.py",
      "sha256": "84755d705ee8f812d83324db6b9535379399eafd2a4b3afceb06c681b110813a",
      "sizeBytes": 1901
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/literature/pipeline.py",
      "sha256": "4437d6e4b3b711063a67dc2a74ed55d2ec8c6b812d9fad3c65a10159a1049fea",
      "sizeBytes": 2853
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/literature/validation.py",
      "sha256": "c0c939db7105c3db5310d80681a1f7387e9d57aff4257239abd7c6b90ba838b2",
      "sizeBytes": 2508
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/parity/__init__.py",
      "sha256": "4b07a414f60d8e610785f644a4a018e43f8d32ab6fe71442a6f4188280d47f54",
      "sizeBytes": 166
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/parity/data.py",
      "sha256": "12e5b74bc66b26fa941dc58d27edeaba5152170828fe654f599882cf9570ca42",
      "sizeBytes": 5908
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/parity/suite.py",
      "sha256": "423973116d4bd0d1571f065adaeb07f52fb4229a2511f368f22cbdb17392962d",
      "sizeBytes": 11605
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/routes/__init__.py",
      "sha256": "9f9c8ff32209047fe8fa2e5e620126b4cafa9a239755a258dd235e785d084bb4",
      "sizeBytes": 73
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/routes/audit.py",
      "sha256": "3439b990e2e54eb4d21f435f354f678b9e22738b1d92ed981d08fd96b60e13b3",
      "sizeBytes": 993
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/routes/jsonrpc.py",
      "sha256": "fe6ae3b434c9cf8dc49e0c178774bc8257bb35a60220eb8c69bce0da95839198",
      "sizeBytes": 12215
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/routes/mcp.py",
      "sha256": "1bb4f3474528381806cabf8bce78fc8b43cdb28da56bcefa149cc926932bdcf7",
      "sizeBytes": 22106
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/routes/resources.py",
      "sha256": "1777d1ad872b793cd44d1f4a04ceb434054bab2c74fc91f26d4eccd5bbf59778",
      "sizeBytes": 86
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/routes/resources_base.py",
      "sha256": "a6cdbed6094b50c3c38a991b5c5ae4bbbdb70b07c91660c0cec806971de8c35c",
      "sizeBytes": 34528
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/routes/simulation.py",
      "sha256": "5425b55d6ca24d5d37cceab80751286ffce50ca0edac8f7d089b8ee73d714b96",
      "sizeBytes": 48818
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/runtime/__init__.py",
      "sha256": "7940713de76978b045ace4bff165886ca38d7009b7cc5e2f44294842e79b5894",
      "sizeBytes": 274
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/runtime/factory.py",
      "sha256": "b53c8cf4a032c58f32e6183333fb62f9b9fd3ff3cf9419d29d18b9e26c5fd1af",
      "sizeBytes": 3172
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/runtime/session_cli.py",
      "sha256": "279237a5ee2d65e2f2a5a2a9f881ec8ed7d3d95b7d1ceae394adc54c1870ef23",
      "sizeBytes": 3143
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/schemas/__init__.py",
      "sha256": "d0b49334a5992a2697fc99a3b6570a2a978aa93c878f4c5a97608c5dfac513c7",
      "sizeBytes": 60
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/schemas/extraction-record.json",
      "sha256": "46f2024647b304d885a9b968bcaeded2566acc0f50e6754d856ff4422a1ba7de",
      "sizeBytes": 2655
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/security/__init__.py",
      "sha256": "abf958184fa45b6de39252fa046a65e33c29672686f3e35f3964346b4dfb7484",
      "sizeBytes": 223
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/security/auth.py",
      "sha256": "9fb5fad56b909e4e805181d0a356c196c8daa722913cd3c60438cdf07a868a29",
      "sizeBytes": 7835
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/security/confirmation.py",
      "sha256": "ef01caa5c11b969a0520b35751e32f2638d06f4e4201beee70e04b691dc5366d",
      "sizeBytes": 1233
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/security/phi.py",
      "sha256": "8dae5ce7e85adaefaa8dbead8b3d09d995e5b847169c53d44d55b1fb2a82a7c0",
      "sizeBytes": 2599
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/security/simple_jwt.py",
      "sha256": "f831776868d4b19ec62ea4e6f25fcd5379441859da9b0b1ce37c87c9a9353532",
      "sizeBytes": 2225
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/services/celery_app.py",
      "sha256": "f461ff156212fc0f22c3365e31f69c7e448027e85be9c31691cee5ff22b85048",
      "sizeBytes": 3059
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/services/job_service.py",
      "sha256": "3cc1465a64f88f9fc5336680612be62347166a42ebcc46ffc89a45a8671a72e0",
      "sizeBytes": 52246
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/services/llm.py",
      "sha256": "8d258575a3a441b308692d7fdd5738019d921b58feb24b281aac7d460e63390e",
      "sizeBytes": 3243
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/services/snapshot_service.py",
      "sha256": "9e93bd27131e8c14c837bdb90e171e7a1283dc0b2c3b3abb02fd499a1078984f",
      "sizeBytes": 1666
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/storage/population_store.py",
      "sha256": "3a32dd1385614609a089fc1e3d50d04cfcc08e37c558d2196e5052ff40f82e3f",
      "sizeBytes": 4743
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/storage/snapshot_store.py",
      "sha256": "b02e5b7119b57e2e01d4f3fb892863500d53817d845cceb8d54e18eae555ef3c",
      "sizeBytes": 5338
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/tools/__init__.py",
      "sha256": "5ca2ce8f6e4750df85208f6aabb1edf80a90166356782155b0cf4cdd25989fe4",
      "sizeBytes": 155
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/tools/registry.py",
      "sha256": "b8c4d0cf161e728f520acb89073a79e005ec4c2e20d489567efa05b87b67d2a1",
      "sizeBytes": 417
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/tools/registry_base.py",
      "sha256": "890944e60bfab7dbd4f2c947775f46eecae92c799aceae58237ee3e9d1b673f7",
      "sizeBytes": 12428
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/util/__init__.py",
      "sha256": "6992a93318005c92e1c7d5f37364b233fb8b7883f516de401c454440d8354af2",
      "sizeBytes": 111
    },
    {
      "group": "source",
      "relativePath": "src/mcp_bridge/util/concurrency.py",
      "sha256": "9e5a3481efcb2e212cc6536a928c3fdc08d2209ce7a8bcb84f6c019177eeff8d",
      "sizeBytes": 481
    },
    {
      "group": "verification",
      "relativePath": "tests/test_capability_matrix.py",
      "sha256": "307eb57a401af87e4861d24d7c9994179cf6f3541ba5f49591f11f3a25c1ae82",
      "sizeBytes": 3597
    },
    {
      "group": "verification",
      "relativePath": "tests/test_config_contract.py",
      "sha256": "03129fc934d8a345d8c8ad0f5844599d8728caad6decc07fea3afb4e3194207b",
      "sizeBytes": 2411
    },
    {
      "group": "verification",
      "relativePath": "tests/test_deployment_profiles.py",
      "sha256": "2208f44388b789f539c489b41693a4a912a1ff3566cc6012912fdc553cd5489f",
      "sizeBytes": 10311
    },
    {
      "group": "verification",
      "relativePath": "tests/test_distribution_artifacts.py",
      "sha256": "a3db829bb67d9681ed81041548d0ff78b37826f26e7f10aa9870f2bb69ddcec0",
      "sizeBytes": 10675
    },
    {
      "group": "verification",
      "relativePath": "tests/test_export_api_docs.py",
      "sha256": "551a24392a43ee490630ed73a78aaa87c2362454a6025c0ab692a8ea43e11d37",
      "sizeBytes": 2197
    },
    {
      "group": "verification",
      "relativePath": "tests/test_external_pbpk_bundle.py",
      "sha256": "3a56dda98bb1f0fa4deef930784baaeace7f0ac6cf23a83b2ca8d548876c506c",
      "sizeBytes": 13621
    },
    {
      "group": "verification",
      "relativePath": "tests/test_generate_repo_concat_script.py",
      "sha256": "7921c17dfaf9ef405581f342af60d5cec8143d6defec6de0e44dd93b4666d4b7",
      "sizeBytes": 2822
    },
    {
      "group": "verification",
      "relativePath": "tests/test_load_simulation_contract.py",
      "sha256": "342a9e8412462b79226ee231de72b099ff9117cdb7db687542b0712bc863aaad",
      "sizeBytes": 958
    },
    {
      "group": "verification",
      "relativePath": "tests/test_model_discovery_live_stack.py",
      "sha256": "afc5b11232387daf63fe0829a99c05d26a6c3e204d593941f8cbba7d7411f8cc",
      "sizeBytes": 23371
    },
    {
      "group": "verification",
      "relativePath": "tests/test_model_manifest.py",
      "sha256": "b9dcd3ce10a29e96e179c6c3fd5d1a7e76c3da8067d7264963d0c3b039e7e725",
      "sizeBytes": 52314
    },
    {
      "group": "verification",
      "relativePath": "tests/test_model_path_env_resolution.py",
      "sha256": "74537aa8b178ca3a6c9f9d779ba1c7f00eb748277985c93ec264436c1c15087b",
      "sizeBytes": 3216
    },
    {
      "group": "verification",
      "relativePath": "tests/test_ngra_object_schemas.py",
      "sha256": "d5e03c3245f6d8de9778032ceb18277ccfe443be2078c8494ac63a3376b0934e",
      "sizeBytes": 6900
    },
    {
      "group": "verification",
      "relativePath": "tests/test_oecd_bridge.py",
      "sha256": "87f3991428ec90556fc66eec98ea011943226b1eda993cfcf96be83360bbaa4e",
      "sizeBytes": 93361
    },
    {
      "group": "verification",
      "relativePath": "tests/test_oecd_live_stack.py",
      "sha256": "4ce7e7e6f38caffd4761b52422e9bcbb2d9925ae86a349fa0c87647bcf39540f",
      "sizeBytes": 44085
    },
    {
      "group": "verification",
      "relativePath": "tests/test_packaged_adapter_namespace.py",
      "sha256": "5c1d6cc7d36940d8c5183c9a1dcdc160f3e74abba165fb9f535de4715165286a",
      "sizeBytes": 1217
    },
    {
      "group": "verification",
      "relativePath": "tests/test_packaged_contract_artifacts.py",
      "sha256": "d32b073041a4c11bd976648cf31672de47276dcb03009522acce2a367275b18e",
      "sizeBytes": 5841
    },
    {
      "group": "verification",
      "relativePath": "tests/test_packaged_mcp_namespace.py",
      "sha256": "989518becb87c3f8c3bd438230463252fea6ae38c8cc99940ea3caf88bcc3cba",
      "sizeBytes": 1253
    },
    {
      "group": "verification",
      "relativePath": "tests/test_packaged_resource_routes.py",
      "sha256": "0cb7bd22a711c485c7e7484dff3404bbc6c858ae0d4e24b3fb61cfd7d1bec2de",
      "sizeBytes": 4369
    },
    {
      "group": "verification",
      "relativePath": "tests/test_packaged_tool_registry.py",
      "sha256": "a8b8787df18ca23023210917e29c17b3c9795b9f9302b9aa9dea4ec814811f3b",
      "sizeBytes": 2083
    },
    {
      "group": "verification",
      "relativePath": "tests/test_regulatory_goldset_analysis.py",
      "sha256": "54e6d77912b949efdd2c5f029cb37e7322f3852b5390e6a5349c4bf3d0b790f2",
      "sizeBytes": 7730
    },
    {
      "group": "verification",
      "relativePath": "tests/test_regulatory_goldset_manifest.py",
      "sha256": "2ec1e05aa31b756a0f687f0917174f6d96f2061fd4d2446f27e4e07e24e8b929",
      "sizeBytes": 1659
    },
    {
      "group": "verification",
      "relativePath": "tests/test_release_metadata.py",
      "sha256": "6e7213203360cf196a5303252ea0e0b3a8cb19e45ae31e506cccbace2774152c",
      "sizeBytes": 5123
    },
    {
      "group": "verification",
      "relativePath": "tests/test_release_readiness_script.py",
      "sha256": "a4f7451b444a4383784f7dbda2382f54b66350c5e968fdc2321b906deada9670",
      "sizeBytes": 3142
    },
    {
      "group": "verification",
      "relativePath": "tests/test_review_signoff.py",
      "sha256": "2a90ea8f00a09e44d1c26a297834612d6fd443b15b4afea5227bb1ff36a8e33c",
      "sizeBytes": 11257
    },
    {
      "group": "verification",
      "relativePath": "tests/test_runtime_security_live_stack.py",
      "sha256": "f13a7de9ab4f78285d14eb39311f22a1e51b051b91a2f44f0d4384a2e708b5b2",
      "sizeBytes": 13766
    },
    {
      "group": "verification",
      "relativePath": "tests/test_security_posture.py",
      "sha256": "f9d32e6e5b0ff6391ed0ff7f5d9bd4d485564fe21e546e191a01968f97930de4",
      "sizeBytes": 4545
    },
    {
      "group": "verification",
      "relativePath": "tests/test_trust_surface.py",
      "sha256": "ead682cb9cc72deacc0719d8e6c620323146f3e06b5b3ddea4e4d64855ada709",
      "sizeBytes": 4774
    },
    {
      "group": "verification",
      "relativePath": "tests/test_validate_model_manifests_script.py",
      "sha256": "ba103676a4865dd034a0cf94431a25499af07e9c9288ec103ffcda60bc82ece2",
      "sizeBytes": 6712
    },
    {
      "group": "verification",
      "relativePath": "tests/test_workspace_model_smoke_script.py",
      "sha256": "252aed1d7ede9b48a6e6d6151cf2b3ce44a9c74ac56bca16026319c5d63a838f",
      "sizeBytes": 1782
    },
    {
      "group": "verification",
      "relativePath": "tests/unit/test_adapter_interface.py",
      "sha256": "ea8ff31d6714576dce67df4e480a4b7d35947d507614e2c1621c9b08ec9632e9",
      "sizeBytes": 3673
    },
    {
      "group": "verification",
      "relativePath": "tests/unit/test_subprocess_adapter.py",
      "sha256": "9030315f50274036fd4943f490d9a8856eb384b34aebd1179d7d946c5bbd6b3c",
      "sizeBytes": 16625
    }
  ],
  "groupCounts": {
    "container": 1,
    "contract": 17,
    "documentation": 68,
    "governance": 2,
    "operations": 24,
    "root": 28,
    "source": 94,
    "verification": 31
  },
  "id": "pbpk-release-bundle-manifest.v1",
  "packageVersion": "0.4.3",
  "selectionPolicy": {
    "acyclicIntegrityExclusions": [
      "docs/architecture/release_bundle_manifest.json",
      "docs/architecture/contract_manifest.json",
      "src/mcp_bridge/contract/artifacts.py"
    ],
    "excludedPatterns": [
      ".git",
      ".mypy_cache",
      ".pytest_cache",
      ".ruff_cache",
      "__pycache__",
      ".tox",
      ".nox",
      ".venv",
      "venv",
      "env",
      ".tmp_codex_*",
      "build",
      "dist",
      "*.egg-info",
      "var",
      "reports",
      "output",
      "tmp",
      "private_models",
      "figures",
      "downloads",
      "extracted",
      "~"
    ],
    "mode": "staged-source-tree-equivalent"
  },
  "totalBytes": 10651964
}
"""

_SCHEMA_JSON = {
    'assessmentContext.v1': r"""
{
  "$defs": {
    "backend": {
      "enum": [
        "ospsuite",
        "rxode2",
        "external-import"
      ],
      "type": "string"
    },
    "selectionTriplet": {
      "additionalProperties": true,
      "properties": {
        "declared": {
          "type": [
            "string",
            "null"
          ]
        },
        "effective": {
          "type": [
            "string",
            "null"
          ]
        },
        "requested": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "effective"
      ],
      "type": "object"
    },
    "stringArray": {
      "items": {
        "type": "string"
      },
      "type": "array"
    }
  },
  "$id": "https://raw.githubusercontent.com/ToxMCP/pbpk-mcp/main/schemas/assessmentContext.v1.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": true,
  "description": "PBPK-side context-alignment object emitted by PBPK MCP.",
  "properties": {
    "assessmentBoundary": {
      "const": "pbpk-context-alignment-only"
    },
    "backend": {
      "$ref": "#/$defs/backend"
    },
    "contextOfUse": {
      "additionalProperties": true,
      "properties": {
        "decisionContext": {
          "$ref": "#/$defs/selectionTriplet"
        },
        "regulatoryUse": {
          "$ref": "#/$defs/selectionTriplet"
        },
        "scientificPurpose": {
          "$ref": "#/$defs/selectionTriplet"
        }
      },
      "required": [
        "regulatoryUse",
        "scientificPurpose",
        "decisionContext"
      ],
      "type": "object"
    },
    "decisionBoundary": {
      "const": "no-ngra-decision-policy"
    },
    "domain": {
      "additionalProperties": true,
      "properties": {
        "compound": {
          "$ref": "#/$defs/selectionTriplet"
        },
        "lifeStage": {
          "$ref": "#/$defs/selectionTriplet"
        },
        "population": {
          "$ref": "#/$defs/selectionTriplet"
        },
        "route": {
          "$ref": "#/$defs/selectionTriplet"
        },
        "species": {
          "$ref": "#/$defs/selectionTriplet"
        }
      },
      "required": [
        "species",
        "route",
        "lifeStage",
        "population",
        "compound"
      ],
      "type": "object"
    },
    "doseScenario": {
      "additionalProperties": true,
      "type": [
        "object",
        "null"
      ]
    },
    "objectId": {
      "minLength": 1,
      "type": "string"
    },
    "objectType": {
      "const": "assessmentContext.v1"
    },
    "populationSupport": {
      "additionalProperties": true,
      "properties": {
        "extrapolationPolicy": {
          "type": [
            "string",
            "null"
          ]
        },
        "supportedGenotypesOrPhenotypes": {
          "$ref": "#/$defs/stringArray"
        },
        "supportedLifeStages": {
          "$ref": "#/$defs/stringArray"
        },
        "supportedPhysiologyContexts": {
          "$ref": "#/$defs/stringArray"
        },
        "supportedSpecies": {
          "$ref": "#/$defs/stringArray"
        },
        "variabilityRepresentation": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "type": [
        "object",
        "null"
      ]
    },
    "simulationId": {
      "type": [
        "string",
        "null"
      ]
    },
    "sourcePlatform": {
      "type": [
        "string",
        "null"
      ]
    },
    "supports": {
      "additionalProperties": true,
      "properties": {
        "decisionRecommendation": {
          "type": "boolean"
        },
        "declaredProfileComparison": {
          "type": "boolean"
        },
        "requestContextAlignment": {
          "type": "boolean"
        },
        "typedNgraHandoff": {
          "type": "boolean"
        }
      },
      "required": [
        "declaredProfileComparison",
        "requestContextAlignment",
        "typedNgraHandoff",
        "decisionRecommendation"
      ],
      "type": "object"
    },
    "targetOutput": {
      "additionalProperties": true,
      "properties": {
        "declared": {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        "requested": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "requested",
        "declared"
      ],
      "type": "object"
    },
    "validationDecision": {
      "type": [
        "string",
        "null"
      ]
    },
    "workflowRole": {
      "additionalProperties": true,
      "properties": {
        "downstreamOutputs": {
          "$ref": "#/$defs/stringArray"
        },
        "nonGoals": {
          "$ref": "#/$defs/stringArray"
        },
        "role": {
          "type": [
            "string",
            "null"
          ]
        },
        "upstreamDependencies": {
          "$ref": "#/$defs/stringArray"
        },
        "workflow": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "type": [
        "object",
        "null"
      ]
    }
  },
  "required": [
    "objectType",
    "objectId",
    "backend",
    "assessmentBoundary",
    "decisionBoundary",
    "contextOfUse",
    "domain",
    "targetOutput",
    "supports"
  ],
  "title": "assessmentContext.v1",
  "type": "object"
}
""",
    'berInputBundle.v1': r"""
{
  "$defs": {
    "backend": {
      "enum": [
        "ospsuite",
        "rxode2",
        "external-import"
      ],
      "type": "string"
    },
    "stringArray": {
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "trueDoseAdjustment": {
      "additionalProperties": true,
      "properties": {
        "applied": {
          "type": "boolean"
        },
        "basis": {
          "type": [
            "string",
            "null"
          ]
        },
        "summary": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "applied"
      ],
      "type": "object"
    }
  },
  "$id": "https://raw.githubusercontent.com/ToxMCP/pbpk-mcp/main/schemas/berInputBundle.v1.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": true,
  "description": "Thin BER-ready PBPK-side handoff bundle emitted by PBPK MCP.",
  "properties": {
    "assessmentBoundary": {
      "const": "external-ber-calculation-only"
    },
    "backend": {
      "$ref": "#/$defs/backend"
    },
    "blockingReasons": {
      "$ref": "#/$defs/stringArray"
    },
    "comparisonMetric": {
      "minLength": 1,
      "type": "string"
    },
    "decisionBoundary": {
      "const": "ber-calculation-and-decision-owned-by-external-orchestrator"
    },
    "decisionOwner": {
      "const": "external-orchestrator"
    },
    "internalExposureEstimateRef": {
      "type": [
        "string",
        "null"
      ]
    },
    "internalExposureMetric": {
      "additionalProperties": true,
      "properties": {
        "metric": {
          "minLength": 1,
          "type": "string"
        },
        "outputPath": {
          "type": [
            "string",
            "null"
          ]
        },
        "unit": {
          "type": [
            "string",
            "null"
          ]
        },
        "value": {
          "type": [
            "number",
            "null"
          ]
        }
      },
      "required": [
        "metric",
        "value",
        "outputPath"
      ],
      "type": [
        "object",
        "null"
      ]
    },
    "objectId": {
      "minLength": 1,
      "type": "string"
    },
    "objectType": {
      "const": "berInputBundle.v1"
    },
    "podMetadata": {
      "additionalProperties": true,
      "properties": {
        "basis": {
          "type": [
            "string",
            "null"
          ]
        },
        "metric": {
          "type": [
            "string",
            "null"
          ]
        },
        "ref": {
          "type": [
            "string",
            "null"
          ]
        },
        "source": {
          "type": [
            "string",
            "null"
          ]
        },
        "summary": {
          "type": [
            "string",
            "null"
          ]
        },
        "unit": {
          "type": [
            "string",
            "null"
          ]
        },
        "value": {
          "type": [
            "number",
            "null"
          ]
        }
      },
      "type": "object"
    },
    "podRef": {
      "type": [
        "string",
        "null"
      ]
    },
    "pointOfDepartureReferenceRef": {
      "type": [
        "string",
        "null"
      ]
    },
    "qualificationSummaryRef": {
      "type": [
        "string",
        "null"
      ]
    },
    "requiredExternalInputs": {
      "$ref": "#/$defs/stringArray"
    },
    "simulationId": {
      "type": [
        "string",
        "null"
      ]
    },
    "sourcePlatform": {
      "type": [
        "string",
        "null"
      ]
    },
    "status": {
      "enum": [
        "ready-for-external-ber-calculation",
        "incomplete"
      ],
      "type": "string"
    },
    "supports": {
      "additionalProperties": true,
      "properties": {
        "decisionRecommendation": {
          "type": "boolean"
        },
        "externalBerCalculation": {
          "type": "boolean"
        },
        "externalPodReferenceAttached": {
          "type": "boolean"
        },
        "internalExposureMetricAttached": {
          "type": "boolean"
        },
        "trueDoseMetadataAttached": {
          "type": "boolean"
        }
      },
      "required": [
        "internalExposureMetricAttached",
        "externalPodReferenceAttached",
        "trueDoseMetadataAttached",
        "externalBerCalculation",
        "decisionRecommendation"
      ],
      "type": "object"
    },
    "trueDoseAdjustment": {
      "$ref": "#/$defs/trueDoseAdjustment"
    },
    "trueDoseAdjustmentApplied": {
      "type": "boolean"
    },
    "uncertaintySummaryRef": {
      "type": [
        "string",
        "null"
      ]
    },
    "warnings": {
      "$ref": "#/$defs/stringArray"
    }
  },
  "required": [
    "objectType",
    "objectId",
    "backend",
    "assessmentBoundary",
    "decisionBoundary",
    "decisionOwner",
    "status",
    "comparisonMetric",
    "trueDoseAdjustment",
    "trueDoseAdjustmentApplied",
    "supports",
    "requiredExternalInputs",
    "blockingReasons"
  ],
  "title": "berInputBundle.v1",
  "type": "object"
}
""",
    'internalExposureEstimate.v1': r"""
{
  "$defs": {
    "backend": {
      "enum": [
        "ospsuite",
        "rxode2",
        "external-import"
      ],
      "type": "string"
    },
    "outputSummary": {
      "additionalProperties": true,
      "properties": {
        "auc0Tlast": {
          "type": [
            "number",
            "null"
          ]
        },
        "aucUnitBasis": {
          "type": [
            "string",
            "null"
          ]
        },
        "cmax": {
          "type": [
            "number",
            "null"
          ]
        },
        "outputPath": {
          "type": [
            "string",
            "null"
          ]
        },
        "pointCount": {
          "minimum": 0,
          "type": "integer"
        },
        "tmax": {
          "type": [
            "number",
            "null"
          ]
        },
        "unit": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "outputPath",
        "pointCount",
        "cmax",
        "tmax",
        "auc0Tlast",
        "aucUnitBasis"
      ],
      "type": "object"
    },
    "stringArray": {
      "items": {
        "type": "string"
      },
      "type": "array"
    }
  },
  "$id": "https://raw.githubusercontent.com/ToxMCP/pbpk-mcp/main/schemas/internalExposureEstimate.v1.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": true,
  "description": "PBPK-side deterministic internal-exposure estimate emitted by PBPK MCP.",
  "properties": {
    "analyte": {
      "type": [
        "string",
        "null"
      ]
    },
    "assessmentBoundary": {
      "const": "pbpk-side-internal-exposure-estimate-only"
    },
    "backend": {
      "$ref": "#/$defs/backend"
    },
    "candidateOutputCount": {
      "minimum": 0,
      "type": "integer"
    },
    "candidateOutputs": {
      "items": {
        "$ref": "#/$defs/outputSummary"
      },
      "type": "array"
    },
    "candidateOutputsTruncated": {
      "type": [
        "boolean",
        "null"
      ]
    },
    "decisionBoundary": {
      "const": "no-ngra-decision-policy"
    },
    "distribution": {
      "additionalProperties": true,
      "type": [
        "object",
        "null"
      ]
    },
    "doseScenario": {
      "additionalProperties": true,
      "type": [
        "object",
        "null"
      ]
    },
    "objectId": {
      "minLength": 1,
      "type": "string"
    },
    "objectType": {
      "const": "internalExposureEstimate.v1"
    },
    "population": {
      "type": [
        "string",
        "null"
      ]
    },
    "requestedTargetOutput": {
      "type": [
        "string",
        "null"
      ]
    },
    "resultsId": {
      "type": [
        "string",
        "null"
      ]
    },
    "route": {
      "type": [
        "string",
        "null"
      ]
    },
    "selectedOutput": {
      "additionalProperties": true,
      "properties": {
        "auc0Tlast": {
          "type": [
            "number",
            "null"
          ]
        },
        "aucUnitBasis": {
          "type": [
            "string",
            "null"
          ]
        },
        "cmax": {
          "type": [
            "number",
            "null"
          ]
        },
        "outputPath": {
          "type": [
            "string",
            "null"
          ]
        },
        "pointCount": {
          "minimum": 0,
          "type": "integer"
        },
        "tmax": {
          "type": [
            "number",
            "null"
          ]
        },
        "unit": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "outputPath",
        "pointCount",
        "cmax",
        "tmax",
        "auc0Tlast",
        "aucUnitBasis"
      ],
      "type": [
        "object",
        "null"
      ]
    },
    "selectionReason": {
      "type": [
        "string",
        "null"
      ]
    },
    "selectionStatus": {
      "type": [
        "string",
        "null"
      ]
    },
    "simulationId": {
      "type": [
        "string",
        "null"
      ]
    },
    "source": {
      "minLength": 1,
      "type": "string"
    },
    "sourcePlatform": {
      "type": [
        "string",
        "null"
      ]
    },
    "species": {
      "type": [
        "string",
        "null"
      ]
    },
    "status": {
      "enum": [
        "available",
        "not-available"
      ],
      "type": "string"
    },
    "supports": {
      "additionalProperties": true,
      "properties": {
        "decisionRecommendation": {
          "type": "boolean"
        },
        "deterministicMetricSelection": {
          "type": "boolean"
        },
        "externalBerHandoff": {
          "type": "boolean"
        },
        "populationDistributionSummary": {
          "type": "boolean"
        }
      },
      "required": [
        "deterministicMetricSelection",
        "populationDistributionSummary",
        "externalBerHandoff",
        "decisionRecommendation"
      ],
      "type": "object"
    },
    "warnings": {
      "$ref": "#/$defs/stringArray"
    }
  },
  "required": [
    "objectType",
    "objectId",
    "backend",
    "assessmentBoundary",
    "decisionBoundary",
    "status",
    "source",
    "candidateOutputCount",
    "candidateOutputs",
    "supports",
    "warnings"
  ],
  "title": "internalExposureEstimate.v1",
  "type": "object"
}
""",
    'pbpkQualificationSummary.v1': r"""
{
  "$defs": {
    "backend": {
      "enum": [
        "ospsuite",
        "rxode2",
        "external-import"
      ],
      "type": "string"
    },
    "stringArray": {
      "items": {
        "type": "string"
      },
      "type": "array"
    }
  },
  "$id": "https://raw.githubusercontent.com/ToxMCP/pbpk-mcp/main/schemas/pbpkQualificationSummary.v1.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": true,
  "description": "PBPK-side qualification summary emitted by PBPK MCP.",
  "properties": {
    "assessmentBoundary": {
      "enum": [
        "pbpk-execution-and-qualification-substrate-only",
        "external-pbpk-normalization-only"
      ],
      "type": "string"
    },
    "backend": {
      "$ref": "#/$defs/backend"
    },
    "cautionSummary": {
      "additionalProperties": true,
      "properties": {
        "advisoryCount": {
          "minimum": 0,
          "type": [
            "integer",
            "null"
          ]
        },
        "blockingCount": {
          "minimum": 0,
          "type": [
            "integer",
            "null"
          ]
        },
        "blockingRecommended": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "cautions": {
          "items": {
            "additionalProperties": true,
            "properties": {
              "cautionType": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "code": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "currentStatus": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "handling": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "message": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "requiresHumanReview": {
                "type": [
                  "boolean",
                  "null"
                ]
              },
              "scope": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "severity": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "sourceSurface": {
                "type": [
                  "string",
                  "null"
                ]
              }
            },
            "type": "object"
          },
          "type": "array"
        },
        "highestSeverity": {
          "type": [
            "string",
            "null"
          ]
        },
        "requiresHumanReview": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "summaryVersion": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "type": [
        "object",
        "null"
      ]
    },
    "checklistScore": {
      "type": [
        "number",
        "null"
      ]
    },
    "decisionBoundary": {
      "const": "no-ngra-decision-policy"
    },
    "evidenceBasis": {
      "additionalProperties": true,
      "properties": {
        "basisType": {
          "type": [
            "string",
            "null"
          ]
        },
        "inVivoSupportStatus": {
          "type": [
            "string",
            "null"
          ]
        },
        "iviveLinkageStatus": {
          "type": [
            "string",
            "null"
          ]
        },
        "parameterizationBasis": {
          "type": [
            "string",
            "null"
          ]
        },
        "populationVariabilityStatus": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "type": [
        "object",
        "null"
      ]
    },
    "evidenceStatus": {
      "minLength": 1,
      "type": "string"
    },
    "executableVerificationStatus": {
      "type": [
        "string",
        "null"
      ]
    },
    "exportBlockPolicy": {
      "additionalProperties": true,
      "properties": {
        "blockReasons": {
          "items": {
            "additionalProperties": true,
            "properties": {
              "appliesTo": {
                "$ref": "#/$defs/stringArray"
              },
              "code": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "currentStatus": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "message": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "requiredFields": {
                "$ref": "#/$defs/stringArray"
              },
              "severity": {
                "type": [
                  "string",
                  "null"
                ]
              }
            },
            "type": "object"
          },
          "type": "array"
        },
        "blockedViewModes": {
          "$ref": "#/$defs/stringArray"
        },
        "contextualizedRenderOnly": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "defaultAction": {
          "type": [
            "string",
            "null"
          ]
        },
        "notes": {
          "$ref": "#/$defs/stringArray"
        },
        "policyVersion": {
          "type": [
            "string",
            "null"
          ]
        },
        "requiredFields": {
          "$ref": "#/$defs/stringArray"
        },
        "workflow": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "type": [
        "object",
        "null"
      ]
    },
    "label": {
      "type": [
        "string",
        "null"
      ]
    },
    "limitations": {
      "$ref": "#/$defs/stringArray"
    },
    "missingEvidenceCount": {
      "minimum": 0,
      "type": "integer"
    },
    "objectId": {
      "minLength": 1,
      "type": "string"
    },
    "objectType": {
      "const": "pbpkQualificationSummary.v1"
    },
    "oecdReadiness": {
      "minLength": 1,
      "type": "string"
    },
    "performanceEvidenceBoundary": {
      "type": [
        "string",
        "null"
      ]
    },
    "platformClass": {
      "type": [
        "string",
        "null"
      ]
    },
    "profileSource": {
      "type": [
        "string",
        "null"
      ]
    },
    "qualificationLevel": {
      "minLength": 1,
      "type": "string"
    },
    "requiredExternalInputs": {
      "$ref": "#/$defs/stringArray"
    },
    "reviewStatus": {
      "additionalProperties": true,
      "properties": {
        "declaredStatus": {
          "type": [
            "string",
            "null"
          ]
        },
        "focusTopics": {
          "$ref": "#/$defs/stringArray"
        },
        "priorUseCount": {
          "minimum": 0,
          "type": [
            "integer",
            "null"
          ]
        },
        "requiresReviewerAttention": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "resolvedDissentCount": {
          "minimum": 0,
          "type": [
            "integer",
            "null"
          ]
        },
        "reviewRecordCount": {
          "minimum": 0,
          "type": [
            "integer",
            "null"
          ]
        },
        "revisionEntryCount": {
          "minimum": 0,
          "type": [
            "integer",
            "null"
          ]
        },
        "revisionStatus": {
          "type": [
            "string",
            "null"
          ]
        },
        "status": {
          "type": [
            "string",
            "null"
          ]
        },
        "summary": {
          "type": [
            "string",
            "null"
          ]
        },
        "unresolvedDissentCount": {
          "minimum": 0,
          "type": [
            "integer",
            "null"
          ]
        }
      },
      "type": [
        "object",
        "null"
      ]
    },
    "riskAssessmentReady": {
      "type": "boolean"
    },
    "scientificProfile": {
      "type": "boolean"
    },
    "simulationId": {
      "type": [
        "string",
        "null"
      ]
    },
    "sourcePlatform": {
      "type": [
        "string",
        "null"
      ]
    },
    "state": {
      "minLength": 1,
      "type": "string"
    },
    "summary": {
      "type": [
        "string",
        "null"
      ]
    },
    "supports": {
      "additionalProperties": true,
      "properties": {
        "externalBerHandoff": {
          "type": "boolean"
        },
        "oecdDossierExport": {
          "type": "boolean"
        },
        "regulatoryDecision": {
          "type": "boolean"
        },
        "typedNgraHandoff": {
          "type": "boolean"
        }
      },
      "required": [
        "typedNgraHandoff",
        "oecdDossierExport",
        "externalBerHandoff",
        "regulatoryDecision"
      ],
      "type": "object"
    },
    "validationDecision": {
      "type": [
        "string",
        "null"
      ]
    },
    "validationReferences": {
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "withinDeclaredContext": {
      "type": [
        "boolean",
        "null"
      ]
    },
    "workflowClaimBoundaries": {
      "additionalProperties": true,
      "properties": {
        "directRegulatoryDoseDerivation": {
          "type": [
            "string",
            "null"
          ]
        },
        "exposureLedPrioritization": {
          "type": [
            "string",
            "null"
          ]
        },
        "forwardDosimetry": {
          "type": [
            "string",
            "null"
          ]
        },
        "reverseDosimetry": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "type": [
        "object",
        "null"
      ]
    }
  },
  "required": [
    "objectType",
    "objectId",
    "backend",
    "assessmentBoundary",
    "decisionBoundary",
    "state",
    "qualificationLevel",
    "oecdReadiness",
    "evidenceStatus",
    "missingEvidenceCount",
    "supports",
    "requiredExternalInputs",
    "limitations"
  ],
  "title": "pbpkQualificationSummary.v1",
  "type": "object"
}
""",
    'pointOfDepartureReference.v1': r"""
{
  "$defs": {
    "backend": {
      "enum": [
        "ospsuite",
        "rxode2",
        "external-import"
      ],
      "type": "string"
    },
    "stringArray": {
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "trueDoseAdjustment": {
      "additionalProperties": true,
      "properties": {
        "applied": {
          "type": "boolean"
        },
        "basis": {
          "type": [
            "string",
            "null"
          ]
        },
        "summary": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "applied"
      ],
      "type": "object"
    }
  },
  "$id": "https://raw.githubusercontent.com/ToxMCP/pbpk-mcp/main/schemas/pointOfDepartureReference.v1.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": true,
  "description": "Typed external point-of-departure reference emitted by PBPK MCP.",
  "properties": {
    "assessmentBoundary": {
      "const": "external-pod-reference-only"
    },
    "backend": {
      "$ref": "#/$defs/backend"
    },
    "basis": {
      "type": [
        "string",
        "null"
      ]
    },
    "decisionBoundary": {
      "const": "pod-interpretation-and-ber-policy-owned-by-external-orchestrator"
    },
    "decisionOwner": {
      "const": "external-orchestrator"
    },
    "metric": {
      "type": [
        "string",
        "null"
      ]
    },
    "objectId": {
      "minLength": 1,
      "type": "string"
    },
    "objectType": {
      "const": "pointOfDepartureReference.v1"
    },
    "podRef": {
      "type": [
        "string",
        "null"
      ]
    },
    "requiredExternalInputs": {
      "$ref": "#/$defs/stringArray"
    },
    "simulationId": {
      "type": [
        "string",
        "null"
      ]
    },
    "source": {
      "type": [
        "string",
        "null"
      ]
    },
    "sourcePlatform": {
      "type": [
        "string",
        "null"
      ]
    },
    "status": {
      "enum": [
        "attached-external-reference",
        "not-attached"
      ],
      "type": "string"
    },
    "summary": {
      "type": [
        "string",
        "null"
      ]
    },
    "supports": {
      "additionalProperties": true,
      "properties": {
        "decisionRecommendation": {
          "type": "boolean"
        },
        "externalBerCalculation": {
          "type": "boolean"
        },
        "metricMetadataAttached": {
          "type": "boolean"
        },
        "trueDoseMetadataAttached": {
          "type": "boolean"
        },
        "typedReference": {
          "type": "boolean"
        }
      },
      "required": [
        "typedReference",
        "metricMetadataAttached",
        "trueDoseMetadataAttached",
        "externalBerCalculation",
        "decisionRecommendation"
      ],
      "type": "object"
    },
    "trueDoseAdjustment": {
      "$ref": "#/$defs/trueDoseAdjustment"
    },
    "trueDoseAdjustmentApplied": {
      "type": "boolean"
    },
    "unit": {
      "type": [
        "string",
        "null"
      ]
    },
    "value": {
      "type": [
        "number",
        "null"
      ]
    },
    "warnings": {
      "$ref": "#/$defs/stringArray"
    }
  },
  "required": [
    "objectType",
    "objectId",
    "backend",
    "assessmentBoundary",
    "decisionBoundary",
    "decisionOwner",
    "status",
    "trueDoseAdjustment",
    "trueDoseAdjustmentApplied",
    "supports",
    "requiredExternalInputs",
    "warnings"
  ],
  "title": "pointOfDepartureReference.v1",
  "type": "object"
}
""",
    'uncertaintyHandoff.v1': r"""
{
  "$defs": {
    "backend": {
      "enum": [
        "ospsuite",
        "rxode2",
        "external-import"
      ],
      "type": "string"
    },
    "stringArray": {
      "items": {
        "type": "string"
      },
      "type": "array"
    }
  },
  "$id": "https://raw.githubusercontent.com/ToxMCP/pbpk-mcp/main/schemas/uncertaintyHandoff.v1.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": true,
  "description": "PBPK-to-cross-domain uncertainty handoff object emitted by PBPK MCP.",
  "properties": {
    "assessmentBoundary": {
      "const": "pbpk-to-cross-domain-uncertainty-handoff-only"
    },
    "backend": {
      "$ref": "#/$defs/backend"
    },
    "blockingReasons": {
      "$ref": "#/$defs/stringArray"
    },
    "decisionBoundary": {
      "const": "cross-domain-uncertainty-synthesis-owned-by-external-orchestrator"
    },
    "decisionOwner": {
      "const": "external-orchestrator"
    },
    "internalExposureEstimateRef": {
      "type": [
        "string",
        "null"
      ]
    },
    "objectId": {
      "minLength": 1,
      "type": "string"
    },
    "objectType": {
      "const": "uncertaintyHandoff.v1"
    },
    "pbpkQualificationSummaryRef": {
      "type": [
        "string",
        "null"
      ]
    },
    "pointOfDepartureReferenceRef": {
      "type": [
        "string",
        "null"
      ]
    },
    "requiredExternalInputs": {
      "$ref": "#/$defs/stringArray"
    },
    "simulationId": {
      "type": [
        "string",
        "null"
      ]
    },
    "sourcePlatform": {
      "type": [
        "string",
        "null"
      ]
    },
    "status": {
      "minLength": 1,
      "type": "string"
    },
    "supports": {
      "additionalProperties": true,
      "properties": {
        "crossDomainUncertaintySynthesis": {
          "type": "boolean"
        },
        "decisionRecommendation": {
          "type": "boolean"
        },
        "pbpkQualificationAttached": {
          "type": "boolean"
        },
        "pbpkUncertaintySummaryAttached": {
          "type": "boolean"
        },
        "typedUncertaintySemanticsAttached": {
          "type": "boolean"
        }
      },
      "required": [
        "pbpkQualificationAttached",
        "pbpkUncertaintySummaryAttached",
        "typedUncertaintySemanticsAttached",
        "crossDomainUncertaintySynthesis",
        "decisionRecommendation"
      ],
      "type": "object"
    },
    "uncertaintyRegisterReferenceRef": {
      "type": [
        "string",
        "null"
      ]
    },
    "uncertaintySummaryRef": {
      "type": [
        "string",
        "null"
      ]
    }
  },
  "required": [
    "objectType",
    "objectId",
    "backend",
    "assessmentBoundary",
    "decisionBoundary",
    "decisionOwner",
    "status",
    "supports",
    "requiredExternalInputs",
    "blockingReasons"
  ],
  "title": "uncertaintyHandoff.v1",
  "type": "object"
}
""",
    'uncertaintyRegisterReference.v1': r"""
{
  "$defs": {
    "backend": {
      "enum": [
        "ospsuite",
        "rxode2",
        "external-import"
      ],
      "type": "string"
    },
    "stringArray": {
      "items": {
        "type": "string"
      },
      "type": "array"
    }
  },
  "$id": "https://raw.githubusercontent.com/ToxMCP/pbpk-mcp/main/schemas/uncertaintyRegisterReference.v1.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": true,
  "description": "Typed external uncertainty-register reference emitted by PBPK MCP.",
  "properties": {
    "assessmentBoundary": {
      "const": "external-uncertainty-register-reference-only"
    },
    "backend": {
      "$ref": "#/$defs/backend"
    },
    "decisionBoundary": {
      "const": "cross-domain-uncertainty-synthesis-owned-by-external-orchestrator"
    },
    "decisionOwner": {
      "const": "external-orchestrator"
    },
    "objectId": {
      "minLength": 1,
      "type": "string"
    },
    "objectType": {
      "const": "uncertaintyRegisterReference.v1"
    },
    "owner": {
      "type": [
        "string",
        "null"
      ]
    },
    "registerRef": {
      "type": [
        "string",
        "null"
      ]
    },
    "requiredExternalInputs": {
      "$ref": "#/$defs/stringArray"
    },
    "scope": {
      "type": [
        "string",
        "null"
      ]
    },
    "simulationId": {
      "type": [
        "string",
        "null"
      ]
    },
    "source": {
      "type": [
        "string",
        "null"
      ]
    },
    "sourcePlatform": {
      "type": [
        "string",
        "null"
      ]
    },
    "status": {
      "enum": [
        "attached-external-reference",
        "not-attached"
      ],
      "type": "string"
    },
    "summary": {
      "type": [
        "string",
        "null"
      ]
    },
    "supports": {
      "additionalProperties": true,
      "properties": {
        "crossDomainUncertaintySynthesis": {
          "type": "boolean"
        },
        "decisionRecommendation": {
          "type": "boolean"
        },
        "typedReference": {
          "type": "boolean"
        }
      },
      "required": [
        "typedReference",
        "crossDomainUncertaintySynthesis",
        "decisionRecommendation"
      ],
      "type": "object"
    },
    "warnings": {
      "$ref": "#/$defs/stringArray"
    }
  },
  "required": [
    "objectType",
    "objectId",
    "backend",
    "assessmentBoundary",
    "decisionBoundary",
    "decisionOwner",
    "status",
    "supports",
    "requiredExternalInputs",
    "warnings"
  ],
  "title": "uncertaintyRegisterReference.v1",
  "type": "object"
}
""",
    'uncertaintySummary.v1': r"""
{
  "$defs": {
    "backend": {
      "enum": [
        "ospsuite",
        "rxode2",
        "external-import"
      ],
      "type": "string"
    },
    "stringArray": {
      "items": {
        "type": "string"
      },
      "type": "array"
    }
  },
  "$id": "https://raw.githubusercontent.com/ToxMCP/pbpk-mcp/main/schemas/uncertaintySummary.v1.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "additionalProperties": true,
  "description": "PBPK-side uncertainty summary emitted by PBPK MCP.",
  "properties": {
    "assessmentBoundary": {
      "const": "pbpk-side-uncertainty-summary-only"
    },
    "backend": {
      "$ref": "#/$defs/backend"
    },
    "bundleMetadata": {
      "additionalProperties": true,
      "type": [
        "object",
        "null"
      ]
    },
    "decisionBoundary": {
      "const": "no-ngra-decision-policy"
    },
    "evidenceRowCount": {
      "minimum": 0,
      "type": "integer"
    },
    "evidenceSource": {
      "type": [
        "string",
        "null"
      ]
    },
    "hasResidualUncertainty": {
      "type": "boolean"
    },
    "hasSensitivityAnalysis": {
      "type": "boolean"
    },
    "hasVariabilityApproach": {
      "type": "boolean"
    },
    "hasVariabilityPropagation": {
      "type": "boolean"
    },
    "issueCount": {
      "minimum": 0,
      "type": "integer"
    },
    "objectId": {
      "minLength": 1,
      "type": "string"
    },
    "objectType": {
      "const": "uncertaintySummary.v1"
    },
    "requiredExternalInputs": {
      "$ref": "#/$defs/stringArray"
    },
    "residualUncertaintyStatus": {
      "type": [
        "string",
        "null"
      ]
    },
    "semanticCoverage": {
      "additionalProperties": true,
      "properties": {
        "declaredOnlyComponents": {
          "$ref": "#/$defs/stringArray"
        },
        "declaredOnlyRowCount": {
          "minimum": 0,
          "type": "integer"
        },
        "overallQuantificationStatus": {
          "minLength": 1,
          "type": "string"
        },
        "quantifiedComponents": {
          "$ref": "#/$defs/stringArray"
        },
        "quantifiedRowCount": {
          "minimum": 0,
          "type": "integer"
        },
        "residualUncertaintyQuantificationStatus": {
          "minLength": 1,
          "type": "string"
        },
        "residualUncertaintyType": {
          "minLength": 1,
          "type": "string"
        },
        "sensitivityQuantificationStatus": {
          "minLength": 1,
          "type": "string"
        },
        "sensitivityType": {
          "minLength": 1,
          "type": "string"
        },
        "variabilityQuantificationStatus": {
          "minLength": 1,
          "type": "string"
        },
        "variabilityType": {
          "minLength": 1,
          "type": "string"
        }
      },
      "required": [
        "overallQuantificationStatus",
        "variabilityType",
        "sensitivityType",
        "residualUncertaintyType",
        "variabilityQuantificationStatus",
        "sensitivityQuantificationStatus",
        "residualUncertaintyQuantificationStatus",
        "quantifiedRowCount",
        "declaredOnlyRowCount",
        "quantifiedComponents",
        "declaredOnlyComponents"
      ],
      "type": "object"
    },
    "sensitivityStatus": {
      "type": [
        "string",
        "null"
      ]
    },
    "simulationId": {
      "type": [
        "string",
        "null"
      ]
    },
    "sourcePlatform": {
      "type": [
        "string",
        "null"
      ]
    },
    "sources": {
      "$ref": "#/$defs/stringArray"
    },
    "status": {
      "minLength": 1,
      "type": "string"
    },
    "summary": {
      "type": [
        "string",
        "null"
      ]
    },
    "supports": {
      "additionalProperties": true,
      "properties": {
        "decisionRecommendation": {
          "type": "boolean"
        },
        "typedNgraHandoff": {
          "type": "boolean"
        },
        "typedUncertaintySemantics": {
          "type": "boolean"
        }
      },
      "required": [
        "typedUncertaintySemantics",
        "typedNgraHandoff",
        "decisionRecommendation"
      ],
      "type": "object"
    },
    "totalEvidenceRows": {
      "minimum": 0,
      "type": "integer"
    },
    "variabilityStatus": {
      "type": [
        "string",
        "null"
      ]
    }
  },
  "required": [
    "objectType",
    "objectId",
    "backend",
    "assessmentBoundary",
    "decisionBoundary",
    "status",
    "evidenceRowCount",
    "totalEvidenceRows",
    "semanticCoverage",
    "supports",
    "requiredExternalInputs"
  ],
  "title": "uncertaintySummary.v1",
  "type": "object"
}
""",
}

_SCHEMA_EXAMPLE_JSON = {
    'assessmentContext.v1': r"""
{
  "assessmentBoundary": "pbpk-context-alignment-only",
  "backend": "external-import",
  "contextOfUse": {
    "decisionContext": {
      "declared": null,
      "effective": "BER handoff",
      "requested": "BER handoff"
    },
    "regulatoryUse": {
      "declared": null,
      "effective": "research-only",
      "requested": "research-only"
    },
    "scientificPurpose": {
      "declared": null,
      "effective": "Tier 1 internal exposure screening",
      "requested": "Tier 1 internal exposure screening"
    }
  },
  "decisionBoundary": "no-ngra-decision-policy",
  "domain": {
    "compound": {
      "declared": null,
      "effective": null,
      "requested": null
    },
    "lifeStage": {
      "declared": null,
      "effective": null,
      "requested": null
    },
    "population": {
      "declared": "adult",
      "effective": "adult",
      "requested": "adult"
    },
    "route": {
      "declared": "oral",
      "effective": "oral",
      "requested": "oral"
    },
    "species": {
      "declared": "human",
      "effective": "human",
      "requested": "human"
    }
  },
  "doseScenario": null,
  "objectId": "gastroplus-assessment-context",
  "objectType": "assessmentContext.v1",
  "populationSupport": {
    "extrapolationPolicy": "outside-declared-population-context-requires-human-review",
    "supportedGenotypesOrPhenotypes": [],
    "supportedLifeStages": [],
    "supportedPhysiologyContexts": [],
    "supportedSpecies": [
      "human"
    ],
    "variabilityRepresentation": "not-declared"
  },
  "simulationId": null,
  "sourcePlatform": "GastroPlus",
  "supports": {
    "decisionRecommendation": false,
    "declaredProfileComparison": true,
    "requestContextAlignment": true,
    "typedNgraHandoff": true
  },
  "targetOutput": {
    "declared": [
      "Plasma|Parent|Concentration"
    ],
    "requested": "Plasma|Parent|Concentration"
  },
  "validationDecision": null,
  "workflowRole": {
    "downstreamOutputs": [
      "internal exposure estimates",
      "PBPK qualification and uncertainty handoff objects",
      "BER-ready input bundle when compatible external PoD metadata are attached"
    ],
    "nonGoals": [
      "standalone weight-of-evidence integration",
      "standalone exposure assessment ownership",
      "direct regulatory decision authority",
      "standalone hazard or AOP interpretation"
    ],
    "role": "pbpk-exposure-translation-and-internal-dose-support",
    "upstreamDependencies": [
      "dose scenario or exposure estimate defined outside PBPK MCP",
      "in vitro ADME or IVIVE parameterization evidence defined outside PBPK MCP",
      "bioactivity, point-of-departure, or NAM interpretation defined outside PBPK MCP"
    ],
    "workflow": "exposure-led-ngra"
  }
}
""",
    'berInputBundle.v1': r"""
{
  "assessmentBoundary": "external-ber-calculation-only",
  "backend": "external-import",
  "blockingReasons": [],
  "comparisonMetric": "cmax",
  "decisionBoundary": "ber-calculation-and-decision-owned-by-external-orchestrator",
  "decisionOwner": "external-orchestrator",
  "internalExposureEstimateRef": "gastroplus-internal-exposure-estimate",
  "internalExposureMetric": {
    "metric": "cmax",
    "outputPath": "Plasma|Parent|Concentration",
    "unit": "uM",
    "value": 3.2
  },
  "objectId": "gastroplus-ber-input-bundle",
  "objectType": "berInputBundle.v1",
  "podMetadata": {
    "basis": "true-dose-adjusted",
    "metric": "cmax",
    "ref": "pod-001",
    "source": "httr-benchmark",
    "summary": null,
    "unit": "uM",
    "value": null
  },
  "podRef": "pod-001",
  "pointOfDepartureReferenceRef": "gastroplus-point-of-departure-reference",
  "qualificationSummaryRef": "gastroplus-qualification-summary",
  "requiredExternalInputs": [
    "BER calculation and decision policy outside PBPK MCP"
  ],
  "simulationId": null,
  "sourcePlatform": "GastroPlus",
  "status": "ready-for-external-ber-calculation",
  "supports": {
    "decisionRecommendation": false,
    "externalBerCalculation": true,
    "externalPodReferenceAttached": true,
    "internalExposureMetricAttached": true,
    "trueDoseMetadataAttached": true
  },
  "trueDoseAdjustment": {
    "applied": true,
    "basis": "free-concentration",
    "summary": "Normalized to free concentration"
  },
  "trueDoseAdjustmentApplied": true,
  "uncertaintySummaryRef": "gastroplus-uncertainty-summary",
  "warnings": []
}
""",
    'internalExposureEstimate.v1': r"""
{
  "analyte": null,
  "assessmentBoundary": "pbpk-side-internal-exposure-estimate-only",
  "backend": "external-import",
  "candidateOutputCount": 1,
  "candidateOutputs": [
    {
      "auc0Tlast": 10.5,
      "aucUnitBasis": "uM*h",
      "cmax": 3.2,
      "outputPath": "Plasma|Parent|Concentration",
      "pointCount": 0,
      "tmax": 1.5,
      "unit": "uM"
    }
  ],
  "candidateOutputsTruncated": false,
  "decisionBoundary": "no-ngra-decision-policy",
  "distribution": null,
  "doseScenario": null,
  "objectId": "gastroplus-internal-exposure-estimate",
  "objectType": "internalExposureEstimate.v1",
  "population": "adult",
  "requestedTargetOutput": "Plasma|Parent|Concentration",
  "resultsId": null,
  "route": "oral",
  "selectedOutput": {
    "auc0Tlast": 10.5,
    "aucUnitBasis": "uM*h",
    "cmax": 3.2,
    "outputPath": "Plasma|Parent|Concentration",
    "pointCount": 0,
    "tmax": 1.5,
    "unit": "uM"
  },
  "selectionStatus": "explicit",
  "simulationId": null,
  "source": "external-import",
  "sourcePlatform": "GastroPlus",
  "species": "human",
  "status": "available",
  "supports": {
    "decisionRecommendation": false,
    "deterministicMetricSelection": true,
    "externalBerHandoff": true,
    "populationDistributionSummary": false
  },
  "warnings": []
}
""",
    'pbpkQualificationSummary.v1': r"""
{
  "assessmentBoundary": "external-pbpk-normalization-only",
  "backend": "external-import",
  "cautionSummary": {
    "advisoryCount": 1,
    "blockingCount": 3,
    "blockingRecommended": true,
    "cautions": [
      {
        "cautionType": "summary-transport-risk",
        "code": "detached-summary-overread",
        "currentStatus": "detached-summary-unsafe",
        "handling": "blocking",
        "message": "Thin report cards, screenshots, or forwarded imported summaries can detach the trust-bearing PBPK label from the caveats it needs.",
        "requiresHumanReview": true,
        "scope": "summary-surface",
        "severity": "high",
        "sourceSurface": "exportBlockPolicy"
      },
      {
        "cautionType": "decision-overclaim-risk",
        "code": "direct-regulatory-dose-derivation-blocked",
        "currentStatus": "not-supported",
        "handling": "blocking",
        "message": "Imported PBPK outputs should not be presented as direct regulatory dose derivations or final decision recommendations.",
        "requiresHumanReview": true,
        "scope": "workflow-claim",
        "severity": "high",
        "sourceSurface": "workflowClaimBoundaries"
      },
      {
        "cautionType": "decision-overclaim-risk",
        "code": "risk-assessment-ready-overclaim",
        "currentStatus": "research-use",
        "handling": "blocking",
        "message": "Imported qualification remains bounded, so decision-ready or regulatory-ready framing should stay blocked.",
        "requiresHumanReview": true,
        "scope": "workflow-claim",
        "severity": "high",
        "sourceSurface": "qualificationState"
      },
      {
        "cautionType": "parameter-transfer-uncertainty",
        "code": "parameter-transfer-uncertainty",
        "currentStatus": "in-vitro-adme-and-literature",
        "handling": "advisory",
        "message": "Parameterization depends on transferred, literature-derived, or default assumptions, so parameter-transfer uncertainty should be reviewed before stronger claims.",
        "requiresHumanReview": true,
        "scope": "model",
        "severity": "medium",
        "sourceSurface": "evidenceBasis"
      }
    ],
    "highestSeverity": "high",
    "requiresHumanReview": true,
    "summaryVersion": "pbpk-caution-summary.v1"
  },
  "checklistScore": null,
  "decisionBoundary": "no-ngra-decision-policy",
  "evidenceBasis": {
    "basisType": "external-imported",
    "inVivoSupportStatus": "no-direct-in-vivo-support",
    "iviveLinkageStatus": "external-ivive-linkage-declared",
    "parameterizationBasis": "in-vitro-adme-and-literature",
    "populationVariabilityStatus": "declared-or-characterized"
  },
  "evidenceStatus": "checked",
  "executableVerificationStatus": "checked",
  "exportBlockPolicy": {
    "blockReasons": [
      {
        "appliesTo": [
          "report-card",
          "screenshot",
          "chat-snippet",
          "forwarded-bundle",
          "thin-api-response"
        ],
        "code": "detached-summary-blocked",
        "currentStatus": "high",
        "message": "Block lossy report cards, screenshots, chat snippets, or forwarded bundles when qualification state, review status, evidence basis, claim boundaries, and anti-misread guidance cannot travel with them.",
        "requiredFields": [
          "qualificationState",
          "reviewStatus",
          "evidenceBasis",
          "claimBoundaries",
          "misreadRiskSummary.plainLanguageSummary",
          "summaryTransportRisk.plainLanguageSummary"
        ],
        "severity": "high"
      },
      {
        "appliesTo": [
          "regulatory-dose-claim",
          "regulatory-decision-summary",
          "decision-recommendation"
        ],
        "code": "direct-regulatory-dose-derivation-blocked",
        "currentStatus": "not-supported",
        "message": "Block downstream presentations that frame this PBPK output as a direct regulatory dose derivation or final decision recommendation.",
        "severity": "high"
      }
    ],
    "blockedViewModes": [
      "report-card",
      "screenshot",
      "chat-snippet",
      "forwarded-bundle",
      "thin-api-response"
    ],
    "contextualizedRenderOnly": true,
    "defaultAction": "block-lossy-or-decision-leaning-exports",
    "notes": [
      "This policy is descriptive and machine-readable so analyst-facing clients can refuse unsafe thin views.",
      "Imported or operator-reviewed state does not create regulatory decision authority inside PBPK MCP."
    ],
    "policyVersion": "pbpk-export-block-policy.v1",
    "requiredFields": [
      "qualificationState",
      "reviewStatus",
      "evidenceBasis",
      "claimBoundaries",
      "misreadRiskSummary.plainLanguageSummary",
      "summaryTransportRisk.plainLanguageSummary"
    ],
    "workflow": "exposure-led-ngra"
  },
  "label": "Research Use",
  "limitations": [
    "Imported performance evidence is limited to runtime or internal supporting evidence."
  ],
  "missingEvidenceCount": 0,
  "objectId": "gastroplus-qualification-summary",
  "objectType": "pbpkQualificationSummary.v1",
  "oecdReadiness": "external-imported",
  "performanceEvidenceBoundary": "runtime-or-internal-evidence-only",
  "platformClass": "commercial",
  "profileSource": "external-import",
  "qualificationLevel": "L2",
  "requiredExternalInputs": [
    "higher-level NGRA decision policy or orchestrator outside PBPK MCP",
    "observed-vs-predicted, predictive-dataset, or external qualification evidence"
  ],
  "reviewStatus": {
    "declaredStatus": "unreported",
    "focusTopics": [],
    "priorUseCount": 0,
    "requiresReviewerAttention": true,
    "resolvedDissentCount": 0,
    "reviewRecordCount": 0,
    "revisionEntryCount": 0,
    "revisionStatus": null,
    "status": "not-declared",
    "summary": "No peer-review, reviewer stance, or prior-use workflow metadata are declared.",
    "unresolvedDissentCount": 0
  },
  "riskAssessmentReady": false,
  "scientificProfile": true,
  "simulationId": null,
  "sourcePlatform": "GastroPlus",
  "state": "research-use",
  "summary": "External PBPK qualification metadata were normalized without executing the upstream platform.",
  "supports": {
    "executableVerification": false,
    "externalBerHandoff": true,
    "externalImportNormalization": true,
    "manifestValidation": false,
    "nativeExecution": false,
    "oecdDossierExport": true,
    "preflightValidation": false,
    "regulatoryDecision": false,
    "typedNgraHandoff": true
  },
  "validationDecision": null,
  "validationReferences": [],
  "withinDeclaredContext": null,
  "workflowClaimBoundaries": {
    "directRegulatoryDoseDerivation": "not-supported",
    "exposureLedPrioritization": "supported-only-as-pbpk-substrate-with-external-orchestrator",
    "forwardDosimetry": "external-imported-not-executed-by-pbpk-mcp",
    "reverseDosimetry": "not-performed-directly-external-workflow-required"
  }
}
""",
    'pointOfDepartureReference.v1': r"""
{
  "assessmentBoundary": "external-pod-reference-only",
  "backend": "external-import",
  "basis": "true-dose-adjusted",
  "decisionBoundary": "pod-interpretation-and-ber-policy-owned-by-external-orchestrator",
  "decisionOwner": "external-orchestrator",
  "metric": "cmax",
  "objectId": "gastroplus-point-of-departure-reference",
  "objectType": "pointOfDepartureReference.v1",
  "podRef": "pod-001",
  "requiredExternalInputs": [
    "PoD interpretation and suitability assessment outside PBPK MCP",
    "BER calculation and decision policy outside PBPK MCP"
  ],
  "simulationId": null,
  "source": "httr-benchmark",
  "sourcePlatform": "GastroPlus",
  "status": "attached-external-reference",
  "summary": null,
  "supports": {
    "decisionRecommendation": false,
    "externalBerCalculation": false,
    "metricMetadataAttached": true,
    "trueDoseMetadataAttached": true,
    "typedReference": true
  },
  "trueDoseAdjustment": {
    "applied": true,
    "basis": "free-concentration",
    "summary": "Normalized to free concentration"
  },
  "trueDoseAdjustmentApplied": true,
  "unit": "uM",
  "value": null,
  "warnings": []
}
""",
    'uncertaintyHandoff.v1': r"""
{
  "assessmentBoundary": "pbpk-to-cross-domain-uncertainty-handoff-only",
  "backend": "external-import",
  "blockingReasons": [],
  "decisionBoundary": "cross-domain-uncertainty-synthesis-owned-by-external-orchestrator",
  "decisionOwner": "external-orchestrator",
  "internalExposureEstimateRef": "gastroplus-internal-exposure-estimate",
  "objectId": "gastroplus-uncertainty-handoff",
  "objectType": "uncertaintyHandoff.v1",
  "pbpkQualificationSummaryRef": "gastroplus-qualification-summary",
  "pointOfDepartureReferenceRef": "gastroplus-point-of-departure-reference",
  "requiredExternalInputs": [
    "cross-domain uncertainty synthesis outside PBPK MCP",
    "exposure-scenario uncertainty outside PBPK MCP",
    "PoD or NAM uncertainty outside PBPK MCP"
  ],
  "simulationId": null,
  "sourcePlatform": "GastroPlus",
  "status": "ready-for-cross-domain-uncertainty-synthesis",
  "supports": {
    "classifiedResidualUncertaintySummaryAttached": true,
    "classifiedVariabilitySummaryAttached": true,
    "crossDomainUncertaintySynthesis": false,
    "decisionRecommendation": false,
    "internalExposureContextAttached": true,
    "pbpkQualificationAttached": true,
    "pbpkUncertaintySummaryAttached": true,
    "pointOfDepartureReferenceAttached": true,
    "quantifiedPbpkResidualUncertainty": false,
    "quantifiedPbpkSensitivity": false,
    "quantifiedPbpkVariability": true,
    "residualUncertaintyTracked": true,
    "typedUncertaintySemanticsAttached": true,
    "uncertaintyRegisterReferenceAttached": true
  },
  "uncertaintyRegisterReferenceRef": "gastroplus-uncertainty-register-reference",
  "uncertaintySummaryRef": "gastroplus-uncertainty-summary"
}
""",
    'uncertaintyRegisterReference.v1': r"""
{
  "assessmentBoundary": "external-uncertainty-register-reference-only",
  "backend": "external-import",
  "decisionBoundary": "cross-domain-uncertainty-synthesis-owned-by-external-orchestrator",
  "decisionOwner": "external-orchestrator",
  "objectId": "gastroplus-uncertainty-register-reference",
  "objectType": "uncertaintyRegisterReference.v1",
  "owner": null,
  "registerRef": "unc-reg-001",
  "requiredExternalInputs": [
    "cross-domain uncertainty synthesis outside PBPK MCP"
  ],
  "scope": "tier-1-systemic",
  "simulationId": null,
  "source": "assessment-workbench",
  "sourcePlatform": "GastroPlus",
  "status": "attached-external-reference",
  "summary": null,
  "supports": {
    "crossDomainUncertaintySynthesis": false,
    "decisionRecommendation": false,
    "typedReference": true
  },
  "warnings": []
}
""",
    'uncertaintySummary.v1': r"""
{
  "assessmentBoundary": "pbpk-side-uncertainty-summary-only",
  "backend": "external-import",
  "bundleMetadata": null,
  "decisionBoundary": "no-ngra-decision-policy",
  "evidenceRowCount": 2,
  "evidenceSource": "external-import",
  "hasResidualUncertainty": true,
  "hasSensitivityAnalysis": false,
  "hasVariabilityApproach": false,
  "hasVariabilityPropagation": true,
  "issueCount": 0,
  "objectId": "gastroplus-uncertainty-summary",
  "objectType": "uncertaintySummary.v1",
  "requiredExternalInputs": [
    "cross-domain uncertainty synthesis outside PBPK MCP"
  ],
  "residualUncertaintyStatus": "declared",
  "semanticCoverage": {
    "declaredOnlyComponents": [
      "residual-uncertainty"
    ],
    "declaredOnlyRowCount": 1,
    "overallQuantificationStatus": "partially-quantified",
    "quantifiedComponents": [
      "variability"
    ],
    "quantifiedRowCount": 1,
    "residualUncertaintyQuantificationStatus": "declared-only",
    "residualUncertaintyType": "declared-residual-uncertainty",
    "sensitivityQuantificationStatus": "unreported",
    "sensitivityType": "unreported",
    "variabilityQuantificationStatus": "quantified",
    "variabilityType": "aleatoric-or-population-variability"
  },
  "sensitivityStatus": "not-bundled",
  "simulationId": null,
  "sourcePlatform": "GastroPlus",
  "sources": [],
  "status": "declared",
  "summary": "Imported uncertainty summary",
  "supports": {
    "classifiedResidualUncertainty": true,
    "classifiedVariability": true,
    "crossDomainUncertaintyRegister": false,
    "decisionRecommendation": false,
    "qualitativeSummary": true,
    "quantifiedResidualUncertainty": false,
    "quantifiedSensitivity": false,
    "quantifiedVariability": true,
    "quantitativePropagation": true,
    "residualUncertaintyTracking": true,
    "sensitivityAnalysis": false,
    "typedNgraHandoff": true,
    "typedUncertaintySemantics": true,
    "variabilityCharacterization": false
  },
  "totalEvidenceRows": 2,
  "variabilityStatus": "propagated"
}
""",
}

def capability_matrix_document() -> dict[str, object]:
    return json.loads(_CAPABILITY_MATRIX_JSON)

def contract_manifest_document() -> dict[str, object]:
    return json.loads(_CONTRACT_MANIFEST_JSON)

def release_bundle_manifest_document() -> dict[str, object]:
    return json.loads(_RELEASE_BUNDLE_MANIFEST_JSON)

def schema_documents() -> dict[str, dict]:
    return {key: json.loads(value) for key, value in _SCHEMA_JSON.items()}

def schema_examples() -> dict[str, dict]:
    return {key: json.loads(value) for key, value in _SCHEMA_EXAMPLE_JSON.items()}
