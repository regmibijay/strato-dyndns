"""
Contains scheme for Namecheap DynDNS service.
"""


class NamecheapSchema:
    """
    Schema class for Namecheap DynDNS
    """

    UPDATE_URL = """
        https://dynamicdns.park-your-domain.com/update?host=<host>&domain=<domain_name>&password=<password>&ip=<ip_address>
        """
