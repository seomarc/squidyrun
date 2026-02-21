"""
Entidade principal SquidyProject
Representa um projeto gerenciado pelo Squidy
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class SquidyProject(BaseModel):
    """
    Representa um projeto Squidy com sua estrutura e metadados.
    
    Attributes:
        name: Nome do projeto (kebab-case)
        display_name: Nome apresentável
        path: Caminho absoluto do projeto
        version: Versão do Squidy usada
        created_at: Data de criação
        updated_at: Data da última atualização
        config: Configuração do projeto
        manifest: Manifesto do projeto (opcional)
    """
    
    name: str = Field(..., description="Nome do projeto em kebab-case")
    display_name: str = Field(..., description="Nome apresentável do projeto")
    path: Path = Field(..., description="Caminho absoluto do projeto")
    version: str = Field(default="2.0.0", description="Versão do Squidy")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    config: Optional[dict[str, Any]] = Field(default=None, description="Configuração")
    manifest: Optional[dict[str, Any]] = Field(default=None, description="Manifesto")
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Valida que o nome está em kebab-case"""
        if not v:
            raise ValueError("Nome do projeto não pode ser vazio")
        if " " in v:
            raise ValueError("Nome do projeto deve estar em kebab-case (sem espaços)")
        if v != v.lower():
            raise ValueError("Nome do projeto deve estar em minúsculas")
        return v
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def __str__(self) -> str:
        return f"SquidyProject({self.name} at {self.path})"
    
    def __repr__(self) -> str:
        return f"<SquidyProject name={self.name} path={self.path}>"
    
    @property
    def doc_path(self) -> Path:
        """Retorna o caminho da pasta doc/"""
        return self.path / "doc"
    
    @property
    def diario_path(self) -> Path:
        """Retorna o caminho da pasta diario/"""
        return self.path / "diario"
    
    @property
    def readme_agent_path(self) -> Path:
        """Retorna o caminho do readme-agent.md"""
        return self.path / "readme-agent.md"
    
    @property
    def manifest_path(self) -> Path:
        """Retorna o caminho do manifest.json"""
        return self.path / ".squidy" / "manifest.json"
    
    def is_initialized(self) -> bool:
        """Verifica se o projeto foi inicializado com Squidy"""
        return (
            self.readme_agent_path.exists()
            and self.doc_path.exists()
            and (self.doc_path / "constituicao.md").exists()
        )
    
    def get_missing_files(self) -> list[str]:
        """Retorna lista de arquivos obrigatórios faltantes"""
        required = [
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
        missing = []
        for file in required:
            if not (self.path / file).exists():
                missing.append(file)
        return missing
    
    def touch(self) -> None:
        """Atualiza o timestamp de modificação"""
        self.updated_at = datetime.now()
