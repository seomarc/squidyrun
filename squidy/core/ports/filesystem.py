"""
FileSystem Port - Interface abstrata para operações de arquivo

Esta interface permite abstrair o sistema de arquivos,
facilitando testes com mocks e suporte a diferentes backends.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union


class FileSystemPort(ABC):
    """
    Interface abstrata para operações de arquivo
    
    Implementações:
        - LocalFileSystem: Operações no filesystem local
        - MockFileSystem: Mock para testes
    """
    
    @abstractmethod
    def exists(self, path: Path) -> bool:
        """Verifica se caminho existe"""
        pass
    
    @abstractmethod
    def is_file(self, path: Path) -> bool:
        """Verifica se é arquivo"""
        pass
    
    @abstractmethod
    def is_dir(self, path: Path) -> bool:
        """Verifica se é diretório"""
        pass
    
    @abstractmethod
    def mkdir(self, path: Path, parents: bool = False, exist_ok: bool = False) -> None:
        """Cria diretório"""
        pass
    
    @abstractmethod
    def read_text(self, path: Path, encoding: str = "utf-8") -> str:
        """Lê arquivo como texto"""
        pass
    
    @abstractmethod
    def write_text(self, path: Path, content: str, encoding: str = "utf-8") -> None:
        """Escreve texto em arquivo"""
        pass
    
    @abstractmethod
    def read_bytes(self, path: Path) -> bytes:
        """Lê arquivo como bytes"""
        pass
    
    @abstractmethod
    def write_bytes(self, path: Path, content: bytes) -> None:
        """Escreve bytes em arquivo"""
        pass
    
    @abstractmethod
    def unlink(self, path: Path, missing_ok: bool = False) -> None:
        """Remove arquivo"""
        pass
    
    @abstractmethod
    def rmdir(self, path: Path, recursive: bool = False) -> None:
        """Remove diretório"""
        pass
    
    @abstractmethod
    def listdir(self, path: Path) -> list[str]:
        """Lista conteúdo do diretório"""
        pass
    
    @abstractmethod
    def glob(self, path: Path, pattern: str) -> list[Path]:
        """Busca arquivos com padrão glob"""
        pass
    
    @abstractmethod
    def stat(self, path: Path) -> dict:
        """Retorna estatísticas do arquivo"""
        pass
    
    @abstractmethod
    def get_mtime(self, path: Path) -> float:
        """Retorna timestamp de modificação"""
        pass
    
    @abstractmethod
    def get_size(self, path: Path) -> int:
        """Retorna tamanho do arquivo em bytes"""
        pass
    
    @abstractmethod
    def copy(self, src: Path, dst: Path) -> None:
        """Copia arquivo"""
        pass
    
    @abstractmethod
    def move(self, src: Path, dst: Path) -> None:
        """Move arquivo"""
        pass
