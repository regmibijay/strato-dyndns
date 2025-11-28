import sys
from argparse import Namespace
from typing import Any

from ..clients import ConnectionHandler
from .file_operations import read_config


class ArgsValidator:
    """
    Validates CLI args in `main.py`,
    expects `arg` which is a set of arguments from
    `ArgumentParser`.
    """

    def __init__(self, arg: Namespace) -> None:
        self._arg = arg
        self._connection_handler = ConnectionHandler()
        self._config: dict[str, Any] = {}
        try:
            self._parse_config()
        except Exception as e:
            print(f"Could not process your parameters, reason: {e}")
            sys.exit(1)

    def _is_valid_string(self, value: Any) -> bool:
        """Check if value is a valid non-empty string."""
        if value is None or isinstance(value, bool):
            return False
        if isinstance(value, list):
            return all(self._is_valid_string(x) for x in value)
        return bool(str(value).strip())

    def _validate_config(self, config: dict) -> dict:
        """Validate that config contains required keys."""
        required_keys = ["username", "password", "domain"]
        if not all(key in config for key in required_keys):
            print("Config file did not contain some required fields.")
            sys.exit(1)
        return config

    def _get_ip_addresses(self, print_detection: bool = False) -> list[str]:
        """Determine IP addresses from arguments or by detection."""
        ip_addresses: list[str] = []

        if self._arg.v4 is True:
            if print_detection:
                print("Determining external ipv4")
            ip_addresses.append(self._connection_handler.get_ip_v4())
        elif self._arg.v4:
            ip_addresses.append(self._arg.v4)

        if self._arg.v6 is True:
            if print_detection:
                print("Determining external ipv6")
            ip_addresses.append(self._connection_handler.get_ip_v6())
        elif self._arg.v6:
            ip_addresses.append(self._arg.v6)

        if self._arg.v4 is None and self._arg.v6 is None:
            print(
                "No IP Addresses provided and no -v4 or -v6 flag set. "
                "Script will not determine interfaces automatically. "
                "Please specify either interface."
            )
            sys.exit(1)

        return ip_addresses

    def _parse_config(self) -> None:
        """Parse and validate configuration from arguments or config file."""
        if self._arg.config:
            self._config = self._validate_config(read_config(self._arg.config))
            # Override config values with command line arguments if provided
            if self._arg.username and self._is_valid_string(self._arg.username):
                self._config["username"] = self._arg.username
            if self._arg.password and self._is_valid_string(self._arg.password):
                self._config["password"] = self._arg.password
            if self._arg.domain and self._is_valid_string(self._arg.domain):
                self._config["domain"] = self._arg.domain

            if self._arg.ip:
                self._config["ip_addresses"] = self._arg.ip
            else:
                self._config["ip_addresses"] = self._get_ip_addresses()
        else:
            if not all([self._arg.username, self._arg.password, self._arg.domain]):
                print(
                    "Neither config nor proper authentication details were provided. "
                    "Please provide either with -c or -u, -p, -d."
                )
                sys.exit(1)

            self._config["username"] = self._arg.username
            self._config["password"] = self._arg.password
            self._config["domain"] = self._arg.domain
            self._config["ip_addresses"] = (
                self._arg.ip
                if self._arg.ip
                else self._get_ip_addresses(print_detection=True)
            )

    def config_in_dict(self) -> dict[str, Any]:
        """Return configuration as a dictionary."""
        return dict(self._config)
