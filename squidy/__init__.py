"""
🦑 Squidy v2.0 - Setup Inteligente para Projetos com Agentes de IA

Uma CLI premium para governança e auditoria de projetos de software
com Agentes de IA (Claude, GPT-4, Cursor, etc).

Features:
    - Setup com IA via entrevista adaptativa
    - Geração de estrutura de governança completa
    - Auditoria de projetos existentes
    - Sistema de plugins extensível
    - UI/UX premium com Rich

Example:
    >>> from squidy import SquidyProject
    >>> project = SquidyProject("meu-projeto")
    >>> project.initialize()
"""

__version__ = "2.0.0"
__author__ = "Marcos Tadeu"
__email__ = "contato@squidy.run"
__license__ = "MIT"
__url__ = "https://squidy.run"

from squidy.core.domain.project import SquidyProject
from squidy.core.domain.config import ProjectConfig
from squidy.core.domain.audit_result import AuditResult

__all__ = [
    "SquidyProject",
    "ProjectConfig", 
    "AuditResult",
    "__version__",
]
