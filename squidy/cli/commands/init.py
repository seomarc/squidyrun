"""
Init Command - Comando de inicialização de projeto
"""

import getpass
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn

from squidy.adapters.providers.openai_adapter import OpenAIAdapter
from squidy.adapters.providers.anthropic_adapter import AnthropicAdapter
from squidy.adapters.providers.openrouter_adapter import OpenRouterAdapter
from squidy.core.domain.config import ProjectConfig
from squidy.core.ports.ai_provider import AIProviderPort
from squidy.core.ports.filesystem import FileSystemPort
from squidy.generation.file_generator import FileGenerator


class InitCommand:
    """Comando de inicialização de projeto Squidy"""
    
    def __init__(self, fs: FileSystemPort, console: Console):
        self.fs = fs
        self.console = console
    
    def execute(
        self,
        path: Path,
        dry_run: bool = False,
        only_missing: bool = False,
        manual: bool = False,
        provider: str = "openai",
    ) -> None:
        """Executa comando init"""
        
        # Resolve caminho absoluto
        target_path = path.resolve()
        
        # Cria diretório se não existir
        if not self.fs.exists(target_path):
            self.console.print(f"[dim]Criando diretório: {target_path}[/dim]")
            if not dry_run:
                self.fs.mkdir(target_path, parents=True, exist_ok=True)
        
        # Verifica se já existe projeto Squidy
        is_existing = self._is_squidy_project(target_path)
        
        if is_existing and not only_missing:
            self.console.print(f"\n[yellow]⚠️  Já existe um projeto Squidy em {target_path}[/yellow]")
            if not Confirm.ask("Deseja sobrescrever?", default=False):
                self.console.print("[dim]Operação cancelada.[/dim]")
                return
        
        # Obtém configuração
        if manual:
            config = self._manual_config()
        else:
            config = self._ai_config(provider)
        
        if not config:
            self.console.print("[red]❌ Não foi possível obter configuração[/red]")
            return
        
        # Preview em dry-run
        if dry_run:
            self._show_preview(config, target_path)
            return
        
        # Gera arquivos
        self._generate_files(config, target_path, only_missing)
    
    def _is_squidy_project(self, path: Path) -> bool:
        """Verifica se diretório já é projeto Squidy"""
        readme = path / "readme-agent.md"
        constituicao = path / "doc" / "constituicao.md"
        return self.fs.exists(readme) or self.fs.exists(constituicao)
    
    def _manual_config(self) -> Optional[ProjectConfig]:
        """Obtém configuração manual do usuário"""
        self.console.print("\n[bold cyan]📝 Setup Manual[/bold cyan]\n")
        
        # Informações básicas
        project_name = Prompt.ask(
            "Nome do projeto (kebab-case)",
            default="meu-projeto"
        )
        display_name = Prompt.ask(
            "Nome apresentável",
            default=project_name.replace("-", " ").title()
        )
        proposito = Prompt.ask(
            "Propósito do projeto (1-2 frases)"
        )
        
        # Stack
        self.console.print("\n[bold]Stack Tecnológica:[/bold]")
        frontend = Prompt.ask(
            "Frontend",
            choices=["React", "Vue", "Angular", "Svelte", "None", "Outro"],
            default="React"
        )
        if frontend == "Outro":
            frontend = Prompt.ask("Especifique o frontend")
        
        backend = Prompt.ask(
            "Backend",
            default="Node.js/Express"
        )
        
        banco = Prompt.ask(
            "Banco de dados",
            choices=["PostgreSQL", "MySQL", "MongoDB", "SQLite", "Outro"],
            default="PostgreSQL"
        )
        if banco == "Outro":
            banco = Prompt.ask("Especifique o banco")
        
        # Tipo de agente
        agent_type = Prompt.ask(
            "Tipo de agente",
            choices=[
                "desenvolvedor-fullstack",
                "desenvolvedor-backend",
                "desenvolvedor-frontend",
                "devops"
            ],
            default="desenvolvedor-fullstack"
        )
        
        return ProjectConfig(
            project_name=project_name,
            display_name=display_name,
            agent_type=agent_type,
            proposito=proposito,
            stack={
                "frontend": frontend,
                "backend": backend,
                "banco": banco,
            },
        )
    
    def _ai_config(self, provider_name: str) -> Optional[ProjectConfig]:
        """Obtém configuração via entrevista com IA"""
        self.console.print("\n[bold cyan]🤖 Setup com IA[/bold cyan]\n")
        
        # Seleciona provider
        provider = self._select_provider(provider_name)
        if not provider:
            return None
        
        # Executa entrevista
        config_dict = self._run_interview(provider)
        if not config_dict:
            return None
        
        return ProjectConfig.from_dict(config_dict)
    
    def _select_provider(self, provider_name: str) -> Optional[AIProviderPort]:
        """Seleciona e configura provider de IA"""
        self.console.print(f"\n[dim]Configurando provider: {provider_name}...[/dim]")
        
        # Obtém API key
        self.console.print(f"\n[blue]🔐 Digite a API key para {provider_name}:[/blue]")
        self.console.print("[dim](a chave não aparece enquanto digita)[/dim]\n")
        
        api_key = getpass.getpass("")
        
        if not api_key or len(api_key) < 10:
            self.console.print("[red]❌ API key inválida[/red]")
            return None
        
        # Cria provider
        if provider_name.lower() == "openai":
            provider = OpenAIAdapter(api_key)
        elif provider_name.lower() == "anthropic":
            provider = AnthropicAdapter(api_key)
        elif provider_name.lower() == "openrouter":
            provider = OpenRouterAdapter(api_key)
        else:
            self.console.print(f"[red]❌ Provider desconhecido: {provider_name}[/red]")
            return None
        
        # Testa conexão
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True,
        ) as progress:
            progress.add_task("[dim]Verificando conexão...[/dim]", total=None)
            
            if not provider.test_connection():
                self.console.print(f"[red]❌ Não foi possível conectar ao {provider_name}[/red]")
                self.console.print("[dim]Verifique sua API key e conexão com a internet[/dim]")
                return None
        
        self.console.print(f"[green]✓ Conectado ao {provider_name}[/green]\n")
        return provider
    
    def _run_interview(self, provider: AIProviderPort) -> Optional[dict]:
        """Executa entrevista adaptativa com IA"""
        self.console.print("[bold]Entrevista com Agente IA[/bold]\n")
        self.console.print(
            "[dim]Vou fazer algumas perguntas sobre seu projeto. "
            "Responda naturalmente, como em uma conversa.[/dim]\n"
        )
        
        # Descrição inicial
        self.console.print("[bold cyan]🤖 Agente:[/bold cyan] Olá! Me conte sobre o projeto que você quer configurar.")
        self.console.print("[dim]           Exemplo: 'API REST para delivery com Node e PostgreSQL'[/dim]")
        
        project_description = Prompt.ask("[bold white]   Você[/bold white]")
        
        if not project_description or len(project_description.strip()) < 10:
            self.console.print("[yellow]⚠️ Descrição muito curta. Tente novamente.[/yellow]\n")
            return self._run_interview(provider)
        
        self.console.print("")
        
        # Loop de Q&A
        qa_history = []
        max_questions = 6
        
        for i in range(max_questions):
            # Gera próxima pergunta
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
                transient=True,
            ) as progress:
                progress.add_task("[dim]Pensando...[/dim]", total=None)
                
                question = provider.generate_interview_question(
                    project_description=project_description,
                    qa_history=qa_history,
                    question_count=i,
                )
            
            # Verifica se deve parar
            if question == "READY":
                self.console.print(f"[green]✓ Contexto suficiente coletado ({i} pergunta(s))[/green]\n")
                break
            
            # Mostra pergunta
            self.console.print(f"[bold cyan]🤖 Agente:[/bold cyan] {question}")
            answer = Prompt.ask("[bold white]   Você[/bold white]")
            
            if not answer or len(answer.strip()) < 2:
                self.console.print("[yellow]⚠️ Resposta muito curta[/yellow]\n")
                continue
            
            qa_history.append((question, answer.strip()))
            self.console.print("")
        
        # Gera configuração
        self.console.print("[dim]Gerando configuração...[/dim]")
        
        # Monta contexto completo
        full_context = f"PROJETO: {project_description}\n\n"
        for q, a in qa_history:
            full_context += f"P: {q}\nR: {a}\n\n"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True,
        ) as progress:
            progress.add_task("[dim]Processando com IA...[/dim]", total=None)
            config = provider.generate_config(full_context)
        
        return config
    
    def _show_preview(self, config: ProjectConfig, path: Path) -> None:
        """Mostra preview em modo dry-run"""
        self.console.print("\n[bold yellow]🔍 PREVIEW (Dry Run)[/bold yellow]\n")
        
        self.console.print(f"[dim]Diretório:[/dim] {path}")
        self.console.print(f"[dim]Projeto:[/dim] {config.display_name}")
        self.console.print(f"[dim]Stack:[/dim] {config.stack}\n")
        
        self.console.print("[dim]Arquivos que seriam criados:[/dim]")
        files = [
            "readme-agent.md",
            "doc/AGENT.md",
            "doc/constituicao.md",
            "doc/oraculo.md",
            "doc/politicas.md",
            "doc/kanban.md",
            "doc/emergencia.md",
            "doc/indice-diario.md",
            "doc/contexto-sessao.md",
            f"diario/{datetime.now().strftime('%Y-%m')}.md",
        ]
        for f in files:
            self.console.print(f"  [green]+[/green] {f}")
        
        self.console.print("\n[dim]Execute sem --dry-run para criar os arquivos.[/dim]\n")
    
    def _generate_files(
        self,
        config: ProjectConfig,
        path: Path,
        only_missing: bool,
    ) -> None:
        """Gera arquivos do projeto"""
        
        generator = FileGenerator(self.fs)
        
        if only_missing:
            # TODO: Implementar geração apenas de arquivos faltantes
            self.console.print("[yellow]⚠️ Modo --only-missing ainda não implementado[/yellow]")
            self.console.print("[dim]Gerando todos os arquivos...[/dim]\n")
        
        # Gera arquivos
        generated = generator.generate_all(config, path, progress=True)
        
        # Mostra resultado
        self.console.print(f"\n[bold green]✅ Setup concluído![/bold green]\n")
        self.console.print(f"[dim]Arquivos gerados em:[/dim] [cyan]{path}[/cyan]\n")
        
        self.console.print("[dim]Próximos passos:[/dim]")
        self.console.print(f"  [bright_cyan]1.[/bright_cyan] Diga ao seu agente: [bold]\"Acesse {path}/readme-agent.md e siga o ritual\"[/bold]")
        self.console.print(f"  [bright_cyan]2.[/bright_cyan] Revise [cyan]{path}/doc/constituicao.md[/cyan]")
        self.console.print(f"  [bright_cyan]3.[/bright_cyan] Adicione tarefas em [cyan]{path}/doc/kanban.md[/cyan]")
        self.console.print()
