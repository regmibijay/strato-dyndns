from ..schema import StratoSchema


class StratoClientInitError(Exception):
    """Exception class for initialization error"""

    def __init__(self, message):
        super().__init__(message)


class StratoClientInitData:
    """
    Provides set of init data for strato client backend.
    """

    username: str
    password: str
    domain: str
    ip_addresses: list
    _valid_fields = ["username", "password", "domain", "ip_addresses"]

    def __init__(self, data):
        if not all([True for key in self._valid_fields if key in data.keys()]):
            raise StratoClientInitError(
                f"Invalid data received. required fields are: {', '.join(self._valid_fields)}"
            )
        self.username = data["username"]
        self.password = data["password"]
        self.domain = data["domain"]
        self.ip_addresses = data["ip_addresses"]


class StratoClient:
    """
    Client class for Strato DynDNS. For DynDNS operations,
    DynDNSClient class is encouraged.
    """

    UPDATE_URL: str
    INIT: list

    def __init__(self) -> None:
        self.UPDATE_URL = StratoSchema.UPDATE_URL
        self.INIT = [False, False, False, False]

    def set_username(self, username: str) -> None:
        """
        Sets `username` for logging in DynDNS server.
        Username is usually main domain if you are
        setting up IP update for subdomains.
        """
        self.UPDATE_URL = self.UPDATE_URL.replace("<username>", username)
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
        self.UPDATE_URL = self.UPDATE_URL.replace("<domain>", domain)
        self.INIT[2] = True

    def set_ip_addresses(self, ip_addresses: list) -> None:
        """
        Sets IP addresses to be updated. Accepts `ip_addresses`
        as list.
        """
        self.UPDATE_URL = self.UPDATE_URL.replace(
            "<ip-address>", ",".join(ip_addresses)
        )
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


class StratoOutputAnalyzer:
    """
    Analyzes output from Strato DynDNS service.
    """

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
    OUTPUT: str

    STATUS: str
    RESPONSE: str

    def __init__(self, output: str) -> None:
        self.OUTPUT = output.strip().split(" ")[0]

    def analyze(self) -> str:
        if "nochg" in self.OUTPUT or "good" in self.OUTPUT:
            self.STATUS = "OK"
            self.RESPONSE = self._POSSIBLE_RESPONSES[self.OUTPUT]
        else:
            self.STATUS = "ERROR"
            try:
                self.RESPONSE = self._POSSIBLE_RESPONSES[self.OUTPUT]
            except KeyError:
                self.RESPONSE = "Unknown response received from dyndns server."
