"""
Base Detector - Interface para detectores de projeto Squidy
"""

from abc import ABC, abstractmethod
from pathlib import Path

from squidy.core.ports.filesystem import FileSystemPort


class BaseDetector(ABC):
    """
    Interface base para detectores de projeto
    
    Detectores identificam se um diretório contém um projeto Squidy.
    
    Implementações:
        - ManifestDetector: Via .squidy/manifest.json
        - HeuristicDetector: Via arquivos característicos
    """
    
    name: str = "BaseDetector"
    description: str = "Descrição do detector"
    
    def __init__(self, fs: FileSystemPort):
        self.fs = fs
    
    @abstractmethod
    def detect(self, path: Path) -> bool:
        """
        Detecta se o diretório é um projeto Squidy
        
        Args:
            path: Caminho do diretório
            
        Returns:
            True se é projeto Squidy, False caso contrário
        """
        pass
    
    @abstractmethod
    def get_confidence(self, path: Path) -> float:
        """
        Retorna nível de confiança da detecção (0.0 a 1.0)
        
        Args:
            path: Caminho do diretório
            
        Returns:
            Confiança (0.0 = baixa, 1.0 = alta)
        """
        pass
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    def __repr__(self) -> str:
        return f"<{self.name}>"
