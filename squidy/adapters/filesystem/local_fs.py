"""
Local FileSystem Adapter

Implementação do FileSystemPort para sistema de arquivos local.
"""

import shutil
from pathlib import Path
from typing import Union

from squidy.core.ports.filesystem import FileSystemPort


class LocalFileSystem(FileSystemPort):
    """
    Adapter para sistema de arquivos local
    
    Esta é a implementação padrão usada em produção.
    """
    
    def exists(self, path: Path) -> bool:
        """Verifica se caminho existe"""
        return path.exists()
    
    def is_file(self, path: Path) -> bool:
        """Verifica se é arquivo"""
        return path.is_file()
    
    def is_dir(self, path: Path) -> bool:
        """Verifica se é diretório"""
        return path.is_dir()
    
    def mkdir(self, path: Path, parents: bool = False, exist_ok: bool = False) -> None:
        """Cria diretório"""
        path.mkdir(parents=parents, exist_ok=exist_ok)
    
    def read_text(self, path: Path, encoding: str = "utf-8") -> str:
        """Lê arquivo como texto"""
        return path.read_text(encoding=encoding)
    
    def write_text(self, path: Path, content: str, encoding: str = "utf-8") -> None:
        """Escreve texto em arquivo"""
        path.write_text(content, encoding=encoding)
    
    def read_bytes(self, path: Path) -> bytes:
        """Lê arquivo como bytes"""
        return path.read_bytes()
    
    def write_bytes(self, path: Path, content: bytes) -> None:
        """Escreve bytes em arquivo"""
        path.write_bytes(content)
    
    def unlink(self, path: Path, missing_ok: bool = False) -> None:
        """Remove arquivo"""
        path.unlink(missing_ok=missing_ok)
    
    def rmdir(self, path: Path, recursive: bool = False) -> None:
        """Remove diretório"""
        if recursive:
            shutil.rmtree(path)
        else:
            path.rmdir()
    
    def listdir(self, path: Path) -> list[str]:
        """Lista conteúdo do diretório"""
        return [p.name for p in path.iterdir()]
    
    def glob(self, path: Path, pattern: str) -> list[Path]:
        """Busca arquivos com padrão glob"""
        return list(path.glob(pattern))
    
    def stat(self, path: Path) -> dict:
        """Retorna estatísticas do arquivo"""
        stat = path.stat()
        return {
            "size": stat.st_size,
            "mtime": stat.st_mtime,
            "ctime": stat.st_ctime,
            "mode": stat.st_mode,
        }
    
    def get_mtime(self, path: Path) -> float:
        """Retorna timestamp de modificação"""
        return path.stat().st_mtime
    
    def get_size(self, path: Path) -> int:
        """Retorna tamanho do arquivo em bytes"""
        return path.stat().st_size
    
    def copy(self, src: Path, dst: Path) -> None:
        """Copia arquivo"""
        shutil.copy2(src, dst)
    
    def move(self, src: Path, dst: Path) -> None:
        """Move arquivo"""
        shutil.move(src, dst)
