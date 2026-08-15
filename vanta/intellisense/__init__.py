"""IntelliSense system - Real code intelligence"""
from .intellisense import IntelliSense
from .context import CodeContext
from .hover import HoverProvider
from .definition import DefinitionProvider
from .references import ReferencesProvider

__all__ = [
    "IntelliSense",
    "CodeContext",
    "HoverProvider",
    "DefinitionProvider",
    "ReferencesProvider",
]
