"""
Storage Port - Interface abstrata para persistência de dados

Esta interface permite abstrair onde os dados são armazenados,
facilitando testes e diferentes backends (local, cloud, etc).
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional


class StoragePort(ABC):
    """
    Interface abstrata para persistência de dados
    
    Implementações:
        - LocalStorage: Armazenamento local (JSON, YAML)
        - CloudStorage: Armazenamento em nuvem
        - MemoryStorage: Armazenamento em memória (testes)
    """
    
    @abstractmethod
    def save(self, key: str, data: Any) -> None:
        """Salva dados"""
        pass
    
    @abstractmethod
    def load(self, key: str) -> Optional[Any]:
        """Carrega dados"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Deleta dados. Retorna True se existia"""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Verifica se chave existe"""
        pass
    
    @abstractmethod
    def list_keys(self, prefix: Optional[str] = None) -> list[str]:
        """Lista chaves, opcionalmente filtradas por prefixo"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Limpa todos os dados"""
        pass
