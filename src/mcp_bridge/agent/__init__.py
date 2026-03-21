"""Agent scaffolding utilities for LangChain/LangGraph workflows."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING


_LANGCHAIN_EXPORTS = {
    "CRITICAL_TOOLS",
    "AgentState",
    "build_agent_graph",
    "create_agent_workflow",
    "create_initial_agent_state",
    "create_tool_registry",
    "route_after_confirmation",
    "route_after_selection",
}

_SENSITIVITY_EXPORTS = {
    "SensitivityAnalysisError",
    "SensitivityAnalysisReport",
    "SensitivityConfig",
    "SensitivityParameterSpec",
    "ScenarioReport",
    "generate_scenarios",
    "run_sensitivity_analysis",
}

__all__ = sorted(_LANGCHAIN_EXPORTS | _SENSITIVITY_EXPORTS)


def __getattr__(name: str):
    if name in _LANGCHAIN_EXPORTS:
        module = import_module(".langchain_scaffolding", __name__)
    elif name in _SENSITIVITY_EXPORTS:
        module = import_module(".sensitivity", __name__)
    else:  # pragma: no cover - standard attribute fallback
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))


if TYPE_CHECKING:  # pragma: no cover - typing only
    from .langchain_scaffolding import (  # noqa: F401
        CRITICAL_TOOLS,
        AgentState,
        build_agent_graph,
        create_agent_workflow,
        create_initial_agent_state,
        create_tool_registry,
        route_after_confirmation,
        route_after_selection,
    )
    from .sensitivity import (  # noqa: F401
        SensitivityAnalysisError,
        SensitivityAnalysisReport,
        SensitivityConfig,
        SensitivityParameterSpec,
        ScenarioReport,
        generate_scenarios,
        run_sensitivity_analysis,
    )
