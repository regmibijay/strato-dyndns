"""
Contains scheme for Strato DynDNS service.
"""


class StratoSchema:
    """
    Schema class for Strato DynDNS
    """

    UPDATE_URL = """
        https://<username>:<password>@dyndns.strato.com/nic/update?
        hostname=<domain>&myip=<ip-address>
        """
