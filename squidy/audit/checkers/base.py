"""
Base Checker - Interface para todos os checkers de auditoria
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from squidy.core.domain.audit_result import Finding, Severity
from squidy.core.ports.filesystem import FileSystemPort


class BaseChecker(ABC):
    """
    Interface base para todos os checkers de auditoria
    
    Cada checker verifica um aspecto específico do projeto:
    - StructureChecker: Arquivos obrigatórios
    - KanbanChecker: Estado do kanban
    - FreshnessChecker: Idade dos arquivos
    - ConsistencyChecker: Consistência entre arquivos
    
    Example:
        >>> checker = StructureChecker(fs)
        >>> findings = checker.check(project_path)
        >>> for finding in findings:
        ...     print(finding)
    """
    
    name: str = "BaseChecker"
    description: str = "Descrição do checker"
    
    def __init__(self, fs: FileSystemPort):
        """
        Inicializa checker
        
        Args:
            fs: Adaptador de filesystem
        """
        self.fs = fs
    
    @abstractmethod
    def check(self, project_path: Path, project_name: str | None = None) -> list[Finding]:
        """
        Executa verificação no projeto
        
        Args:
            project_path: Caminho do projeto
            project_name: Nome do projeto (opcional)
            
        Returns:
            Lista de findings (problemas encontrados)
        """
        pass
    
    def _create_finding(
        self,
        message: str,
        severity: Severity,
        file: str | None = None,
        suggestion: str | None = None,
        auto_fixable: bool = False,
    ) -> Finding:
        """
        Helper para criar Finding
        
        Args:
            message: Descrição do problema
            severity: Nível de severidade
            file: Arquivo afetado
            suggestion: Sugestão de correção
            auto_fixable: Se pode ser corrigido automaticamente
            
        Returns:
            Finding criado
        """
        return Finding(
            checker=self.name,
            severity=severity,
            message=message,
            file=file,
            suggestion=suggestion,
            auto_fixable=auto_fixable,
        )
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    def __repr__(self) -> str:
        return f"<{self.name}>"
