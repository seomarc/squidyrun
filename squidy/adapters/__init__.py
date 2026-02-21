"""
Adapters module - Implementações das interfaces (Ports)

Este módulo contém implementações concretas das interfaces
definidas em core/ports/.
"""

from squidy.adapters.filesystem.local_fs import LocalFileSystem

__all__ = [
    "LocalFileSystem",
]
