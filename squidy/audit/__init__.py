"""
Audit module - Sistema de auditoria de projetos Squidy

Este módulo permite auditar projetos existentes para verificar:
- Se a estrutura está completa
- Se o kanban está atualizado
- Se há inconsistências
- Se há arquivos desatualizados
"""

from squidy.audit.checkers.base import BaseChecker
from squidy.audit.checkers.structure_checker import StructureChecker
from squidy.audit.checkers.kanban_checker import KanbanChecker
from squidy.audit.checkers.freshness_checker import FreshnessChecker
from squidy.audit.checkers.consistency_checker import ConsistencyChecker
from squidy.audit.detectors.base import BaseDetector
from squidy.audit.detectors.manifest_detector import ManifestDetector
from squidy.audit.detectors.heuristic_detector import HeuristicDetector
from squidy.audit.engine import AuditEngine

__all__ = [
    "BaseChecker",
    "StructureChecker",
    "KanbanChecker",
    "FreshnessChecker",
    "ConsistencyChecker",
    "BaseDetector",
    "ManifestDetector",
    "HeuristicDetector",
    "AuditEngine",
]
