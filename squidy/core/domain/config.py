"""
Configuração do projeto Squidy
"""

from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator


class StackConfig(BaseModel):
    """Configuração da stack tecnológica"""
    
    frontend: str = Field(default="None", description="Framework frontend")
    backend: str = Field(default="Python/FastAPI", description="Framework backend")
    banco: str = Field(default="PostgreSQL", description="Banco de dados")
    
    def __str__(self) -> str:
        parts = []
        if self.frontend and self.frontend != "None":
            parts.append(self.frontend)
        if self.backend:
            parts.append(self.backend)
        if self.banco:
            parts.append(self.banco)
        return " · ".join(parts) if parts else "Stack não definida"


class ConventionsConfig(BaseModel):
    """Convenções de nomenclatura do projeto"""
    
    variaveis: str = Field(default="camelCase", description="Convenção para variáveis")
    funcoes: str = Field(default="camelCase", description="Convenção para funções")
    classes: str = Field(default="PascalCase", description="Convenção para classes")
    constantes: str = Field(default="UPPER_SNAKE", description="Convenção para constantes")
    arquivos: str = Field(default="kebab-case", description="Convenção para arquivos")
    banco: str = Field(default="snake_case", description="Convenção para banco de dados")


class ProjectConfig(BaseModel):
    """
    Configuração completa de um projeto Squidy
    
    Esta configuração é gerada pela entrevista com IA e usada
    para gerar todos os arquivos de documentação.
    """
    
    # Identificação
    project_name: str = Field(..., description="Nome do projeto (kebab-case)")
    display_name: str = Field(..., description="Nome apresentável")
    agent_type: str = Field(
        default="desenvolvedor-fullstack",
        description="Tipo de agente (desenvolvedor-fullstack|backend|frontend|devops)"
    )
    
    # Contexto
    proposito: str = Field(..., description="Propósito do projeto em 1-2 frases")
    contexto_negocio: Optional[dict[str, str]] = Field(
        default=None,
        description="Contexto de negócio (problema, usuários, valor)"
    )
    
    # Stack
    stack: StackConfig = Field(default_factory=StackConfig)
    
    # Arquitetura
    arquitetura: Optional[dict[str, Any]] = Field(
        default=None,
        description="Decisões de arquitetura (padrão, camadas, integrações)"
    )
    
    # Qualidade
    qualidade: Optional[dict[str, Any]] = Field(
        default=None,
        description="Configurações de qualidade (testes, cobertura, CI/CD)"
    )
    
    # Governança
    principios: list[str] = Field(
        default_factory=list,
        validate_default=True,
        description="Princípios do projeto (o que SEMPRE fazer)"
    )
    proibicoes: list[str] = Field(
        default_factory=list,
        validate_default=True,
        description="Proibições do projeto (o que NUNCA fazer)"
    )
    dod: list[str] = Field(
        default_factory=list,
        validate_default=True,
        description="Definition of Done (critérios de pronto)"
    )
    restricoes: list[str] = Field(
        default_factory=list,
        description="Restrições técnicas"
    )
    
    # Convenções
    convencoes: ConventionsConfig = Field(default_factory=ConventionsConfig)
    
    # Metadados
    provider: Optional[str] = Field(default=None, description="Provedor de IA usado")
    generated_at: Optional[str] = Field(default=None, description="Data de geração")
    version: str = Field(default="2.0.0", description="Versão do Squidy")
    
    @field_validator("principios")
    @classmethod
    def validate_principios(cls, v: list[str]) -> list[str]:
        """Garante que há princípios definidos"""
        if not v:
            return [
                "Manter código limpo e legível",
                "Escrever testes automatizados",
                "Documentar decisões importantes",
                "Fazer code review antes de merge",
            ]
        return v
    
    @field_validator("proibicoes")
    @classmethod
    def validate_proibicoes(cls, v: list[str]) -> list[str]:
        """Garante que há proibições definidas"""
        if not v:
            return [
                "Nunca commitar código sem testes",
                "Nunca subir credenciais ou secrets",
                "Nunca fazer deploy sem CI passar",
                "Nunca pular code review",
            ]
        return v
    
    @field_validator("dod")
    @classmethod
    def validate_dod(cls, v: list[str]) -> list[str]:
        """Garante que há DoD definido"""
        if not v:
            return [
                "Testes unitários passando",
                "Code review aprovado",
                "Documentação atualizada",
                "CI/CD pipeline verde",
                "Sem warnings do linter",
            ]
        return v
    
    def to_dict(self) -> dict[str, Any]:
        """Converte para dicionário"""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectConfig":
        """Cria instância a partir de dicionário (aceita chaves em inglês ou português)"""
        # Mapeia chaves em inglês para português (geradas pelo prompt en-US)
        top_level_map = {
            "purpose": "proposito",
            "business_context": "contexto_negocio",
            "architecture": "arquitetura",
            "quality": "qualidade",
            "principles": "principios",
            "prohibitions": "proibicoes",
            "restrictions": "restricoes",
            "conventions": "convencoes",
        }
        normalized = {top_level_map.get(k, k): v for k, v in data.items()}

        # Normaliza stack: database → banco
        if "stack" in normalized and isinstance(normalized["stack"], dict):
            stack = dict(normalized["stack"])
            if "database" in stack and "banco" not in stack:
                stack["banco"] = stack.pop("database")
            normalized["stack"] = stack

        # Normaliza convencoes: chaves em inglês → português
        if "convencoes" in normalized and isinstance(normalized["convencoes"], dict):
            conv_map = {
                "variables": "variaveis",
                "functions": "funcoes",
                "constants": "constantes",
                "files": "arquivos",
                "database": "banco",
            }
            normalized["convencoes"] = {
                conv_map.get(k, k): v for k, v in normalized["convencoes"].items()
            }

        return cls(**normalized)
    
    def __str__(self) -> str:
        return f"ProjectConfig({self.project_name})"
    
    def __repr__(self) -> str:
        return f"<ProjectConfig name={self.project_name} stack={self.stack}>"
