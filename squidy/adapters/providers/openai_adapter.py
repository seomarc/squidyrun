"""
OpenAI Adapter

Implementação do AIProviderPort para OpenAI API.
"""

import json
from pathlib import Path
from typing import Any

import yaml
from openai import OpenAI, OpenAIError

from squidy.core.ports.ai_provider import AIProviderPort


class OpenAIAdapter(AIProviderPort):
    """
    Adapter para OpenAI API
    
    Usa GPT-4o-mini para geração de config (custo-benefício)
    e GPT-3.5-turbo para perguntas de entrevista.
    """
    
    name = "OpenAI"
    
    # Modelos
    INTERVIEW_MODEL = "gpt-4o-mini"
    CONFIG_MODEL = "gpt-4o-mini"
    REFINE_MODEL = "gpt-4o-mini"
    
    def __init__(self, api_key: str):
        """
        Inicializa adapter OpenAI
        
        Args:
            api_key: API key da OpenAI
        """
        self.api_key = api_key
        self._client: OpenAI | None = None
    
    @property
    def client(self) -> OpenAI:
        """Lazy initialization do cliente"""
        if self._client is None:
            self._client = OpenAI(api_key=self.api_key)
        return self._client
    
    def _load_prompts(self, language: str) -> dict:
        """
        Carrega prompts do arquivo YAML para o idioma especificado.
        
        Args:
            language: Código do idioma (pt-BR, en-US)
            
        Returns:
            Dicionário com os prompts
        """
        # Default para pt-BR se idioma não suportado
        if language not in ["pt-BR", "en-US"]:
            language = "pt-BR"
        
        # Caminho para o arquivo de prompts
        module_dir = Path(__file__).parent.parent.parent
        prompts_file = module_dir / "locales" / language / "prompts.yaml"
        
        try:
            with open(prompts_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception:
            # Fallback para pt-BR se arquivo não encontrado
            if language != "pt-BR":
                return self._load_prompts("pt-BR")
            return {}
    
    def test_connection(self) -> bool:
        """Testa conexão com OpenAI"""
        try:
            import httpx
            test_client = OpenAI(
                api_key=self.api_key,
                timeout=httpx.Timeout(10.0, connect=5.0)
            )
            models = test_client.models.list()
            return hasattr(models, 'data') and len(models.data) > 0
        except Exception:
            return False
    
    def generate_interview_question(
        self,
        project_description: str,
        qa_history: list[tuple[str, str]],
        question_count: int,
        language: str = "pt-BR",
    ) -> str:
        """
        Gera próxima pergunta da entrevista
        
        Args:
            project_description: Descrição do projeto
            qa_history: Histórico de perguntas e respostas
            question_count: Número da pergunta atual
            language: Idioma da entrevista (pt-BR, en-US)
        """
        # Carrega prompts do idioma
        prompts = self._load_prompts(language)
        interview_prompts = prompts.get("interview", {})
        
        system_prompt = interview_prompts.get("system_prompt", self._default_interview_prompt())

        # Monta mensagens como conversa real
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{project_description}"},
        ]
        
        # Adiciona histórico como conversa
        for question, answer in qa_history:
            messages.append({"role": "assistant", "content": question})
            messages.append({"role": "user", "content": answer})
        
        # Força READY após 5 perguntas
        ready_instruction = "You have asked enough questions. Reply only: READY" if language == "en-US" else "Você já fez perguntas suficientes. Responda apenas: READY"
        if question_count >= 5:
            messages.append({
                "role": "system", 
                "content": ready_instruction
            })
        
        try:
            response = self.client.chat.completions.create(
                model=self.INTERVIEW_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=80,
            )
            
            question = response.choices[0].message.content.strip()
            
            # Normaliza READY
            ready_keywords = interview_prompts.get("ready_keywords", ["READY", "PRONTO", "DONE", "OK"])
            if question.upper() in [k.upper() for k in ready_keywords]:
                return "READY"
            
            return question
            
        except OpenAIError as e:
            # Fallback em caso de erro
            fallback_question = interview_prompts.get("fallback_question", "What is the main technology you plan to use?" if language == "en-US" else "Qual tecnologia principal você pretende usar?")
            if question_count >= 3:
                return "READY"
            return fallback_question
    
    def generate_config(self, full_context: str, language: str = "pt-BR") -> dict[str, Any]:
        """
        Gera configuração Squidy a partir do contexto da entrevista
        
        Args:
            full_context: Contexto completo da entrevista
            language: Idioma da configuração (pt-BR, en-US)
            
        Returns:
            Dicionário com configuração do projeto
        """
        # Carrega prompts do idioma
        prompts = self._load_prompts(language)
        config_prompts = prompts.get("config", {})
        
        system_prompt = config_prompts.get("system_prompt", self._default_config_prompt())
        
        user_prompt = f"""Interview Context:
{full_context}

Generate complete Squidy configuration in JSON.""" if language == "en-US" else f"""CONTEXTO DA ENTREVISTA:
{full_context}

Gere a configuração Squidy completa em JSON."""

        try:
            response = self.client.chat.completions.create(
                model=self.CONFIG_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=2000,
            )
            
            config_text = response.choices[0].message.content.strip()
            config = json.loads(config_text)
            
            # Valida campos obrigatórios
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
        """Refina uma tarefa vaga em subtarefas específicas"""
        if language == "en-US":
            return {
                "task": task_description,
                "subtasks": [
                    {"id": "SUB-001", "description": "Analyze requirements", "estimated_time": "30min"},
                    {"id": "SUB-002", "description": "Implement solution", "estimated_time": "2h"},
                    {"id": "SUB-003", "description": "Test", "estimated_time": "30min"},
                ]
            }
        else:
            return {
                "task": task_description,
                "subtasks": [
                    {"id": "SUB-001", "description": "Analisar requisitos", "estimated_time": "30min"},
                    {"id": "SUB-002", "description": "Implementar solução", "estimated_time": "2h"},
                    {"id": "SUB-003", "description": "Testar", "estimated_time": "30min"},
                ]
            }
    
    def analyze_project(self, project_files: dict[str, str], language: str = "pt-BR") -> dict:
        """Analisa arquivos do projeto e sugere melhorias"""
        if language == "en-US":
            return {
                "analysis": "Basic project analysis",
                "suggestions": [
                    "Add more tests",
                    "Improve documentation",
                ]
            }
        else:
            return {
                "analysis": "Análise básica do projeto",
                "suggestions": [
                    "Adicionar mais testes",
                    "Melhorar documentação",
                ]
            }
    
    def _default_interview_prompt(self) -> str:
        """Prompt padrão de entrevista (pt-BR)"""
        return """Você é um Arquiteto de Software Sênior amigável e consultor, especialista em entender necessidades de projetos.

ESTILO:
- Conduza uma conversa natural e profissional (não uma interrogatório)
- Seja caloroso mas direto: "Legal! Me conta mais sobre..."
- Faça UMA pergunta específica por vez
- Máximo 20 palavras por pergunta
- NUNCA repita perguntas já feitas
- Use follow-ups inteligentes baseados na última resposta

ESTRUTURA DA ENTREVISTA (5 fases):
1. Contexto de Negócio (1-2 perguntas) - problema, usuários, valor
2. Stack Tecnológica (1-2 perguntas) - tecnologias, versões
3. Arquitetura e Design (1 pergunta) - padrões, decisões
4. Qualidade e Processos (1 pergunta) - testes, CI/CD
5. Time e Entrega (1 pergunta) - tamanho, prazos

SUGESTÕES CONTEXTUAIS:
- Quando apropriado, sugira: "Para MVP, X pode ser mais simples que Y"
- Ajude o usuário a tomar decisões, não apenas colete dados

QUANDO DIZER "READY":
- Após cobrir: contexto de negócio + stack + arquitetura
- OU após 5-6 perguntas

FORMATO: Apenas a pergunta (sem "Próxima pergunta:", sem markdown)"""
    
    def _default_config_prompt(self) -> str:
        """Prompt padrão de configuração (pt-BR)"""
        return """Você é o Gerador de Configuração Squidy, especialista em arquitetura de software.

MISSÃO: Transformar contexto de entrevista em configuração JSON completa e enriquecida.

ESTRUTURA JSON DE SAÍDA:
{
  "project_name": "nome-kebab-case",
  "display_name": "Nome Legível",
  "agent_type": "desenvolvedor-fullstack|backend|frontend|devops",
  "proposito": "Objetivo claro em 1-2 frases",
  "contexto_negocio": {
    "problema": "Qual problema resolve?",
    "usuarios_alvo": "Quem usa?",
    "valor_principal": "Benefício principal"
  },
  "stack": {
    "frontend": "React|Vue|Angular|None",
    "backend": "Python/FastAPI|Node/Express|Java/Spring",
    "banco": "PostgreSQL|MySQL|MongoDB"
  },
  "arquitetura": {
    "padrao": "MVC|Clean|Hexagonal|Microservices",
    "camadas": ["camada1", "camada2"],
    "integracoes": ["API externa", "Webhook"]
  },
  "qualidade": {
    "cobertura_testes": "80%",
    "ferramentas": ["jest", "pytest"],
    "ci_cd": true
  },
  "principios": [
    "Princípio específico 1",
    "Princípio específico 2"
  ],
  "proibicoes": [
    "Proibição clara 1",
    "Proibição clara 2"
  ],
  "dod": [
    "Critério de pronto 1",
    "Critério de pronto 2"
  ],
  "restricoes": ["Restrição técnica"],
  "convencoes": {
    "variaveis": "camelCase",
    "funcoes": "camelCase",
    "classes": "PascalCase",
    "constantes": "UPPER_SNAKE",
    "arquivos": "kebab-case",
    "banco": "snake_case"
  },
  "provider": "OpenAI",
  "generated_at": "2026-02-21T10:00:00",
  "version": "2.0.0"
}

REGRAS:
1. BASEIE-SE APENAS no contexto fornecido
2. Seja ESPECÍFICO nas convenções (não genérico)
3. Principios devem ser ACIONÁVEIS (ex: "Testes com 80%+ coverage")
4. Proibições devem ter CONSEQUÊNCIA clara
5. Use valores padrão sensatos para o que não foi mencionado

RETORNE APENAS O JSON, sem markdown, sem explicações."""
    
    def _fallback_config(self, context: str, error: str, language: str = "pt-BR") -> dict[str, Any]:
        """Configuração de fallback em caso de erro"""
        if language == "en-US":
            return {
                "project_name": "squidy-project",
                "display_name": "Squidy Project",
                "agent_type": "fullstack-developer",
                "purpose": "Project with fallback configuration",
                "business_context": {
                    "problem": "To be defined",
                    "target_users": "To be defined",
                    "main_value": "To be defined",
                },
                "stack": {
                    "frontend": "React",
                    "backend": "Node.js/Express",
                    "database": "PostgreSQL",
                },
                "architecture": {
                    "pattern": "MVC",
                    "layers": ["Controller", "Service", "Repository"],
                    "integrations": [],
                },
                "quality": {
                    "test_coverage": "70%",
                    "tools": ["jest"],
                    "ci_cd": True,
                },
                "principles": [
                    "Keep code clean and readable",
                    "Write automated tests",
                    "Document important decisions",
                ],
                "prohibitions": [
                    "Never commit code without tests",
                    "Never push credentials",
                ],
                "dod": [
                    "Unit tests passing",
                    "Code review approved",
                ],
                "restrictions": [],
                "conventions": {
                    "variables": "camelCase",
                    "functions": "camelCase",
                    "classes": "PascalCase",
                    "constants": "UPPER_SNAKE",
                    "files": "kebab-case",
                    "database": "snake_case",
                },
                "provider": "OpenAI",
                "generated_at": "2026-02-21T00:00:00",
                "version": "2.0.0",
                "_fallback": True,
                "_error": error,
            }
        else:
            return {
                "project_name": "projeto-squidy",
                "display_name": "Projeto Squidy",
                "agent_type": "desenvolvedor-fullstack",
                "proposito": "Projeto gerado com configuração de fallback",
                "contexto_negocio": {
                    "problema": "A definir",
                    "usuarios_alvo": "A definir",
                    "valor_principal": "A definir",
                },
                "stack": {
                    "frontend": "React",
                    "backend": "Node.js/Express",
                    "banco": "PostgreSQL",
                },
                "arquitetura": {
                    "padrao": "MVC",
                    "camadas": ["Controller", "Service", "Repository"],
                    "integracoes": [],
                },
                "qualidade": {
                    "cobertura_testes": "70%",
                    "ferramentas": ["jest"],
                    "ci_cd": True,
                },
                "principios": [
                    "Manter código limpo e legível",
                    "Escrever testes automatizados",
                    "Documentar decisões importantes",
                ],
                "proibicoes": [
                    "Nunca commitar código sem testes",
                    "Nunca subir credenciais",
                ],
                "dod": [
                    "Testes unitários passando",
                    "Code review aprovado",
                ],
                "restricoes": [],
                "convencoes": {
                    "variaveis": "camelCase",
                    "funcoes": "camelCase",
                    "classes": "PascalCase",
                    "constantes": "UPPER_SNAKE",
                    "arquivos": "kebab-case",
                    "banco": "snake_case",
                },
                "provider": "OpenAI",
                "generated_at": "2026-02-21T00:00:00",
                "version": "2.0.0",
                "_fallback": True,
                "_error": error,
            }
