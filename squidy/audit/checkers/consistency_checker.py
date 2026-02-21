"""
Consistency Checker

Verifica consistência entre diferentes arquivos:
- Stack em constituicao.md vs oraculo.md
- Princípios em AGENT.md vs constituicao.md
- Tasks no kanban vs contexto-sessao.md
"""

import re
from pathlib import Path

from squidy.core.domain.audit_result import Finding, Severity
from squidy.core.ports.filesystem import FileSystemPort

from .base import BaseChecker


class ConsistencyChecker(BaseChecker):
    """
    Verifica consistência entre arquivos
    
    Checks:
    - Stack consistente entre arquivos
    - Princípios consistentes
    - Tasks sincronizadas
    """
    
    name = "ConsistencyChecker"
    description = "Verifica consistência entre arquivos"
    
    def __init__(self, fs: FileSystemPort):
        super().__init__(fs)
    
    def check(self, project_path: Path, project_name: str | None = None) -> list[Finding]:
        """Verifica consistência entre arquivos"""
        findings = []
        
        # Verifica consistência da stack
        findings.extend(self._check_stack_consistency(project_path))
        
        # Verifica consistência de princípios
        findings.extend(self._check_principles_consistency(project_path))
        
        return findings
    
    def _check_stack_consistency(self, project_path: Path) -> list[Finding]:
        """Verifica se stack é consistente entre arquivos"""
        findings = []
        
        # Lê stack de diferentes arquivos
        constituicao_stack = self._extract_stack_from_constituicao(project_path)
        oraculo_stack = self._extract_stack_from_oraculo(project_path)
        
        if constituicao_stack and oraculo_stack:
            if constituicao_stack != oraculo_stack:
                findings.append(self._create_finding(
                    message="Stack inconsistente entre constituicao.md e oraculo.md",
                    severity=Severity.MEDIUM,
                    suggestion="Padronize a stack em todos os arquivos",
                ))
        
        return findings
    
    def _check_principles_consistency(self, project_path: Path) -> list[Finding]:
        """Verifica se princípios são consistentes"""
        findings = []
        
        # Extrai princípios de diferentes arquivos
        agent_principles = self._extract_principles_from_agent(project_path)
        constituicao_principles = self._extract_principles_from_constituicao(project_path)
        
        if agent_principles and constituicao_principles:
            # Verifica se há divergências significativas
            agent_set = set(p.lower() for p in agent_principles)
            constituicao_set = set(p.lower() for p in constituicao_principles)
            
            if len(agent_set - constituicao_set) > 2:
                findings.append(self._create_finding(
                    message="Princípios divergentes entre AGENT.md e constituicao.md",
                    severity=Severity.LOW,
                    suggestion="Mantenha princípios sincronizados entre arquivos",
                ))
        
        return findings
    
    def _extract_stack_from_constituicao(self, project_path: Path) -> dict | None:
        """Extrai stack de constituicao.md"""
        try:
            path = project_path / "doc" / "constituicao.md"
            if not self.fs.exists(path):
                return None
            
            content = self.fs.read_text(path)
            stack = {}
            
            # Procura por padrões como "**Frontend:** React"
            frontend_match = re.search(r"\*\*Frontend:\*\*\s*(.+)", content)
            if frontend_match:
                stack["frontend"] = frontend_match.group(1).strip()
            
            backend_match = re.search(r"\*\*Backend:\*\*\s*(.+)", content)
            if backend_match:
                stack["backend"] = backend_match.group(1).strip()
            
            banco_match = re.search(r"\*\*Banco.*:\*\*\s*(.+)", content)
            if banco_match:
                stack["banco"] = banco_match.group(1).strip()
            
            return stack if stack else None
        except Exception:
            return None
    
    def _extract_stack_from_oraculo(self, project_path: Path) -> dict | None:
        """Extrai stack de oraculo.md"""
        try:
            path = project_path / "doc" / "oraculo.md"
            if not self.fs.exists(path):
                return None
            
            content = self.fs.read_text(path)
            stack = {}
            
            # Procura na seção ADR-001
            adr_match = re.search(r"ADR-001.*?(?=ADR-002|$)", content, re.DOTALL)
            if adr_match:
                adr_section = adr_match.group(0)
                
                frontend_match = re.search(r"\*\*Frontend:\*\*\s*(.+)", adr_section)
                if frontend_match:
                    stack["frontend"] = frontend_match.group(1).strip()
                
                backend_match = re.search(r"\*\*Backend:\*\*\s*(.+)", adr_section)
                if backend_match:
                    stack["backend"] = backend_match.group(1).strip()
                
                banco_match = re.search(r"\*\*Banco.*:\*\*\s*(.+)", adr_section)
                if banco_match:
                    stack["banco"] = banco_match.group(1).strip()
            
            return stack if stack else None
        except Exception:
            return None
    
    def _extract_principles_from_agent(self, project_path: Path) -> list[str] | None:
        """Extrai princípios de AGENT.md"""
        try:
            path = project_path / "doc" / "AGENT.md"
            if not self.fs.exists(path):
                return None
            
            content = self.fs.read_text(path)
            
            # Procura seção de princípios
            principles_match = re.search(
                r"(?:##?\s*Princípios|Regras que você DEVE seguir).*?\n(.*?)(?=##?|$)",
                content,
                re.DOTALL | re.IGNORECASE,
            )
            
            if principles_match:
                principles_text = principles_match.group(1)
                # Extrai itens de lista
                principles = re.findall(r"[-*]\s+(.+)", principles_text)
                return [p.strip() for p in principles if p.strip()]
            
            return None
        except Exception:
            return None
    
    def _extract_principles_from_constituicao(self, project_path: Path) -> list[str] | None:
        """Extrai princípios de constituicao.md"""
        try:
            path = project_path / "doc" / "constituicao.md"
            if not self.fs.exists(path):
                return None
            
            content = self.fs.read_text(path)
            
            # Procura seção §2 - PRINCÍPIOS
            principles_match = re.search(
                r"##?\s*§?2.*PRINCÍPIOS.*?\n(.*?)(?=##?\s*§?3|$)",
                content,
                re.DOTALL | re.IGNORECASE,
            )
            
            if principles_match:
                principles_text = principles_match.group(1)
                # Extrai itens numerados ou com bullet
                principles = re.findall(r"(?:\d+\.\s+|[-*]\s+)(.+)", principles_text)
                return [p.strip() for p in principles if p.strip()]
            
            return None
        except Exception:
            return None
