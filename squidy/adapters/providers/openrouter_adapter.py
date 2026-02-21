"""
OpenRouter Adapter

Implementação do AIProviderPort para OpenRouter API.
OpenRouter é um gateway que permite acessar múltiplos modelos
(Claude, GPT, Mistral, etc.) através de uma única API.
"""

import json
from typing import Any

from openai import OpenAI

from squidy.core.ports.ai_provider import AIProviderPort


class OpenRouterAdapter(AIProviderPort):
    """
    Adapter para OpenRouter API
    
    Usa modelos gratuitos/bons para entrevista e configuração.
    OpenRouter é compatível com API da OpenAI.
    """
    
    name = "OpenRouter"
    
    # Endpoints
    BASE_URL = "https://openrouter.ai/api/v1"
    
    # Modelos (free tier ou baratos)
    INTERVIEW_MODEL = "google/gemma-3-12b-it:free"
    CONFIG_MODEL = "anthropic/claude-3-haiku"
    REFINE_MODEL = "google/gemma-3-12b-it:free"
    
    def __init__(self, api_key: str):
        """
        Inicializa adapter OpenRouter
        
        Args:
            api_key: API key do OpenRouter (sk-or-...)
        """
        self.api_key = api_key
        self._client: OpenAI | None = None
    
    @property
    def client(self) -> OpenAI:
        """Lazy initialization do cliente"""
        if self._client is None:
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.BASE_URL,
            )
        return self._client
    
    def test_connection(self) -> bool:
        """Testa conexão com OpenRouter"""
        try:
            response = self.client.chat.completions.create(
                model=self.INTERVIEW_MODEL,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5,
            )
            return True
        except Exception:
            return False
    
    def generate_interview_question(
        self,
        project_description: str,
        qa_history: list[tuple[str, str]],
        question_count: int,
    ) -> str:
        """Gera próxima pergunta da entrevista"""
        system_prompt = """Você é um Arquiteto de Software amigável.

ESTILO:
- Conversa natural, não interrogatório
- UMA pergunta por vez, máx 20 palavras
- Follow-ups inteligentes
- Sugestões contextuais quando útil

ESTRUTURA (5 fases):
1. Contexto de negócio
2. Stack tecnológica
3. Arquitetura
4. Qualidade
5. Time

QUANDO "READY": Após contexto + stack + arquitetura

FORMATO: Apenas a pergunta"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": project_description},
        ]
        
        for question, answer in qa_history:
            messages.append({"role": "assistant", "content": question})
            messages.append({"role": "user", "content": answer})
        
        if question_count >= 5 and messages[-1]["role"] == "user":
            messages[-1]["content"] += "\n[Responda apenas: READY]"
        
        try:
            response = self.client.chat.completions.create(
                model=self.INTERVIEW_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=80,
            )
            
            question = response.choices[0].message.content.strip()
            
            if question.upper() in ["READY", "READY.", "PRONTO"]:
                return "READY"
            
            return question
            
        except Exception:
            if question_count >= 3:
                return "READY"
            return "Qual tecnologia você vai usar?"
    
    def generate_config(self, full_context: str) -> dict[str, Any]:
        """Gera configuração Squidy"""
        system_prompt = """Gere configuração Squidy em JSON com:
- project_name, display_name, agent_type
- proposito, contexto_negocio
- stack, arquitetura, qualidade
- principios, proibicoes, dod, restricoes
- convencoes de nomenclatura

Baseie-se apenas no contexto. Retorne apenas JSON."""

        user_prompt = f"Contexto:\n{full_context}\n\nGere JSON:"

        try:
            response = self.client.chat.completions.create(
                model=self.CONFIG_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=2000,
            )
            
            config_text = self._sanitize_json_response(
                response.choices[0].message.content.strip()
            )
            config = json.loads(config_text)
            
            required = ["project_name", "display_name", "proposito", "stack"]
            for field in required:
                if field not in config:
                    raise ValueError(f"Campo obrigatório faltando: {field}")
            
            return config
            
        except json.JSONDecodeError as e:
            return self._fallback_config(full_context, f"JSON error: {e}")
        except Exception as e:
            return self._fallback_config(full_context, str(e))
    
    def refine_task(self, task_description: str, project_context: dict) -> dict:
        """Refina uma tarefa"""
        return {
            "task": task_description,
            "subtasks": [
                {"id": "SUB-001", "description": "Analisar", "estimated_time": "30min"},
                {"id": "SUB-002", "description": "Implementar", "estimated_time": "2h"},
                {"id": "SUB-003", "description": "Testar", "estimated_time": "30min"},
            ]
        }
    
    def analyze_project(self, project_files: dict[str, str]) -> dict:
        """Analisa arquivos do projeto"""
        return {
            "analysis": "Análise básica",
            "suggestions": ["Adicionar testes"],
        }
    
    def _fallback_config(self, context: str, error: str) -> dict[str, Any]:
        """Configuração de fallback"""
        return {
            "project_name": "projeto-squidy",
            "display_name": "Projeto Squidy",
            "agent_type": "desenvolvedor-fullstack",
            "proposito": "Projeto com configuração de fallback",
            "stack": {"frontend": "React", "backend": "Node.js", "banco": "PostgreSQL"},
            "principios": ["Código limpo"],
            "proibicoes": ["Nunca commitar sem testes"],
            "dod": ["Testes passando"],
            "provider": "OpenRouter",
            "version": "2.0.0",
            "_fallback": True,
            "_error": error,
        }
