"""
AI Provider Port - Interface abstrata para provedores de IA

Esta interface permite trocar facilmente entre diferentes
provedores (OpenAI, Anthropic, OpenRouter, etc).
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class AIProviderPort(ABC):
    """
    Interface abstrata para provedores de IA
    
    Implementações:
        - OpenAIAdapter: OpenAI API (GPT-4, GPT-3.5)
        - AnthropicAdapter: Anthropic API (Claude)
        - OpenRouterAdapter: OpenRouter (multi-model)
    """
    
    name: str = "BaseProvider"
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        Testa conexão com o provedor
        
        Returns:
            True se conexão OK, False caso contrário
        """
        pass
    
    @abstractmethod
    def generate_interview_question(
        self,
        project_description: str,
        qa_history: list[tuple[str, str]],
        question_count: int,
    ) -> str:
        """
        Gera próxima pergunta da entrevista
        
        Args:
            project_description: Descrição inicial do projeto
            qa_history: Histórico de Q&A [(pergunta, resposta), ...]
            question_count: Número da pergunta atual
            
        Returns:
            Próxima pergunta ou "READY" se suficiente
        """
        pass
    
    @abstractmethod
    def generate_config(self, full_context: str) -> dict[str, Any]:
        """
        Gera configuração Squidy a partir do contexto da entrevista
        
        Args:
            full_context: Contexto completo (descrição + Q&A)
            
        Returns:
            Dicionário com configuração do projeto
        """
        pass
    
    @abstractmethod
    def refine_task(self, task_description: str, project_context: dict) -> dict:
        """
        Refina uma tarefa vaga em subtarefas específicas
        
        Args:
            task_description: Descrição da tarefa
            project_context: Contexto do projeto
            
        Returns:
            Dicionário com subtarefas e critérios
        """
        pass
    
    @abstractmethod
    def analyze_project(self, project_files: dict[str, str]) -> dict:
        """
        Analisa arquivos do projeto e sugere melhorias
        
        Args:
            project_files: Dict {caminho: conteúdo}
            
        Returns:
            Análise e sugestões
        """
        pass
    
    def _sanitize_json_response(self, content: str) -> str:
        """
        Remove markdown code blocks de respostas JSON
        
        Args:
            content: Conteúdo bruto da resposta
            
        Returns:
            JSON limpo
        """
        if "```json" in content:
            return content.split("```json")[1].split("```")[0].strip()
        if "```" in content:
            return content.split("```")[1].split("```")[0].strip()
        return content.strip()
