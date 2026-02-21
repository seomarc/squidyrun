"""
Ports module - Interfaces abstratas (contratos)

Seguindo o padrão Ports & Adapters (Arquitetura Hexagonal),
estas interfaces definem contratos que os adapters implementam.
"""

from .filesystem import FileSystemPort
from .ai_provider import AIProviderPort
from .storage import StoragePort

__all__ = [
    "FileSystemPort",
    "AIProviderPort",
    "StoragePort",
]
