from typing import Any
from xml.etree import ElementTree as ET

from ..schema import NamecheapSchema


class NamecheapClientInitError(Exception):
    """Exception class for initialization error."""

    pass


class NamecheapClientInitData:
    """Provides set of init data for Namecheap client backend."""

    _REQUIRED_FIELDS = ("domain", "password", "username", "ip_addresses")

    def __init__(self, data: dict[str, Any]) -> None:
        if not all(key in data for key in self._REQUIRED_FIELDS):
            raise NamecheapClientInitError(
                f"Invalid data received. Required fields are: {', '.join(self._REQUIRED_FIELDS)}"
            )
        self.domain: str = data["domain"]
        self.password: str = data["password"]
        self.username: str = data["username"]

        # Namecheap requires IP address in the format: xxx.xxx.xxx.xxx
        if len(data["ip_addresses"]) > 1:
            raise NamecheapClientInitError(
                "You have supplied more than one IP address. "
                "Namecheap requires only one IP address."
            )
        if ":" in data["ip_addresses"][0]:
            raise NamecheapClientInitError(
                "Updating IPv6 is currently not supported by Namecheap."
            )
        # Namecheap only supports one IPv4 address - this ensures backwards compatibility
        self.ip_addresses: list[str] = [data["ip_addresses"][0]]


class NamecheapClient:
    """
    Client class for Namecheap DynDNS. For DynDNS operations,
    DynDNSClient class is encouraged.
    """

    def __init__(self) -> None:
        self._update_url: str = NamecheapSchema.UPDATE_URL
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
        self._update_url = self._update_url.replace("<domain_name>", username)
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
        self._update_url = self._update_url.replace("<host>", domain)
        self._init_flags["domain"] = True

    def set_ip_addresses(self, ip_addresses: list[str]) -> None:
        """Set IP addresses to be updated. Accepts `ip_addresses` as list."""
        self._update_url = self._update_url.replace("<ip_address>", ip_addresses[0])
        self._init_flags["ip_addresses"] = True

    def is_initialized(self) -> bool:
        """Return whether all values in schema have been properly initialized."""
        return all(self._init_flags.values())

    def update_url(self) -> str:
        """Return update path as a single line string."""
        return "".join(self._update_url.replace("  ", "").splitlines())


class NamecheapOutputAnalyzer:
    """Analyzes output from Namecheap DynDNS service."""

    def __init__(self, output: str) -> None:
        self._output = output
        self.status: str = ""
        self.response: str = ""

    def analyze(self) -> None:
        """Analyze the XML output and set status and response."""
        xml_obj = ET.fromstring(self._output)
        err_count_elem = xml_obj.find("ErrCount")
        self.status = (
            "OK"
            if err_count_elem is not None and err_count_elem.text == "0"
            else "ERROR"
        )

        response_elem = xml_obj.find(".//responses/response/ResponseString")
        self.response = (
            response_elem.text if response_elem is not None else "Unknown response"
        )
