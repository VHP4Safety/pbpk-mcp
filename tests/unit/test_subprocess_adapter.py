"""Tests for the subprocess-backed ospsuite adapter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import pytest

from mcp_bridge.adapter import AdapterConfig, AdapterError, AdapterErrorCode
from mcp_bridge.adapter.environment import REnvironmentStatus
from mcp_bridge.adapter.mock import InMemoryAdapter
from mcp_bridge.adapter.ospsuite import CommandResult, SubprocessOspsuiteAdapter
from mcp_bridge.adapter.schema import (
    ParameterSummary,
    ParameterValue,
    PopulationCohortConfig,
    PopulationOutputsConfig,
    PopulationSimulationConfig,
)
from mcp_bridge.storage.population_store import PopulationResultStore

DEFAULT_PARAMS = {
    "Organ.Liver.Volume": {"value": 1.6, "unit": "L", "displayName": "Liver Volume"},
    "Protein.Plasma.Albumin": {"value": 45.0, "unit": "g/L", "displayName": "Albumin"},
}


def _fake_env_detector(_: AdapterConfig) -> REnvironmentStatus:
    status = REnvironmentStatus(
        available=True,
        r_path="/usr/bin/R",
        ospsuite_libs="/opt/ospsuite",
        r_version="4.3.2",
        ospsuite_available=True,
        issues=[],
    )
    return status


class FakeBridgeRunner:
    """Command runner that proxies to the in-memory adapter for deterministic behaviour."""

    def __init__(self) -> None:
        self._adapter = InMemoryAdapter()
        self._adapter.init()
        self._metadata: dict[str, dict[str, Any]] = {}

    def __call__(self, action: str, payload: Mapping[str, Any]) -> CommandResult:
        try:
            if action == "load_simulation":
                handle = self._adapter.load_simulation(
                    payload["filePath"], simulation_id=payload["simulationId"]
                )
                params = []
                for path, details in DEFAULT_PARAMS.items():
                    value = self._adapter.set_parameter_value(
                        handle.simulation_id,
                        path,
                        details["value"],
                        unit=details["unit"],
                        comment=details["displayName"],
                    )
                    params.append(value.model_dump())
                self._metadata[handle.simulation_id] = {
                    "filePath": payload["filePath"],
                    "parameterCount": len(params),
                }
                body = {
                    "handle": handle.model_dump(),
                    "parameters": params,
                    "metadata": self._metadata[handle.simulation_id],
                }
            elif action == "list_parameters":
                params = self._adapter.list_parameters(
                    payload["simulationId"], payload.get("pattern")
                )
                body = {"parameters": [item.model_dump() for item in params]}
            elif action == "get_parameter_value":
                value = self._adapter.get_parameter_value(
                    payload["simulationId"], payload["parameterPath"]
                )
                body = {"parameter": value.model_dump()}
            elif action == "set_parameter_value":
                value = self._adapter.set_parameter_value(
                    payload["simulationId"],
                    payload["parameterPath"],
                    payload["value"],
                    unit=payload.get("unit"),
                    comment=payload.get("comment"),
                )
                body = {"parameter": value.model_dump()}
            elif action == "run_simulation_sync":
                result = self._adapter.run_simulation_sync(
                    payload["simulationId"], run_id=payload.get("runId")
                )
                body = {"result": result.model_dump()}
            elif action == "get_results":
                result = self._adapter.get_results(payload["resultsId"])
                body = {"result": result.model_dump()}
            elif action == "validate_simulation_request":
                body = self._adapter.validate_simulation_request(
                    payload["simulationId"],
                    request=payload.get("request"),
                    stage=payload.get("stage"),
                )
            elif action == "run_verification_checks":
                body = self._adapter.run_verification_checks(
                    payload["simulationId"],
                    request=payload.get("request"),
                    include_population_smoke=bool(payload.get("includePopulationSmoke")),
                    population_cohort=payload.get("populationCohort"),
                    population_outputs=payload.get("populationOutputs"),
                )
            elif action == "export_oecd_report":
                body = self._adapter.export_oecd_report(
                    payload["simulationId"],
                    request=payload.get("request"),
                    include_parameter_table=bool(payload.get("includeParameterTable", True)),
                    parameter_pattern=payload.get("parameterPattern"),
                    parameter_limit=int(payload.get("parameterLimit", 200)),
                )
            elif action == "run_population_simulation_sync":
                config = PopulationSimulationConfig(
                    model_path=payload["modelPath"],
                    simulation_id=payload["simulationId"],
                    cohort=PopulationCohortConfig.model_validate(payload["cohort"]),
                    outputs=PopulationOutputsConfig.model_validate(payload.get("outputs", {})),
                    metadata=dict(payload.get("metadata", {})),
                )
                result = self._adapter.run_population_simulation_sync(config)
                result_payload = result.model_dump(by_alias=True, mode="json")
                result_payload["chunk_handles"] = [
                    {
                        "chunkId": handle.chunk_id,
                        "subjectRange": list(handle.subject_range)
                        if handle.subject_range
                        else None,
                        "timeRange": list(handle.time_range) if handle.time_range else None,
                        "preview": handle.preview,
                        "payload": self._adapter._population_chunks.get(handle.chunk_id),
                    }
                    for handle in result.chunk_handles
                ]
                body = {"result": result_payload}
            elif action == "get_population_results":
                result = self._adapter.get_population_results(payload["resultsId"])
                result_payload = result.model_dump(by_alias=True, mode="json")
                result_payload["chunk_handles"] = [
                    {
                        "chunkId": handle.chunk_id,
                        "subjectRange": list(handle.subject_range)
                        if handle.subject_range
                        else None,
                        "timeRange": list(handle.time_range) if handle.time_range else None,
                        "preview": handle.preview,
                        "payload": self._adapter._population_chunks.get(handle.chunk_id),
                    }
                    for handle in result.chunk_handles
                ]
                body = {"result": result_payload}
            else:
                raise ValueError(f"Unknown action '{action}'")
            return CommandResult(returncode=0, stdout=json.dumps(body))
        except AdapterError as exc:
            return CommandResult(
                returncode=0,
                stdout=json.dumps(
                    {
                        "error": {
                            "code": exc.code.value,
                            "message": exc.args[0],
                            "details": exc.details,
                        }
                    }
                ),
            )
        except Exception as exc:  # pragma: no cover - defensive
            return CommandResult(returncode=1, stdout="", stderr=str(exc))


class ExplodingRunner:
    """Runner that always fails to exercise error mapping."""

    def __call__(self, _: str, __: Mapping[str, Any]) -> CommandResult:
        return CommandResult(returncode=1, stdout="", stderr="boom")


@pytest.fixture()
def temp_pkml(tmp_path: Path) -> Path:
    file_path = tmp_path / "demo.pkml"
    file_path.write_text("<pkml/>", encoding="utf-8")
    return file_path


def test_load_simulation_populates_cache(temp_pkml: Path) -> None:
    adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(temp_pkml.parent),)),
        command_runner=FakeBridgeRunner(),
        env_detector=_fake_env_detector,
    )
    adapter.init()

    handle = adapter.load_simulation(str(temp_pkml), simulation_id="demo")

    assert handle.simulation_id == "demo"
    assert adapter.health()["status"] == "initialised"

    summaries = adapter.list_parameters("demo")
    assert summaries
    assert all(isinstance(item, ParameterSummary) for item in summaries)

    value = adapter.get_parameter_value("demo", summaries[0].path)
    assert isinstance(value, ParameterValue)


def test_set_parameter_updates_cache(temp_pkml: Path) -> None:
    runner = FakeBridgeRunner()
    adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(temp_pkml.parent),)),
        command_runner=runner,
        env_detector=_fake_env_detector,
    )
    adapter.init()
    adapter.load_simulation(str(temp_pkml), simulation_id="demo")

    updated = adapter.set_parameter_value("demo", "Organ.Liver.Volume", 2.1, unit="L")
    fetched = adapter.get_parameter_value("demo", "Organ.Liver.Volume")

    assert updated.value == pytest.approx(2.1)
    assert fetched.value == pytest.approx(2.1)


def test_run_simulation_caches_results(temp_pkml: Path) -> None:
    adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(temp_pkml.parent),)),
        command_runner=FakeBridgeRunner(),
        env_detector=_fake_env_detector,
    )
    adapter.init()
    adapter.load_simulation(str(temp_pkml), simulation_id="demo")

    result = adapter.run_simulation_sync("demo")
    cached = adapter.get_results(result.results_id)

    assert cached.results_id == result.results_id
    assert cached.series


def test_validate_simulation_request_updates_handle_metadata(temp_pkml: Path) -> None:
    adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(temp_pkml.parent),)),
        command_runner=FakeBridgeRunner(),
        env_detector=_fake_env_detector,
    )
    adapter.init()
    handle = adapter.load_simulation(str(temp_pkml), simulation_id="demo")

    response = adapter.validate_simulation_request(
        "demo",
        request={"dose": 1.0},
        stage="preflight",
    )

    assert response["validation"]["status"] == "passed"
    assert handle.metadata["validation"]["status"] == "passed"
    assert handle.metadata["backend"] == "mock"


def test_run_verification_checks_updates_handle_metadata(temp_pkml: Path) -> None:
    adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(temp_pkml.parent),)),
        command_runner=FakeBridgeRunner(),
        env_detector=_fake_env_detector,
    )
    adapter.init()
    handle = adapter.load_simulation(str(temp_pkml), simulation_id="demo")

    response = adapter.run_verification_checks(
        "demo",
        include_population_smoke=True,
        population_cohort={"size": 8},
        population_outputs={"aggregates": ["meanCmax"]},
    )

    assert response["verification"]["status"] == "passed"
    assert handle.metadata["verification"]["status"] == "passed"
    assert handle.metadata["backend"] == "mock"


def test_export_oecd_report_updates_handle_metadata(temp_pkml: Path) -> None:
    adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(temp_pkml.parent),)),
        command_runner=FakeBridgeRunner(),
        env_detector=_fake_env_detector,
    )
    adapter.init()
    handle = adapter.load_simulation(str(temp_pkml), simulation_id="demo")

    response = adapter.export_oecd_report(
        "demo",
        request={"contextOfUse": "internal"},
        parameter_pattern="Organ.",
    )

    assert response["report"]["validation"]["status"] == "passed"
    assert handle.metadata["profile"]["name"] == temp_pkml.name
    assert handle.metadata["backend"] == "mock"


def test_population_results_are_persisted_and_reloaded(temp_pkml: Path, tmp_path: Path) -> None:
    store = PopulationResultStore(tmp_path / "population-store")
    adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(temp_pkml.parent),)),
        command_runner=FakeBridgeRunner(),
        env_detector=_fake_env_detector,
        population_store=store,
    )
    adapter.init()

    result = adapter.run_population_simulation_sync(
        PopulationSimulationConfig(
            model_path=str(temp_pkml),
            simulation_id="demo",
            cohort=PopulationCohortConfig(size=16, seed=7),
            outputs=PopulationOutputsConfig(aggregates=["meanCmax"]),
            metadata={"testCase": "population-cache"},
        )
    )

    assert result.chunk_handles
    assert result.chunk_handles[0].uri is not None

    restored_adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(temp_pkml.parent),)),
        command_runner=ExplodingRunner(),
        env_detector=_fake_env_detector,
        population_store=store,
    )
    restored_adapter.init()

    restored = restored_adapter.get_population_results(result.results_id)

    assert restored.results_id == result.results_id
    assert restored.chunk_handles[0].uri == result.chunk_handles[0].uri


def test_invalid_extension_rejected(temp_pkml: Path) -> None:
    adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(temp_pkml.parent),)),
        command_runner=FakeBridgeRunner(),
        env_detector=_fake_env_detector,
    )
    adapter.init()

    with pytest.raises(AdapterError) as exc_info:
        adapter.load_simulation(str(temp_pkml.with_suffix(".txt")))

    assert exc_info.value.code == AdapterErrorCode.INVALID_INPUT


def test_outside_allowed_root_rejected(tmp_path: Path) -> None:
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    disallowed = tmp_path / "disallowed"
    disallowed.mkdir()
    pkml = disallowed / "model.pkml"
    pkml.write_text("<pkml/>", encoding="utf-8")

    adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(allowed),)),
        command_runner=FakeBridgeRunner(),
        env_detector=_fake_env_detector,
    )
    adapter.init()

    with pytest.raises(AdapterError) as exc_info:
        adapter.load_simulation(str(pkml))

    assert exc_info.value.code == AdapterErrorCode.INVALID_INPUT
    assert "outside the allowed directories" in str(exc_info.value)


def test_backend_error_maps_to_adapter_error(temp_pkml: Path) -> None:
    class RejectingRunner(FakeBridgeRunner):
        def __call__(self, action: str, payload: Mapping[str, Any]) -> CommandResult:
            if action == "get_parameter_value":
                return CommandResult(
                    returncode=0,
                    stdout=json.dumps(
                        {
                            "error": {
                                "code": AdapterErrorCode.NOT_FOUND.value,
                                "message": "unknown parameter",
                            }
                        }
                    ),
                )
            return super().__call__(action, payload)

    adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(temp_pkml.parent),)),
        command_runner=RejectingRunner(),
        env_detector=_fake_env_detector,
    )
    adapter.init()
    adapter.load_simulation(str(temp_pkml), simulation_id="demo")

    with pytest.raises(AdapterError) as exc_info:
        adapter.get_parameter_value("demo", "Unknown.Path")

    assert exc_info.value.code == AdapterErrorCode.NOT_FOUND


def test_non_zero_returncode_maps_to_interop_error(temp_pkml: Path) -> None:
    adapter = SubprocessOspsuiteAdapter(
        AdapterConfig(model_search_paths=(str(temp_pkml.parent),)),
        command_runner=ExplodingRunner(),
        env_detector=_fake_env_detector,
    )
    adapter.init()

    with pytest.raises(AdapterError) as exc_info:
        adapter.load_simulation(str(temp_pkml), simulation_id="demo")

    assert exc_info.value.code == AdapterErrorCode.INTEROP_ERROR
