"""
Domain module - Entidades e objetos de valor
"""

from .project import SquidyProject
from .config import ProjectConfig, StackConfig, ConventionsConfig
from .audit_result import AuditResult, Finding, Severity

__all__ = [
    "SquidyProject",
    "ProjectConfig",
    "StackConfig",
    "ConventionsConfig",
    "AuditResult",
    "Finding",
    "Severity",
]
