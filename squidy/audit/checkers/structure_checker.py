"""
Structure Checker

Verifica se a estrutura de arquivos obrigatórios está completa.
"""

from pathlib import Path

from squidy.core.domain.audit_result import Finding, Severity
from squidy.core.ports.filesystem import FileSystemPort

from .base import BaseChecker


class StructureChecker(BaseChecker):
    """
    Verifica estrutura de arquivos obrigatórios
    
    Arquivos obrigatórios:
    - readme-agent.md (raiz)
    - doc/AGENT.md
    - doc/constituicao.md
    - doc/oraculo.md
    - doc/politicas.md
    - doc/kanban.md
    - doc/emergencia.md
    - doc/indice-diario.md
    - doc/contexto-sessao.md
    - diario/ (pasta)
    """
    
    name = "StructureChecker"
    description = "Verifica se arquivos obrigatórios existem"
    
    # Arquivos obrigatórios
    REQUIRED_FILES = [
        "readme-agent.md",
        "doc/AGENT.md",
        "doc/constituicao.md",
        "doc/oraculo.md",
        "doc/politicas.md",
        "doc/kanban.md",
        "doc/emergencia.md",
        "doc/indice-diario.md",
        "doc/contexto-sessao.md",
    ]
    
    # Diretórios obrigatórios
    REQUIRED_DIRS = [
        "doc",
        "diario",
    ]
    
    def __init__(self, fs: FileSystemPort):
        super().__init__(fs)
    
    def check(self, project_path: Path, project_name: str | None = None) -> list[Finding]:
        """
        Verifica estrutura do projeto
        
        Args:
            project_path: Caminho do projeto
            project_name: Nome do projeto
            
        Returns:
            Lista de findings
        """
        findings = []
        
        # Verifica diretórios obrigatórios
        for dir_name in self.REQUIRED_DIRS:
            dir_path = project_path / dir_name
            if not self.fs.exists(dir_path):
                findings.append(self._create_finding(
                    message=f"Diretório obrigatório ausente: {dir_name}/",
                    severity=Severity.CRITICAL,
                    suggestion=f"Crie o diretório: mkdir {dir_name}",
                    auto_fixable=True,
                ))
        
        # Verifica arquivos obrigatórios
        for file_path in self.REQUIRED_FILES:
            full_path = project_path / file_path
            if not self.fs.exists(full_path):
                findings.append(self._create_finding(
                    message=f"Arquivo obrigatório ausente: {file_path}",
                    severity=Severity.CRITICAL,
                    file=file_path,
                    suggestion=f"Gere o arquivo com: squidy init --only-missing",
                    auto_fixable=True,
                ))
            else:
                # Verifica se arquivo não está vazio
                try:
                    size = self.fs.get_size(full_path)
                    if size < 100:  # Menos de 100 bytes
                        findings.append(self._create_finding(
                            message=f"Arquivo muito pequeno (pode estar vazio): {file_path}",
                            severity=Severity.HIGH,
                            file=file_path,
                            suggestion="Regenere o arquivo",
                        ))
                except Exception:
                    pass
        
        # Verifica se há arquivos no diario/
        diario_path = project_path / "diario"
        if self.fs.exists(diario_path):
            diario_files = self.fs.glob(diario_path, "*.md")
            if not diario_files:
                findings.append(self._create_finding(
                    message="Diretório diario/ está vazio",
                    severity=Severity.LOW,
                    file="diario/",
                    suggestion="Crie o primeiro arquivo de diário",
                ))
        
        return findings
