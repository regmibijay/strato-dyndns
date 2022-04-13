from xml.etree import ElementTree as ET

from ..schema import NamecheapSchema


class NamecheapClientInitError(Exception):
    """Exception class for initialization error"""

    def __init__(self, message):
        super().__init__(message)


class NamecheapClientInitData:
    """
    Provides set of init data for Namecheap client backend.
    """

    domain: str
    password: str
    username: str
    ip_addresses: list
    _valid_fields = ["domain", "password", "username", "ip_addresses"]

    def __init__(self, data):
        if not all([True for key in self._valid_fields if key in data.keys()]):
            raise NamecheapClientInitError(
                f"Invalid data received. required fields are: {', '.join(self._valid_fields)}"
            )
        self.domain = data["domain"]
        self.password = data["password"]
        self.username = data["username"]

        # Namecheap requires IP address in the format: xxx.xxx.xxx.xxx
        if len(data["ip_addresses"]) > 1:
            raise NamecheapClientInitError(
                "You have supplied more than one IP address. Namecheap requires only one IP address."
            )
        if ":" in data["ip_addresses"][0]:
            raise NamecheapClientInitError(
                "Updating IPv6 is currently not supported by Namecheap."
            )
        # Namecheap only supports one ipv4 address and this is for
        # backwards compatibility
        self.ip_addresses = [data["ip_addresses"][0]]


class NamecheapClient:
    """
    Client class for Namecheap DynDNS. For DynDNS operations,
    DynDNSClient class is encouraged.
    """

    UPDATE_URL: str
    INIT: list

    def __init__(self) -> None:
        self.UPDATE_URL = NamecheapSchema.UPDATE_URL
        self.INIT = [False, False, False, False]

    def set_username(self, username: str) -> None:
        """
        Sets `username` for logging in DynDNS server.
        Username is usually main domain if you are
        setting up IP update for subdomains.
        """
        self.UPDATE_URL = self.UPDATE_URL.replace("<domain_name>", username)
        self.INIT[0] = True

    def set_password(self, password: str) -> None:
        """
        Sets `password` for logging in DynDNS server.
        """
        self.UPDATE_URL = self.UPDATE_URL.replace("<password>", password)
        self.INIT[1] = True

    def set_authentication(self, username: str, password: str) -> None:
        """
        Sets `username` and `password` for logging in DynDNS
        server. Username is usually main domain if you are
        setting up IP update for subdomains.
        """
        self.set_username(username=username)
        self.set_password(password=password)
        self.INIT[0:2] = [True] * 2

    def set_domain(self, domain: str) -> None:
        """
        Sets `domain` for which the record is to be updated.
        """
        self.UPDATE_URL = self.UPDATE_URL.replace("<host>", domain)
        self.INIT[2] = True

    def set_ip_addresses(self, ip_addresses: str) -> None:
        """
        Sets IP addresses to be updated. Accepts `ip_addresses`
        as list.
        """
        self.UPDATE_URL = self.UPDATE_URL.replace("<ip_address>", ip_addresses[0])
        self.INIT[3] = True

    def is_initialized(self) -> bool:
        """
        Returns boolean whether all values in schema has
        been properly initialized
        """
        return all(self.INIT)

    def update_url(self) -> str:
        """
        Returns update path in plain single line string.
        """
        return "".join(self.UPDATE_URL.replace("  ", "").splitlines())


class NamecheapOutputAnalyzer:
    """
    Analyzes output from Namecheap DynDNS service.
    """

    STATUS: str
    RESPONSE: str

    def __init__(self, output: str) -> None:
        self.output = output

    def analyze(self) -> tuple:
        xml_obj = ET.fromstring(self.output)
        self.STATUS = "ERROR"
        if xml_obj.find("ErrCount").text == "0":
            self.STATUS = "OK"
        self.RESPONSE = xml_obj.find(".//responses/response/ResponseString").text
