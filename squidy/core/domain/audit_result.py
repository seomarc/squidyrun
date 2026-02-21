"""
Resultado de auditoria de um projeto Squidy
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class Severity(str, Enum):
    """Níveis de severidade de findings"""
    CRITICAL = "critical"      # 🔴 Impede funcionamento
    HIGH = "high"              # 🟠 Problema sério
    MEDIUM = "medium"          # 🟡 Atenção necessária
    LOW = "low"                # 🟢 Sugestão de melhoria
    INFO = "info"              # 🔵 Informação


class Finding(BaseModel):
    """
    Representa um problema encontrado na auditoria
    
    Attributes:
        checker: Nome do checker que encontrou
        severity: Nível de severidade
        message: Descrição do problema
        file: Arquivo afetado (opcional)
        line: Linha afetada (opcional)
        suggestion: Sugestão de correção
        auto_fixable: Se pode ser corrigido automaticamente
    """
    
    checker: str = Field(..., description="Nome do checker")
    severity: Severity = Field(..., description="Nível de severidade")
    message: str = Field(..., description="Descrição do problema")
    file: Optional[str] = Field(default=None, description="Arquivo afetado")
    line: Optional[int] = Field(default=None, description="Linha afetada")
    suggestion: Optional[str] = Field(default=None, description="Sugestão de correção")
    auto_fixable: bool = Field(default=False, description="Pode ser corrigido automaticamente")
    
    def __str__(self) -> str:
        emoji = {
            Severity.CRITICAL: "🔴",
            Severity.HIGH: "🟠",
            Severity.MEDIUM: "🟡",
            Severity.LOW: "🟢",
            Severity.INFO: "🔵",
        }.get(self.severity, "⚪")
        
        location = f" in {self.file}" if self.file else ""
        return f"{emoji} [{self.severity.upper()}] {self.message}{location}"
    
    def __repr__(self) -> str:
        return f"<Finding {self.severity} checker={self.checker}>"


class AuditResult(BaseModel):
    """
    Resultado completo de uma auditoria
    
    Attributes:
        project_path: Caminho do projeto auditado
        project_name: Nome do projeto
        timestamp: Data/hora da auditoria
        findings: Lista de problemas encontrados
        duration_ms: Duração da auditoria em ms
        checkers_run: Lista de checkers executados
        summary: Resumo dos findings por severidade
    """
    
    project_path: Path = Field(..., description="Caminho do projeto")
    project_name: Optional[str] = Field(default=None, description="Nome do projeto")
    timestamp: datetime = Field(default_factory=datetime.now)
    findings: list[Finding] = Field(default_factory=list)
    duration_ms: Optional[int] = Field(default=None, description="Duração em ms")
    checkers_run: list[str] = Field(default_factory=list)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def __str__(self) -> str:
        return f"AuditResult({len(self.findings)} findings)"
    
    def __repr__(self) -> str:
        return f"<AuditResult findings={len(self.findings)}>"
    
    @property
    def summary(self) -> dict[str, int]:
        """Retorna resumo de findings por severidade"""
        counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0,
            "total": len(self.findings),
        }
        for finding in self.findings:
            counts[finding.severity.value] += 1
        return counts
    
    @property
    def has_critical(self) -> bool:
        """Verifica se há findings críticos"""
        return any(f.severity == Severity.CRITICAL for f in self.findings)
    
    @property
    def has_issues(self) -> bool:
        """Verifica se há algum problema (critical, high, medium)"""
        return any(
            f.severity in (Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM)
            for f in self.findings
        )
    
    @property
    def auto_fixable_count(self) -> int:
        """Retorna quantidade de findings auto-fixáveis"""
        return sum(1 for f in self.findings if f.auto_fixable)
    
    def get_by_severity(self, severity: Severity) -> list[Finding]:
        """Retorna findings de uma severidade específica"""
        return [f for f in self.findings if f.severity == severity]
    
    def get_by_checker(self, checker: str) -> list[Finding]:
        """Retorna findings de um checker específico"""
        return [f for f in self.findings if f.checker == checker]
    
    def add_finding(self, finding: Finding) -> None:
        """Adiciona um finding ao resultado"""
        self.findings.append(finding)
    
    def to_dict(self) -> dict[str, Any]:
        """Converte para dicionário"""
        return {
            "project_path": str(self.project_path),
            "project_name": self.project_name,
            "timestamp": self.timestamp.isoformat(),
            "findings": [f.model_dump() for f in self.findings],
            "duration_ms": self.duration_ms,
            "checkers_run": self.checkers_run,
            "summary": self.summary,
        }
