from typing import Any

from ..schema import StratoSchema


class StratoClientInitError(Exception):
    """Exception class for initialization error."""

    pass


class StratoClientInitData:
    """
    Provides set of init data for strato client backend.
    """

    _REQUIRED_FIELDS = ("username", "password", "domain", "ip_addresses")

    def __init__(self, data: dict[str, Any]) -> None:
        if not all(key in data for key in self._REQUIRED_FIELDS):
            raise StratoClientInitError(
                f"Invalid data received. Required fields are: {', '.join(self._REQUIRED_FIELDS)}"
            )
        self.username: str = data["username"]
        self.password: str = data["password"]
        self.domain: str = data["domain"]
        self.ip_addresses: list[str] = data["ip_addresses"]


class StratoClient:
    """
    Client class for Strato DynDNS. For DynDNS operations,
    DynDNSClient class is encouraged.
    """

    def __init__(self) -> None:
        self._update_url: str = StratoSchema.UPDATE_URL
        self._init_flags: dict[str, bool] = {
            "username": False,
            "password": False,
            "domain": False,
            "ip_addresses": False,
        }

    def set_username(self, username: str) -> None:
        """
        Set `username` for logging in DynDNS server.
        Username is usually main domain if you are
        setting up IP update for subdomains.
        """
        self._update_url = self._update_url.replace("<username>", username)
        self._init_flags["username"] = True

    def set_password(self, password: str) -> None:
        """Set `password` for logging in DynDNS server."""
        self._update_url = self._update_url.replace("<password>", password)
        self._init_flags["password"] = True

    def set_authentication(self, username: str, password: str) -> None:
        """
        Set `username` and `password` for logging in DynDNS server.
        Username is usually main domain if you are
        setting up IP update for subdomains.
        """
        self.set_username(username=username)
        self.set_password(password=password)

    def set_domain(self, domain: str) -> None:
        """Set `domain` for which the record is to be updated."""
        self._update_url = self._update_url.replace("<domain>", domain)
        self._init_flags["domain"] = True

    def set_ip_addresses(self, ip_addresses: list[str]) -> None:
        """
        Set IP addresses to be updated. Accepts `ip_addresses` as list.
        """
        self._update_url = self._update_url.replace(
            "<ip-address>", ",".join(ip_addresses)
        )
        self._init_flags["ip_addresses"] = True

    def is_initialized(self) -> bool:
        """Return whether all values in schema have been properly initialized."""
        return all(self._init_flags.values())

    def update_url(self) -> str:
        """Return update path as a single line string."""
        return "".join(self._update_url.replace("  ", "").splitlines())


class StratoOutputAnalyzer:
    """Analyzes output from Strato DynDNS service."""

    _RESPONSE_MESSAGES: dict[str, str] = {
        "badauth": (
            "Server stated authentication data was not correct, "
            "please check and try again later."
        ),
        "good": (
            "IP update completed successfully, "
            "new IP was successfully written to DNS records."
        ),
        "nochg": "IP update completed successfully, yet no changes were made.",
        "notfqdn": (
            "The hostname specified is not a fully-qualified domain name "
            "(not in the form hostname.dyndns.org or domain.com)."
        ),
        "nohost": (
            "The hostname specified does not exist in this user account "
            "(or is not in the service specified in the system parameter)."
        ),
        "numhost": (
            "Too many hosts (more than 20) specified in an update. "
            "Also returned if trying to update a round robin (which is not allowed)."
        ),
        "abuse": "The hostname specified is blocked for update abuse.",
        "badagent": (
            "The user agent was not sent or HTTP method is not permitted "
            "(we recommend use of GET request method)."
        ),
        "dnserr": "DNS error encountered.",
        "911": "There is a problem or scheduled maintenance on servers.",
    }

    def __init__(self, output: str) -> None:
        self._output_code = output.strip().split(" ")[0]
        self.status: str = ""
        self.response: str = ""

    def analyze(self) -> None:
        """Analyze the output and set status and response."""
        if self._output_code in ("nochg", "good"):
            self.status = "OK"
            self.response = self._RESPONSE_MESSAGES[self._output_code]
        else:
            self.status = "ERROR"
            self.response = self._RESPONSE_MESSAGES.get(
                self._output_code, "Unknown response received from dyndns server."
            )
