import socket

from ..lib import requests_wrapper as _requests


class ClientConnectException(Exception):
    """Exception class for DynDNS client connection."""

    pass


class ConnectionHandler:
    """Handles connection requests to external server."""

    _DEFAULT_API_URL = "https://regdelivery.de:443/ip-api?src=stratodyndns"

    def __init__(self, external_server: str | None = None) -> None:
        self._external_api_url = external_server or self._DEFAULT_API_URL

    def get_ip_v4(self) -> str:
        """Get IPv4 address from external server."""
        try:
            return _requests.get(self._external_api_url, family=socket.AF_INET).text
        except ConnectionError as e:
            raise ClientConnectException(
                f"Failed to connect to external server: {e}. "
                "Make sure you have IPv4 network connectivity."
            )

    def get_ip_v6(self) -> str:
        """Get IPv6 address from external server."""
        try:
            return _requests.get(self._external_api_url, family=socket.AF_INET6).text
        except Exception as e:
            raise ClientConnectException(
                f"Failed to connect to external server: {e}. "
                "Make sure you have IPv6 network connectivity."
            )
