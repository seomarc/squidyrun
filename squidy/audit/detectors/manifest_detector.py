"""
Manifest Detector

Detecta projeto Squidy via arquivo .squidy/manifest.json
"""

import json
from pathlib import Path

from squidy.core.ports.filesystem import FileSystemPort

from .base import BaseDetector


class ManifestDetector(BaseDetector):
    """
    Detecta projeto via manifest.json
    
    Este é o detector mais confiável, pois verifica o arquivo
    de manifesto oficial do Squidy.
    """
    
    name = "ManifestDetector"
    description = "Detecta via .squidy/manifest.json"
    
    def __init__(self, fs: FileSystemPort):
        super().__init__(fs)
    
    def detect(self, path: Path) -> bool:
        """
        Detecta via manifest.json
        
        Args:
            path: Caminho do diretório
            
        Returns:
            True se manifest.json existe e é válido
        """
        manifest_path = path / ".squidy" / "manifest.json"
        
        if not self.fs.exists(manifest_path):
            return False
        
        try:
            content = self.fs.read_text(manifest_path)
            manifest = json.loads(content)
            
            # Verifica campos obrigatórios
            required_fields = ["name", "version", "created_at"]
            return all(field in manifest for field in required_fields)
            
        except (json.JSONDecodeError, Exception):
            return False
    
    def get_confidence(self, path: Path) -> float:
        """
        Retorna confiança alta se manifest existe
        
        Returns:
            1.0 se manifest válido, 0.0 caso contrário
        """
        return 1.0 if self.detect(path) else 0.0
    
    def read_manifest(self, path: Path) -> dict | None:
        """
        Lê e retorna conteúdo do manifest
        
        Args:
            path: Caminho do projeto
            
        Returns:
            Conteúdo do manifest ou None
        """
        manifest_path = path / ".squidy" / "manifest.json"
        
        if not self.fs.exists(manifest_path):
            return None
        
        try:
            content = self.fs.read_text(manifest_path)
            return json.loads(content)
        except Exception:
            return None
