"""Benchmark harness for MCP Bridge performance evaluation."""

from __future__ import annotations


def main() -> int:
    from .cli import main as cli_main

    return cli_main()

__all__ = ["main"]
