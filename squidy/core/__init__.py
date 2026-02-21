"""
Core module - Regras de negócio puras do Squidy

Este módulo contém:
    - Domain: Entidades e objetos de valor
    - Ports: Interfaces abstratas (contratos)
    - Use Cases: Casos de uso da aplicação
"""

from squidy.core.domain.project import SquidyProject
from squidy.core.domain.config import ProjectConfig
from squidy.core.domain.audit_result import AuditResult, Finding, Severity

__all__ = [
    "SquidyProject",
    "ProjectConfig",
    "AuditResult",
    "Finding",
    "Severity",
]
