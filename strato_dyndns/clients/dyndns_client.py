from ..lib import requests_wrapper as _requests
from .namecheap_client import (
    NamecheapClient,
    NamecheapClientInitData,
    NamecheapOutputAnalyzer,
)
from .strato_client import StratoClient, StratoClientInitData, StratoOutputAnalyzer


class DynDNSClientInitException(Exception):
    """Exception class for DynDNS client initialization"""

    def __init__(self, message: str):
        super().__init__(message)


class DynDNSClientConnectException(Exception):
    """Exception class for DynDNS client connection"""

    def __init__(self, message: str):
        super().__init__(message)


class DynDNSClientStatusException(Exception):
    """Exception class for DynDNS client result"""

    def __init__(self, message: str):
        super().__init__(message)


class DynDNSClient:
    """
    Standard DynDNS client for supported providers
    """

    _INSTANCE: None
    _INSTANCE_DATA_INITIALIZER: None
    _INSTANCE_OUTPUT_ANALYZER = None
    _INSTANCE_TYPE: str
    _INSTANCE_INIT: bool
    _SUPPORTED_PROVIDERS = {
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

    def __init__(self, provider: str):
        if provider not in self._SUPPORTED_PROVIDERS.keys():
            raise DynDNSClientInitException(f"{provider} is not supported")
        self._INSTANCE = self._SUPPORTED_PROVIDERS[provider]["client"]()
        self._INSTANCE_TYPE = provider
        self._INSTANCE_DATA_INITIALIZER = self._SUPPORTED_PROVIDERS[provider]["data"]
        self._INSTANCE_OUTPUT_ANALYZER = self._SUPPORTED_PROVIDERS[provider]["output"]

    def init_data(self, data: dict):
        """
        Expects init data needed for provider backend.
        `username`, `password`, `domain`, `ip_addresses`
        """

        data = self._INSTANCE_DATA_INITIALIZER(data)
        self._INSTANCE.set_authentication(
            username=data.username, password=data.password
        )
        self._INSTANCE.set_domain(data.domain)
        self._INSTANCE.set_ip_addresses(ip_addresses=data.ip_addresses)
        self._INSTANCE_INIT = True

    def update_record(self) -> str:
        """
        Sends update request to provider and returns update response
        """
        if not self._INSTANCE_INIT:
            raise DynDNSClientInitException(
                "trying to update record before backend was initialized"
            )
        resp = _requests.get(self._INSTANCE.update_url()).text
        return self.analyze_output(resp)

    def analyze_output(self, output: str) -> str:
        """
        Analyzes output from DynDNS server.
        """
        analyzer = self._INSTANCE_OUTPUT_ANALYZER(output)
        analyzer.analyze()
        if analyzer.STATUS == "ERROR":
            raise DynDNSClientStatusException(analyzer.RESPONSE)
        return analyzer.RESPONSE
