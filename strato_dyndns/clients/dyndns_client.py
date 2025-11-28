from typing import Any

from ..lib import requests_wrapper as _requests
from .namecheap_client import (
    NamecheapClient,
    NamecheapClientInitData,
    NamecheapOutputAnalyzer,
)
from .strato_client import StratoClient, StratoClientInitData, StratoOutputAnalyzer


class DynDNSClientInitException(Exception):
    """Exception class for DynDNS client initialization."""

    pass


class DynDNSClientConnectException(Exception):
    """Exception class for DynDNS client connection."""

    pass


class DynDNSClientStatusException(Exception):
    """Exception class for DynDNS client result."""

    pass


class DynDNSClient:
    """Standard DynDNS client for supported providers."""

    _SUPPORTED_PROVIDERS: dict[str, dict[str, Any]] = {
        "strato": {
            "client": StratoClient,
            "data": StratoClientInitData,
            "output": StratoOutputAnalyzer,
        },
        "namecheap": {
            "client": NamecheapClient,
            "data": NamecheapClientInitData,
            "output": NamecheapOutputAnalyzer,
        },
    }

    def __init__(self, provider: str) -> None:
        if provider not in self._SUPPORTED_PROVIDERS:
            raise DynDNSClientInitException(f"{provider} is not supported")
        self._provider_config = self._SUPPORTED_PROVIDERS[provider]
        self._instance = self._provider_config["client"]()
        self._provider_type = provider
        self._data_initializer = self._provider_config["data"]
        self._output_analyzer = self._provider_config["output"]
        self._is_initialized = False

    def init_data(self, data: dict[str, Any]) -> None:
        """
        Initialize with data needed for provider backend.
        Required keys: `username`, `password`, `domain`, `ip_addresses`
        """
        init_data = self._data_initializer(data)
        self._instance.set_authentication(
            username=init_data.username, password=init_data.password
        )
        self._instance.set_domain(init_data.domain)
        self._instance.set_ip_addresses(ip_addresses=init_data.ip_addresses)
        self._is_initialized = True

    def update_record(self) -> str:
        """Send update request to provider and return update response."""
        if not self._is_initialized:
            raise DynDNSClientInitException(
                "Trying to update record before backend was initialized"
            )
        response = _requests.get(self._instance.update_url()).text
        return self._analyze_output(response)

    def _analyze_output(self, output: str) -> str:
        """Analyze output from DynDNS server."""
        analyzer = self._output_analyzer(output)
        analyzer.analyze()
        if analyzer.status == "ERROR":
            raise DynDNSClientStatusException(analyzer.response)
        return analyzer.response
