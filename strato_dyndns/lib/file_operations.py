import json


def read_config(path: str) -> dict:
    """Reads configuration from provided file"""
    with open(path, "r") as f:
        return json.load(f)


def write_config(path: str, data: dict) -> dict:
    """Writes configuration to provided file"""
    with open(path, "w") as f:
        json.dump(data, f)
