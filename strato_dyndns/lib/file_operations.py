"""File operations for reading and writing configuration files."""

import json
from typing import Any


def read_config(path: str) -> dict[str, Any]:
    """Read configuration from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_config(path: str, data: dict[str, Any]) -> None:
    """Write configuration to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
