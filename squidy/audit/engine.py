"""
Audit Engine

Orquestra o processo de auditoria, coordenando detectores e checkers.
"""

import time
from pathlib import Path
from typing import Type

from squidy.core.domain.audit_result import AuditResult, Finding
from squidy.core.ports.filesystem import FileSystemPort

from .checkers.base import BaseChecker
from .detectors.base import BaseDetector


class AuditEngine:
    """
    Motor de auditoria de projetos Squidy
    
    Coordena detectores (identificam projetos) e checkers (verificam problemas).
    
    Example:
        >>> engine = AuditEngine(fs)
        >>> engine.register_checker(StructureChecker)
        >>> engine.register_detector(ManifestDetector)
        >>> result = engine.audit(Path("./meu-projeto"))
        >>> print(result.summary)
    """
    
    def __init__(self, fs: FileSystemPort):
        """
        Inicializa engine de auditoria
        
        Args:
            fs: Adaptador de filesystem
        """
        self.fs = fs
        self._checkers: list[Type[BaseChecker]] = []
        self._detectors: list[Type[BaseDetector]] = []
    
    def register_checker(self, checker_class: Type[BaseChecker]) -> None:
        """
        Registra um checker
        
        Args:
            checker_class: Classe do checker (não instância)
        """
        self._checkers.append(checker_class)
    
    def register_detector(self, detector_class: Type[BaseDetector]) -> None:
        """
        Registra um detector
        
        Args:
            detector_class: Classe do detector (não instância)
        """
        self._detectors.append(detector_class)
    
    def is_squidy_project(self, path: Path) -> tuple[bool, float]:
        """
        Verifica se diretório é um projeto Squidy
        
        Args:
            path: Caminho do diretório
            
        Returns:
            Tuple (is_squidy, confidence)
        """
        if not self._detectors:
            # Sem detectores registrados, usa heuristic básica
            return self._basic_detection(path)
        
        max_confidence = 0.0
        
        for detector_class in self._detectors:
            detector = detector_class(self.fs)
            if detector.detect(path):
                confidence = detector.get_confidence(path)
                max_confidence = max(max_confidence, confidence)
        
        return (max_confidence > 0.5, max_confidence)
    
    def audit(
        self,
        path: Path,
        project_name: str | None = None,
        checkers: list[str] | None = None,
    ) -> AuditResult:
        """
        Executa auditoria completa
        
        Args:
            path: Caminho do projeto
            project_name: Nome do projeto (opcional)
            checkers: Lista de nomes de checkers para executar (None = todos)
            
        Returns:
            Resultado da auditoria
        """
        start_time = time.time()
        
        result = AuditResult(
            project_path=path,
            project_name=project_name,
        )
        
        # Executa cada checker
        for checker_class in self._checkers:
            checker_name = checker_class.name
            
            # Filtra checkers se especificado
            if checkers and checker_name not in checkers:
                continue
            
            try:
                checker = checker_class(self.fs)
                findings = checker.check(path, project_name)
                
                for finding in findings:
                    result.add_finding(finding)
                
                result.checkers_run.append(checker_name)
                
            except Exception as e:
                # Registra erro do checker como finding
                result.add_finding(Finding(
                    checker=checker_name,
                    severity="high",
                    message=f"Erro ao executar checker: {e}",
                ))
        
        # Calcula duração
        duration_ms = int((time.time() - start_time) * 1000)
        result.duration_ms = duration_ms
        
        return result
    
    def get_checker_names(self) -> list[str]:
        """Retorna nomes dos checkers registrados"""
        return [c.name for c in self._checkers]
    
    def get_detector_names(self) -> list[str]:
        """Retorna nomes dos detectores registrados"""
        return [d.name for d in self._detectors]
    
    def _basic_detection(self, path: Path) -> tuple[bool, float]:
        """
        Detecção básica sem detectores registrados
        
        Verifica presença de readme-agent.md e doc/constituicao.md
        """
        readme_path = path / "readme-agent.md"
        constituicao_path = path / "doc" / "constituicao.md"
        
        has_readme = self.fs.exists(readme_path)
        has_constituicao = self.fs.exists(constituicao_path)
        
        if has_readme and has_constituicao:
            return (True, 1.0)
        elif has_readme or has_constituicao:
            return (True, 0.5)
        else:
            return (False, 0.0)
