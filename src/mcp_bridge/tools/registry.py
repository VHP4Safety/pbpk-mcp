"""Central registry describing packaged MCP tools exposed by the bridge."""

from __future__ import annotations

from typing import Dict

from .registry_base import ToolDescriptor, get_base_tool_registry


def get_tool_registry() -> Dict[str, ToolDescriptor]:
    """Return the packaged MCP tool registry keyed by tool name."""

    return get_base_tool_registry()


__all__ = ["ToolDescriptor", "get_tool_registry"]
