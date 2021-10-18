from ..lib import requests_wrapper as _requests
from .strato_client import StratoClient, StratoClientInitData


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
    _INSTANCE_TYPE: str
    _INSTANCE_INIT: bool
    _SUPPORTED_PROVIDERS = {"strato": StratoClient}
    _POSSIBLE_RESPONSES = {
        "badauth": "Server stated authentification data was not correct, please check and try again later.",
        "good": "IP update completed successfully, new ip was successfully written to DNS records.",
        "nochg": "IP update completed successfully, yet no changes were made.",
        "notfqdn": "The hostname specified is not a fully-qualified domain name (not in the form hostname.dyndns.org or domain.com).",
        "nohost": "The hostname specified does not exist in this user account (or is not in the service specified in the system parameter).",
        "numhost": "Too many hosts (more than 20) specified in an update. Also returned if trying to update a round robin (which is not allowed).",
        "abuse": "The hostname specified is blocked for update abuse.",
        "badagent": "The user agent was not sent or HTTP method is not permitted (we recommend use of GET request method).",
        "dnserr": "DNS error encountered.",
        "911": "There is a problem or scheduled maintainance on Servers.",
    }

    def __init__(self, provider: str):
        if provider not in self._SUPPORTED_PROVIDERS.keys():
            raise DynDNSClientInitException(f"{provider} is not supported")
        self._INSTANCE = self._SUPPORTED_PROVIDERS[provider]()
        self._INSTANCE_TYPE = provider

    def init_data(self, data: dict):
        """
        Expects init data needed for provider backend.
        `username`, `password`, `domain`, `ip_addresses`
        """
        if self._INSTANCE_TYPE == "strato":
            data = StratoClientInitData(data)
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
        if not resp not in self._POSSIBLE_RESPONSES.keys():
            raise DynDNSClientConnectException(
                f"Request was sent to server but server sent unknown response: {resp}"
            )
        return self.analyze_output(resp.strip().split(" ")[0])

    def analyze_output(self, output: str) -> str:
        """
        Analyzes output from DynDNS server.
        """
        if output in ["good", "nochg"]:
            return self._POSSIBLE_RESPONSES[output]
        raise DynDNSClientStatusException(
            f"Server returned error : {self._POSSIBLE_RESPONSES[output]}"
        )
