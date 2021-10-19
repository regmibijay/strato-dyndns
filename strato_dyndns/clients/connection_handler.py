import socket

from ..lib import requests_wrapper as _requests


class ClientConnectException(Exception):
    """Exception class for DynDNS client connection"""

    def __init__(self, message: str):
        super().__init__(message)


class ConnectionHandler:
    """
    Handles connection requests to external server
    """

    _EXTERAL_API_URL: str

    def __init__(self, external_server: str = "https://regdelivery.de:443/ip-api"):
        self._EXTERAL_API_URL = external_server

    def get_ip_v4(self):
        """
        Gets IPV4 from external server.
        """
        try:
            return _requests.get(self._EXTERAL_API_URL, family=socket.AF_INET).text
        except ConnectionError as e:
            raise ClientConnectException(
                f"""
            Failed to connect to external server: {e}, 
            \nmake sure you have IPV4 network connectivity.
            """
            )

    def get_ip_v6(self):
        """
        Gets IPV6 from external server.
        """
        try:
            return _requests.get(self._EXTERAL_API_URL, family=socket.AF_INET6).text
        except Exception as e:
            raise ClientConnectException(
                f"""
            Failed to connect to external server: {e}, 
            \nmake sure you have IPV6 network connectivity.
            """
            )
