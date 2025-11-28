"""Strato DynDNS - Updates DNS records on supported DNS registrars."""

from .clients import DynDNSClient, DynDNSClientStatusException

__all__ = ["DynDNSClient", "DynDNSClientStatusException"]
