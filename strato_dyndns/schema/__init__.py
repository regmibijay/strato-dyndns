"""Schema definitions for DynDNS providers."""

from .namecheap import NamecheapSchema
from .strato import StratoSchema

__all__ = ["NamecheapSchema", "StratoSchema"]
