from .strato_client import StratoClient
from ..lib import requests_wrapper as _requests
import socket


class DynDNSClientInitException(Exception):
    """Exception class for DynDNS client initialization"""

    def __init__(self, message: str):
        super().__init__(message)


class DynDNSClientConnectException(Exception):
    """Exception class for DynDNS client connection"""

    def __init__(self, message: str):
        super().__init__(message)


class DynDNSClient:
    """
    Standard DynDNS client for supported providers
    """

    _INSTANCE: None
    _EXTERAL_API_URL: str

    _SUPPORTED_PROVIDERS = ["strato"]

    def __init__(
        self, provider: str, external_server: str = "https://regdelivery.de/ip-api"
    ):
        if provider not in self._SUPPORTED_PROVIDERS:
            raise DynDNSClientInitException(f"{provider} is not supported")
        self._INSTANCE = StratoClient()
        self._EXTERAL_API_URL = external_server

    def get_ip_v4(self):
        """
        Gets IPV4 from external server.
        """
        try:
            return _requests.get(self._EXTERAL_API_URL).text
        except ConnectionError as e:
            raise DynDNSClientConnectException(
                f"Failed to connect to external server: {e}"
            )

    def get_ip_v6(self):
        """
        Gets IPV6 from external server.
        """
        try:
            return _requests.get(self._EXTERAL_API_URL, family=socket.AF_INET6).text
        except Exception as e:
            raise DynDNSClientConnectException(
                f"Failed to connect to external server: {e}"
            )
