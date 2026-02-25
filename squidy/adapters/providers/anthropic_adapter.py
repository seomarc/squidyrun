"""
Anthropic Adapter

Implementação do AIProviderPort para Anthropic API (Claude).
"""

import json
from pathlib import Path
from typing import Any

import yaml
from anthropic import AuthenticationError, APIConnectionError, APIStatusError

from squidy.core.ports.ai_provider import AIProviderPort


class AnthropicAdapter(AIProviderPort):
    """
    Adapter para Anthropic API (Claude)
    
    Usa Claude 3 Haiku para perguntas (rápido e barato)
    e Claude 3.5 Sonnet para geração de config (alta qualidade).
    """
    
    name = "Anthropic"
    
    # Modelos
    INTERVIEW_MODEL = "claude-3-haiku-20240307"
    CONFIG_MODEL = "claude-3-5-sonnet-20241022"
    REFINE_MODEL = "claude-3-haiku-20240307"
    
    def __init__(self, api_key: str):
        """
        Inicializa adapter Anthropic
        
        Args:
            api_key: API key da Anthropic (sk-ant-...)
        """
        self.api_key = api_key
        self._client = None
    
    @property
    def client(self):
        """Lazy initialization do cliente"""
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client
    
    def _load_prompts(self, language: str) -> dict:
        """Carrega prompts do arquivo YAML para o idioma especificado."""
        if language not in ["pt-BR", "en-US"]:
            language = "pt-BR"
        
        module_dir = Path(__file__).parent.parent.parent
        prompts_file = module_dir / "locales" / language / "prompts.yaml"
        
        try:
            with open(prompts_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception:
            if language != "pt-BR":
                return self._load_prompts("pt-BR")
            return {}
    
    def test_connection(self) -> bool:
        """Testa conexão com Anthropic"""
        try:
            response = self.client.messages.create(
                model=self.INTERVIEW_MODEL,
                max_tokens=5,
                messages=[{"role": "user", "content": "Hi"}]
            )
            return True
        except (AuthenticationError, APIConnectionError, APIStatusError):
            return False
        except Exception:
            return False
    
    def generate_interview_question(
        self,
        project_description: str,
        qa_history: list[tuple[str, str]],
        question_count: int,
        language: str = "pt-BR",
    ) -> str:
        """Gera próxima pergunta da entrevista"""
        prompts = self._load_prompts(language)
        interview_prompts = prompts.get("interview", {})
        
        system_prompt = interview_prompts.get("system_prompt", self._default_interview_prompt())

        # Monta mensagens
        messages = [{"role": "user", "content": project_description}]
        
        for question, answer in qa_history:
            messages.append({"role": "assistant", "content": question})
            messages.append({"role": "user", "content": answer})
        
        # Força READY após 5 perguntas
        ready_instruction = "You have asked enough questions. Reply only: READY" if language == "en-US" else "Você já fez perguntas suficientes. Responda apenas: READY"
        if question_count >= 5:
            extra_instruction = f"\n\n[{ready_instruction}]"
            if messages:
                messages[-1]["content"] += extra_instruction
        
        try:
            response = self.client.messages.create(
                model=self.INTERVIEW_MODEL,
                max_tokens=80,
                system=system_prompt,
                messages=messages,
            )
            
            question = response.content[0].text.strip()
            
            ready_keywords = interview_prompts.get("ready_keywords", ["READY", "PRONTO", "DONE"])
            if question.upper() in [k.upper() for k in ready_keywords]:
                return "READY"
            
            return question
            
        except Exception:
            fallback_question = interview_prompts.get("fallback_question", "What is the main technology you plan to use?" if language == "en-US" else "Qual tecnologia principal você pretende usar?")
            if question_count >= 3:
                return "READY"
            return fallback_question
    
    def generate_config(self, full_context: str, language: str = "pt-BR") -> dict[str, Any]:
        """Gera configuração Squidy a partir do contexto"""
        prompts = self._load_prompts(language)
        config_prompts = prompts.get("config", {})
        
        system_prompt = config_prompts.get("system_prompt", self._default_config_prompt())
        
        user_prompt = f"Context:\n{full_context}\n\nGenerate configuration JSON:" if language == "en-US" else f"Contexto:\n{full_context}\n\nGere configuração JSON:"

        try:
            response = self.client.messages.create(
                model=self.CONFIG_MODEL,
                max_tokens=2000,
                temperature=0.3,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            
            config_text = self._sanitize_json_response(response.content[0].text.strip())
            config = json.loads(config_text)
            
            required = config_prompts.get("required_fields", ["project_name", "display_name", "proposito", "stack"])
            for field in required:
                if field not in config:
                    raise ValueError(f"Campo obrigatório faltando: {field}")
            
            return config
            
        except json.JSONDecodeError as e:
            return self._fallback_config(full_context, f"JSON error: {e}", language)
        except Exception as e:
            return self._fallback_config(full_context, str(e), language)
    
    def refine_task(self, task_description: str, project_context: dict, language: str = "pt-BR") -> dict:
        """Refina uma tarefa vaga em subtarefas"""
        if language == "en-US":
            return {
                "task": task_description,
                "subtasks": [
                    {"id": "SUB-001", "description": "Analyze requirements", "estimated_time": "30min"},
                    {"id": "SUB-002", "description": "Implement", "estimated_time": "2h"},
                    {"id": "SUB-003", "description": "Test", "estimated_time": "30min"},
                ]
            }
        else:
            return {
                "task": task_description,
                "subtasks": [
                    {"id": "SUB-001", "description": "Analisar requisitos", "estimated_time": "30min"},
                    {"id": "SUB-002", "description": "Implementar", "estimated_time": "2h"},
                    {"id": "SUB-003", "description": "Testar", "estimated_time": "30min"},
                ]
            }
    
    def analyze_project(self, project_files: dict[str, str], language: str = "pt-BR") -> dict:
        """Analisa arquivos do projeto"""
        if language == "en-US":
            return {
                "analysis": "Basic analysis",
                "suggestions": ["Add tests", "Improve docs"],
            }
        else:
            return {
                "analysis": "Análise básica",
                "suggestions": ["Adicionar testes", "Melhorar docs"],
            }
    
    def _default_interview_prompt(self) -> str:
        """Prompt padrão de entrevista"""
        return """Você é um Arquiteto de Software Sênior amigável, especialista em entender necessidades de projetos.

ESTILO:
- Conduza uma conversa natural (não interrogatório)
- Seja caloroso: "Legal! Me conta mais sobre..."
- Faça UMA pergunta específica por vez
- Máximo 20 palavras
- NUNCA repita perguntas
- Use follow-ups inteligentes

ESTRUTURA (5 fases):
1. Contexto de Negócio - problema, usuários
2. Stack Tecnológica - tecnologias
3. Arquitetura - padrões
4. Qualidade - testes, CI/CD
5. Time - prazos

SUGESTÕES: "Para MVP, X pode ser mais simples"

QUANDO "READY": Após cobrir contexto + stack + arquitetura

FORMATO: Apenas a pergunta"""
    
    def _default_config_prompt(self) -> str:
        """Prompt padrão de configuração"""
        return """Você é o Gerador de Configuração Squidy.

Gere JSON enriquecido com:
- project_name, display_name, agent_type
- proposito, contexto_negocio (problema, usuarios, valor)
- stack (frontend, backend, banco)
- arquitetura (padrao, camadas, integracoes)
- qualidade (cobertura, ferramentas, ci_cd)
- principios (acionáveis), proibicoes (com consequência), dod
- restricoes, convencoes (nomenclatura completa)

REGRAS:
1. Baseie-se APENAS no contexto
2. Seja ESPECÍFICO
3. Principios ACIONÁVEIS
4. Retorne APENAS JSON"""
    
    def _fallback_config(self, context: str, error: str, language: str = "pt-BR") -> dict[str, Any]:
        """Configuração de fallback"""
        if language == "en-US":
            return {
                "project_name": "squidy-project",
                "display_name": "Squidy Project",
                "agent_type": "fullstack-developer",
                "purpose": "Project with fallback configuration",
                "stack": {"frontend": "React", "backend": "Node.js", "database": "PostgreSQL"},
                "principles": ["Clean code", "Automated tests"],
                "prohibitions": ["Never commit without tests"],
                "dod": ["Tests passing"],
                "provider": "Anthropic",
                "version": "2.0.0",
                "_fallback": True,
                "_error": error,
            }
        else:
            return {
                "project_name": "projeto-squidy",
                "display_name": "Projeto Squidy",
                "agent_type": "desenvolvedor-fullstack",
                "proposito": "Projeto com configuração de fallback",
                "stack": {"frontend": "React", "backend": "Node.js", "banco": "PostgreSQL"},
                "principios": ["Código limpo", "Testes automatizados"],
                "proibicoes": ["Nunca commitar sem testes"],
                "dod": ["Testes passando"],
                "provider": "Anthropic",
                "version": "2.0.0",
                "_fallback": True,
                "_error": error,
            }
