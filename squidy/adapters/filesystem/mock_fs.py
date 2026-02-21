"""
Mock FileSystem Adapter

Implementação em memória do FileSystemPort para testes.
Não faz operações reais no disco.
"""

from pathlib import Path
from typing import Union
from datetime import datetime

from squidy.core.ports.filesystem import FileSystemPort


class MockFileSystem(FileSystemPort):
    """
    Mock de sistema de arquivos para testes
    
    Armazena tudo em memória, sem tocar no disco real.
    Útil para testes unitários rápidos e isolados.
    
    Example:
        >>> fs = MockFileSystem()
        >>> fs.write_text(Path("/test/file.txt"), "Hello")
        >>> fs.read_text(Path("/test/file.txt"))
        'Hello'
    """
    
    def __init__(self):
        self._files: dict[str, Union[str, bytes]] = {}
        self._dirs: set[str] = set()
        self._mtimes: dict[str, float] = {}
    
    def _normalize_path(self, path: Path) -> str:
        """Normaliza path para string absoluta"""
        return str(path.resolve()) if path.is_absolute() else str(Path("/" / path).resolve())
    
    def exists(self, path: Path) -> bool:
        """Verifica se caminho existe"""
        path_str = self._normalize_path(path)
        return path_str in self._files or path_str in self._dirs
    
    def is_file(self, path: Path) -> bool:
        """Verifica se é arquivo"""
        return self._normalize_path(path) in self._files
    
    def is_dir(self, path: Path) -> bool:
        """Verifica se é diretório"""
        path_str = self._normalize_path(path)
        if path_str in self._dirs:
            return True
        # Verifica se há arquivos neste diretório
        return any(p.startswith(path_str + "/") for p in self._files)
    
    def mkdir(self, path: Path, parents: bool = False, exist_ok: bool = False) -> None:
        """Cria diretório"""
        path_str = self._normalize_path(path)
        
        if path_str in self._files:
            raise FileExistsError(f"{path} é um arquivo")
        
        if path_str in self._dirs and not exist_ok:
            raise FileExistsError(f"Diretório {path} já existe")
        
        if parents and "/" in path_str:
            # Cria diretórios pai
            parts = path_str.split("/")
            for i in range(2, len(parts) + 1):
                parent = "/".join(parts[:i])
                self._dirs.add(parent)
        else:
            self._dirs.add(path_str)
    
    def read_text(self, path: Path, encoding: str = "utf-8") -> str:
        """Lê arquivo como texto"""
        path_str = self._normalize_path(path)
        if path_str not in self._files:
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        content = self._files[path_str]
        if isinstance(content, bytes):
            return content.decode(encoding)
        return content
    
    def write_text(self, path: Path, content: str, encoding: str = "utf-8") -> None:
        """Escreve texto em arquivo"""
        path_str = self._normalize_path(path)
        self._files[path_str] = content
        self._mtimes[path_str] = datetime.now().timestamp()
        # Cria diretórios pai automaticamente
        parent = path.parent
        if str(parent) != ".":
            self.mkdir(parent, parents=True, exist_ok=True)
    
    def read_bytes(self, path: Path) -> bytes:
        """Lê arquivo como bytes"""
        path_str = self._normalize_path(path)
        if path_str not in self._files:
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        content = self._files[path_str]
        if isinstance(content, str):
            return content.encode("utf-8")
        return content
    
    def write_bytes(self, path: Path, content: bytes) -> None:
        """Escreve bytes em arquivo"""
        path_str = self._normalize_path(path)
        self._files[path_str] = content
        self._mtimes[path_str] = datetime.now().timestamp()
        parent = path.parent
        if str(parent) != ".":
            self.mkdir(parent, parents=True, exist_ok=True)
    
    def unlink(self, path: Path, missing_ok: bool = False) -> None:
        """Remove arquivo"""
        path_str = self._normalize_path(path)
        if path_str not in self._files:
            if missing_ok:
                return
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        del self._files[path_str]
        if path_str in self._mtimes:
            del self._mtimes[path_str]
    
    def rmdir(self, path: Path, recursive: bool = False) -> None:
        """Remove diretório"""
        path_str = self._normalize_path(path)
        
        if recursive:
            # Remove tudo dentro
            to_remove = [p for p in self._files if p.startswith(path_str + "/")]
            for p in to_remove:
                del self._files[p]
                if p in self._mtimes:
                    del self._mtimes[p]
            to_remove_dirs = [d for d in self._dirs if d.startswith(path_str)]
            for d in to_remove_dirs:
                self._dirs.discard(d)
        else:
            if any(p.startswith(path_str + "/") for p in self._files):
                raise OSError(f"Diretório não vazio: {path}")
            self._dirs.discard(path_str)
    
    def listdir(self, path: Path) -> list[str]:
        """Lista conteúdo do diretório"""
        path_str = self._normalize_path(path)
        items = set()
        
        # Arquivos diretos
        for p in self._files:
            if "/" in p[len(path_str) + 1:]:
                continue
            if p.startswith(path_str + "/"):
                items.add(p[len(path_str) + 1:].split("/")[0])
        
        # Diretórios diretos
        for d in self._dirs:
            if d == path_str:
                continue
            if d.startswith(path_str + "/"):
                rel = d[len(path_str) + 1:]
                if "/" not in rel:
                    items.add(rel)
        
        return sorted(list(items))
    
    def glob(self, path: Path, pattern: str) -> list[Path]:
        """Busca arquivos com padrão glob (simplificado)"""
        import fnmatch
        path_str = self._normalize_path(path)
        results = []
        
        for p in self._files:
            rel = p[len(path_str) + 1:] if p.startswith(path_str) else p
            if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(p, pattern):
                results.append(Path(p))
        
        return results
    
    def stat(self, path: Path) -> dict:
        """Retorna estatísticas do arquivo"""
        path_str = self._normalize_path(path)
        if path_str not in self._files:
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        
        content = self._files[path_str]
        size = len(content.encode("utf-8") if isinstance(content, str) else content)
        
        return {
            "size": size,
            "mtime": self._mtimes.get(path_str, 0),
            "ctime": self._mtimes.get(path_str, 0),
            "mode": 0o644,
        }
    
    def get_mtime(self, path: Path) -> float:
        """Retorna timestamp de modificação"""
        path_str = self._normalize_path(path)
        if path_str not in self._files:
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        return self._mtimes.get(path_str, 0)
    
    def get_size(self, path: Path) -> int:
        """Retorna tamanho do arquivo em bytes"""
        return self.stat(path)["size"]
    
    def copy(self, src: Path, dst: Path) -> None:
        """Copia arquivo"""
        content = self.read_bytes(src)
        self.write_bytes(dst, content)
    
    def move(self, src: Path, dst: Path) -> None:
        """Move arquivo"""
        self.copy(src, dst)
        self.unlink(src)
    
    def reset(self) -> None:
        """Limpa todos os dados (útil entre testes)"""
        self._files.clear()
        self._dirs.clear()
        self._mtimes.clear()
    
    def dump_state(self) -> dict:
        """Retorna estado atual para debug"""
        return {
            "files": list(self._files.keys()),
            "dirs": list(self._dirs),
        }
