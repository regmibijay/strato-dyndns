"""Client modules for DynDNS providers."""

from .connection_handler import ConnectionHandler
from .dyndns_client import (
    DynDNSClient,
    DynDNSClientConnectException,
    DynDNSClientInitException,
    DynDNSClientStatusException,
)
from .namecheap_client import NamecheapClient
from .strato_client import StratoClient

__all__ = [
    "ConnectionHandler",
    "DynDNSClient",
    "DynDNSClientConnectException",
    "DynDNSClientInitException",
    "DynDNSClientStatusException",
    "NamecheapClient",
    "StratoClient",
]
