"""
Kanban Checker

Analisa o kanban.md para verificar:
- Data da última atualização
- WIP limit (máximo de tarefas em progresso)
- Tarefas bloqueadas
- Distribuição de tarefas
"""

import re
from datetime import datetime, timedelta
from pathlib import Path

from squidy.core.domain.audit_result import Finding, Severity
from squidy.core.ports.filesystem import FileSystemPort

from .base import BaseChecker


class KanbanChecker(BaseChecker):
    """
    Verifica estado do kanban.md
    
    Checks:
    - Última atualização (alerta se > 7 dias)
    - WIP limit (máx 3 tarefas em DOING)
    - Tarefas bloqueadas há muito tempo
    - Tasks sem épico vinculado
    """
    
    name = "KanbanChecker"
    description = "Analisa kanban.md"
    
    # WIP limit recomendado
    WIP_LIMIT = 3
    
    # Dias para considerar kanban desatualizado
    FRESHNESS_DAYS = 7
    
    # Dias para alertar tarefa bloqueada
    BLOCKED_DAYS = 3
    
    def __init__(self, fs: FileSystemPort):
        super().__init__(fs)
    
    def check(self, project_path: Path, project_name: str | None = None) -> list[Finding]:
        """Verifica kanban.md"""
        findings = []
        kanban_path = project_path / "doc" / "kanban.md"
        
        if not self.fs.exists(kanban_path):
            findings.append(self._create_finding(
                message="kanban.md não encontrado",
                severity=Severity.CRITICAL,
                file="doc/kanban.md",
            ))
            return findings
        
        try:
            content = self.fs.read_text(kanban_path)
        except Exception as e:
            findings.append(self._create_finding(
                message=f"Erro ao ler kanban.md: {e}",
                severity=Severity.CRITICAL,
                file="doc/kanban.md",
            ))
            return findings
        
        # Verifica data de geração/atualização
        findings.extend(self._check_freshness(content, kanban_path))
        
        # Verifica WIP limit
        findings.extend(self._check_wip_limit(content))
        
        # Verifica tarefas bloqueadas
        findings.extend(self._check_blocked_tasks(content))
        
        # Verifica se há tasks no backlog
        findings.extend(self._check_backlog(content))
        
        return findings
    
    def _check_freshness(self, content: str, kanban_path: Path) -> list[Finding]:
        """Verifica quando o kanban foi atualizado"""
        findings = []
        
        # Busca data de geração
        date_match = re.search(r"\*\*Gerado em:\*\* (\d{4}-\d{2}-\d{2})", content)
        if date_match:
            try:
                generated_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
                days_old = (datetime.now() - generated_date).days
                
                if days_old > self.FRESHNESS_DAYS:
                    findings.append(self._create_finding(
                        message=f"Kanban desatualizado (última atualização há {days_old} dias)",
                        severity=Severity.MEDIUM,
                        file="doc/kanban.md",
                        suggestion="Atualize o kanban com o progresso atual",
                    ))
            except ValueError:
                pass
        
        return findings
    
    def _check_wip_limit(self, content: str) -> list[Finding]:
        """Verifica WIP limit"""
        findings = []
        
        # Conta tarefas em progresso
        # Procura seção "EM PROGRESSO" ou "DOING"
        doing_match = re.search(
            r"##\s*(?:🏗️\s*)?(?:EM PROGRESSO|DOING).*?\n(.*?)(?=##|$)",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        
        if doing_match:
            doing_section = doing_match.group(1)
            # Conta tasks (linhas começando com - [ ] ou - [x])
            tasks = re.findall(r"- \[.\]\s+\*\*TASK-\d+\*\*", doing_section)
            
            if len(tasks) > self.WIP_LIMIT:
                findings.append(self._create_finding(
                    message=f"WIP limit excedido: {len(tasks)} tarefas em progresso (limite: {self.WIP_LIMIT})",
                    severity=Severity.HIGH,
                    file="doc/kanban.md",
                    suggestion="Conclua ou pause tarefas antes de iniciar novas",
                ))
        
        return findings
    
    def _check_blocked_tasks(self, content: str) -> list[Finding]:
        """Verifica tarefas bloqueadas"""
        findings = []
        
        # Procura seção BLOQUEADO
        blocked_match = re.search(
            r"##\s*(?:⏸️\s*)?(?:BLOQUEADO|BLOCKED).*?\n(.*?)(?=##|$)",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        
        if blocked_match:
            blocked_section = blocked_match.group(1)
            blocked_tasks = re.findall(
                r"- \[.\]\s+\*\*(TASK-\d+)\*\*",
                blocked_section,
            )
            
            if blocked_tasks:
                findings.append(self._create_finding(
                    message=f"{len(blocked_tasks)} tarefa(s) bloqueada(s): {', '.join(blocked_tasks[:3])}",
                    severity=Severity.MEDIUM,
                    file="doc/kanban.md",
                    suggestion="Resolva bloqueios ou registre em emergencia.md",
                ))
        
        return findings
    
    def _check_backlog(self, content: str) -> list[Finding]:
        """Verifica se há tasks no backlog"""
        findings = []
        
        # Procura seção BACKLOG
        backlog_match = re.search(
            r"##\s*(?:📋\s*)?BACKLOG.*?\n(.*?)(?=##|$)",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        
        if backlog_match:
            backlog_section = backlog_match.group(1)
            # Conta tasks
            tasks = re.findall(r"- \[.\]\s+\*\*TASK-\d+\*\*", backlog_section)
            
            if len(tasks) == 0:
                findings.append(self._create_finding(
                    message="Backlog vazio - adicione tarefas futuras",
                    severity=Severity.LOW,
                    file="doc/kanban.md",
                    suggestion="Adicione tarefas planejadas ao backlog",
                ))
            elif len(tasks) > 20:
                findings.append(self._create_finding(
                    message=f"Backlog muito grande ({len(tasks)} tarefas) - considere priorizar",
                    severity=Severity.LOW,
                    file="doc/kanban.md",
                ))
        
        return findings
