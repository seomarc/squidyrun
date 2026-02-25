"""
Init Command - Comando de inicialização de projeto
"""

import getpass
import json
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
from squidy.core.domain.config import ProjectConfig
from squidy.core.i18n import i18n
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
            self.console.print(f"[dim]{i18n.t('init.creating_directory')}: {target_path}[/dim]")
            if not dry_run:
                self.fs.mkdir(target_path, parents=True, exist_ok=True)
        
        # Verifica se já existe projeto Squidy
        is_existing = self._is_squidy_project(target_path)
        
        if is_existing and not only_missing:
            self.console.print(f"\n[yellow]⚠️  {i18n.t('init.already_exists', path=target_path)}[/yellow]")
            if not Confirm.ask(i18n.t('init.overwrite_confirm'), default=False):
                self.console.print(f"[dim]{i18n.t('init.operation_cancelled')}.[/dim]")
                return
        
        # Obtém configuração
        if manual:
            config = self._manual_config()
        else:
            config = self._ai_config(provider)
        
        if not config:
            self.console.print(f"[red]{i18n.t('init.config_error', default='❌ Não foi possível obter configuração')}[/red]")
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
        manifest = path / ".squidy" / "manifest.json"
        return self.fs.exists(readme) or self.fs.exists(constituicao) or self.fs.exists(manifest)
    
    def _load_language_from_manifest(self, path: Path) -> str | None:
        """
        Carrega idioma do manifest.json se existir.
        
        Args:
            path: Caminho do projeto
            
        Returns:
            Código do idioma ou None se não encontrado
        """
        manifest_path = path / ".squidy" / "manifest.json"
        
        if not self.fs.exists(manifest_path):
            return None
        
        try:
            content = self.fs.read_text(manifest_path)
            manifest = json.loads(content)
            language = manifest.get("language")
            
            # Valida idioma
            if language and language in i18n.SUPPORTED_LANGUAGES:
                return language
        except Exception:
            pass
        
        return None
    
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
        self.console.print(f"\n[bold cyan]🤖 {i18n.t('init.title')}[/bold cyan]\n")
        
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
        self.console.print(f"\n[blue]🔐 {i18n.t('init.api_key_prompt', provider=provider_name)}:[/blue]")
        self.console.print(f"[dim]{i18n.t('init.api_key_hint')}[/dim]\n")
        
        api_key = getpass.getpass("")
        
        if not api_key or len(api_key) < 10:
            self.console.print(f"[red]{i18n.t('init.api_key_invalid')}[/red]")
            return None
        
        # Cria provider
        if provider_name.lower() == "openai":
            provider = OpenAIAdapter(api_key)
        elif provider_name.lower() == "anthropic":
            provider = AnthropicAdapter(api_key)
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
            progress.add_task(f"[dim]{i18n.t('init.connection_testing')}[/dim]", total=None)
            
            if not provider.test_connection():
                self.console.print(f"[red]{i18n.t('init.connection_error', provider=provider_name)}[/red]")
                self.console.print(f"[dim]{i18n.t('init.connection_hint')}[/dim]")
                return None
        
        self.console.print(f"[green]{i18n.t('init.connection_success', provider=provider_name)}[/green]\n")
        return provider
    
    def _run_interview(self, provider: AIProviderPort) -> Optional[dict]:
        """Executa entrevista adaptativa com IA"""
        self.console.print(f"[bold]{i18n.t('init.interview_title')}[/bold]\n")
        self.console.print(
            f"[dim]{i18n.t('init.interview_description')}[/dim]\n"
        )
        
        # Descrição inicial
        self.console.print(f"[bold cyan]🤖 {i18n.t('init.interview_agent')}: [/bold cyan]{i18n.t('init.interview_agent_greeting')}")
        self.console.print(f"[dim]           {i18n.t('init.interview_example')}[/dim]")
        
        project_description = Prompt.ask(f"[bold white]   {i18n.t('init.interview_you')}[/bold white]")
        
        if not project_description or len(project_description.strip()) < 10:
            self.console.print(f"[yellow]{i18n.t('init.description_short')}[/yellow]\n")
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
                progress.add_task(f"[dim]{i18n.t('init.interview_thinking')}[/dim]", total=None)
                
                question = provider.generate_interview_question(
                    project_description=project_description,
                    qa_history=qa_history,
                    question_count=i,
                    language=i18n.get_language(),
                )
            
            # Verifica se deve parar
            if question == "READY":
                self.console.print(f"[green]{i18n.t('init.interview_context_ready', count=i)}[/green]\n")
                break
            
            # Mostra pergunta
            self.console.print(f"[bold cyan]🤖 {i18n.t('init.interview_agent')}:[/bold cyan] {question}")
            answer = Prompt.ask(f"[bold white]   {i18n.t('init.interview_you')}[/bold white]")
            
            if not answer or len(answer.strip()) < 2:
                self.console.print(f"[yellow]{i18n.t('init.answer_short')}[/yellow]\n")
                continue
            
            qa_history.append((question, answer.strip()))
            self.console.print("")
        
        # Gera configuração
        self.console.print(f"[dim]{i18n.t('init.interview_generating')}[/dim]")
        
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
            progress.add_task(f"[dim]{i18n.t('init.interview_processing')}[/dim]", total=None)
            config = provider.generate_config(full_context, language=i18n.get_language())
        
        return config
    
    def _show_preview(self, config: ProjectConfig, path: Path) -> None:
        """Mostra preview em modo dry-run"""
        self.console.print(f"\n[bold yellow]🔍 {i18n.t('init.dry_run_title')}[/bold yellow]\n")
        
        self.console.print(f"[dim]{i18n.t('init.dry_run_directory')}:[/dim] {path}")
        self.console.print(f"[dim]{i18n.t('init.dry_run_project')}:[/dim] {config.display_name}")
        self.console.print(f"[dim]{i18n.t('init.dry_run_stack')}:[/dim] {config.stack}\n")
        
        self.console.print(f"[dim]{i18n.t('init.dry_run_files')}:[/dim]")
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
        
        self.console.print(f"\n[dim]{i18n.t('init.dry_run_run_without')}.[/dim]\n")
    
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
            self.console.print(f"[yellow]{i18n.t('init.only_missing_warning')}[/yellow]")
            self.console.print(f"[dim]{i18n.t('init.dry_run_files')}...[/dim]\n")
        
        # Gera arquivos
        generated = generator.generate_all(config, path, progress=True)
        
        # Mostra resultado
        self.console.print(f"\n[bold green]{i18n.t('init.success')}[/bold green]\n")
        self.console.print(f"[dim]{i18n.t('init.files_generated')}:[/dim] [cyan]{path}[/cyan]\n")
        
        self.console.print(f"[dim]{i18n.t('init.next_steps')}:[/dim]")
        self.console.print(f"  [bright_cyan]1.[/bright_cyan] {i18n.t('init.next_step_1', path=path)}")
        self.console.print(f"  [bright_cyan]2.[/bright_cyan] {i18n.t('init.next_step_2', path=path)}")
        self.console.print(f"  [bright_cyan]3.[/bright_cyan] {i18n.t('init.next_step_3', path=path)}")
        self.console.print()
