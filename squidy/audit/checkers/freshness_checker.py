"""
Freshness Checker

Verifica a idade dos arquivos para identificar:
- Arquivos não modificados há muito tempo
- Contexto de sessão desatualizado
- Diário sem entradas recentes
"""

from datetime import datetime, timedelta
from pathlib import Path

from squidy.core.domain.audit_result import Finding, Severity
from squidy.core.ports.filesystem import FileSystemPort

from .base import BaseChecker


class FreshnessChecker(BaseChecker):
    """
    Verifica idade dos arquivos
    
    Checks:
    - Arquivos não modificados há > 30 dias
    - contexto-sessao.md desatualizado
    - Diário sem entradas recentes
    """
    
    name = "FreshnessChecker"
    description = "Verifica idade dos arquivos"
    
    # Dias para considerar arquivo desatualizado
    FILE_FRESHNESS_DAYS = 30
    
    # Dias para alertar contexto desatualizado
    CONTEXT_FRESHNESS_DAYS = 7
    
    # Dias para alertar diário sem atualização
    DIARY_FRESHNESS_DAYS = 7
    
    def __init__(self, fs: FileSystemPort):
        super().__init__(fs)
    
    def check(self, project_path: Path, project_name: str | None = None) -> list[Finding]:
        """Verifica idade dos arquivos"""
        findings = []
        
        # Verifica arquivos principais
        main_files = [
            "doc/constituicao.md",
            "doc/oraculo.md",
            "doc/politicas.md",
        ]
        
        for file_path in main_files:
            full_path = project_path / file_path
            if self.fs.exists(full_path):
                findings.extend(self._check_file_age(full_path, file_path))
        
        # Verifica contexto-sessao.md
        context_path = project_path / "doc" / "contexto-sessao.md"
        if self.fs.exists(context_path):
            findings.extend(self._check_context_freshness(context_path))
        
        # Verifica diário
        diario_path = project_path / "diario"
        if self.fs.exists(diario_path):
            findings.extend(self._check_diary_freshness(diario_path))
        
        return findings
    
    def _check_file_age(self, file_path: Path, relative_path: str) -> list[Finding]:
        """Verifica idade de um arquivo"""
        findings = []
        
        try:
            mtime = self.fs.get_mtime(file_path)
            last_modified = datetime.fromtimestamp(mtime)
            days_old = (datetime.now() - last_modified).days
            
            if days_old > self.FILE_FRESHNESS_DAYS:
                findings.append(self._create_finding(
                    message=f"Arquivo não modificado há {days_old} dias",
                    severity=Severity.LOW,
                    file=relative_path,
                    suggestion="Revise se o conteúdo ainda está atualizado",
                ))
        except Exception:
            pass
        
        return findings
    
    def _check_context_freshness(self, context_path: Path) -> list[Finding]:
        """Verifica se contexto-sessao.md está atualizado"""
        findings = []
        
        try:
            mtime = self.fs.get_mtime(context_path)
            last_modified = datetime.fromtimestamp(mtime)
            days_old = (datetime.now() - last_modified).days
            
            if days_old > self.CONTEXT_FRESHNESS_DAYS:
                findings.append(self._create_finding(
                    message=f"Contexto de sessão desatualizado (última atualização há {days_old} dias)",
                    severity=Severity.MEDIUM,
                    file="doc/contexto-sessao.md",
                    suggestion="Atualize o contexto ao final de cada sessão de trabalho",
                ))
        except Exception:
            pass
        
        return findings
    
    def _check_diary_freshness(self, diario_path: Path) -> list[Finding]:
        """Verifica se há entradas recentes no diário"""
        findings = []
        
        try:
            # Lista arquivos do diário
            files = self.fs.glob(diario_path, "*.md")
            
            if not files:
                findings.append(self._create_finding(
                    message="Nenhum arquivo de diário encontrado",
                    severity=Severity.MEDIUM,
                    file="diario/",
                    suggestion="Crie o primeiro arquivo de diário",
                ))
                return findings
            
            # Pega o arquivo mais recente
            latest_file = max(files, key=lambda p: self.fs.get_mtime(p))
            mtime = self.fs.get_mtime(latest_file)
            last_modified = datetime.fromtimestamp(mtime)
            days_old = (datetime.now() - last_modified).days
            
            if days_old > self.DIARY_FRESHNESS_DAYS:
                findings.append(self._create_finding(
                    message=f"Diário sem atualizações há {days_old} dias",
                    severity=Severity.MEDIUM,
                    file=f"diario/{latest_file.name}",
                    suggestion="Registre as decisões e progresso no diário regularmente",
                ))
        except Exception:
            pass
        
        return findings
