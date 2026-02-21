"""
Heuristic Detector

Detecta projeto Squidy via presença de arquivos característicos.
"""

from pathlib import Path

from squidy.core.ports.filesystem import FileSystemPort

from .base import BaseDetector


class HeuristicDetector(BaseDetector):
    """
    Detecta projeto via heurísticas
    
    Verifica presença de arquivos característicos do Squidy.
    Menos confiável que ManifestDetector, mas funciona para
    projetos antigos sem manifest.
    """
    
    name = "HeuristicDetector"
    description = "Detecta via arquivos característicos"
    
    # Arquivos que indicam projeto Squidy
    MARKER_FILES = [
        "readme-agent.md",
        "doc/AGENT.md",
        "doc/constituicao.md",
        "doc/kanban.md",
    ]
    
    # Pontuação por arquivo encontrado
    SCORE_PER_FILE = 0.25
    
    def __init__(self, fs: FileSystemPort):
        super().__init__(fs)
    
    def detect(self, path: Path) -> bool:
        """
        Detecta via heurísticas
        
        Args:
            path: Caminho do diretório
            
        Returns:
            True se encontrou arquivos suficientes
        """
        score = self._calculate_score(path)
        # Detecta se score >= 0.5 (pelo menos 2 arquivos)
        return score >= 0.5
    
    def get_confidence(self, path: Path) -> float:
        """
        Retorna confiança baseada no score
        
        Returns:
            Confiança de 0.0 a 1.0
        """
        return self._calculate_score(path)
    
    def _calculate_score(self, path: Path) -> float:
        """
        Calcula score baseado em arquivos encontrados
        
        Args:
            path: Caminho do diretório
            
        Returns:
            Score de 0.0 a 1.0
        """
        found = 0
        
        for marker in self.MARKER_FILES:
            marker_path = path / marker
            if self.fs.exists(marker_path):
                found += 1
        
        return min(found * self.SCORE_PER_FILE, 1.0)
    
    def get_found_markers(self, path: Path) -> list[str]:
        """
        Retorna lista de markers encontrados
        
        Args:
            path: Caminho do diretório
            
        Returns:
            Lista de arquivos encontrados
        """
        found = []
        
        for marker in self.MARKER_FILES:
            marker_path = path / marker
            if self.fs.exists(marker_path):
                found.append(marker)
        
        return found
