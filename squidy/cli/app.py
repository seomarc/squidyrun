#!/usr/bin/env python3
"""
Squidy CLI - Interface de linha de comando premium

Uma CLI moderna e imersiva para governança de projetos com Agentes de IA.
"""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

from squidy.adapters.filesystem.local_fs import LocalFileSystem
from squidy.cli.commands.init import InitCommand
from squidy.cli.commands.audit import AuditCommand
from squidy.cli.commands.status import StatusCommand
from squidy.cli.ui.theme import SquidyTheme
from squidy.cli.ui.language_selector import select_language, detect_system_language
from squidy.core.i18n import i18n

# Console principal
console = Console()

# App Typer
app = typer.Typer(
    name="squidy",
    help="🦑 Squidy - Setup inteligente para projetos com Agentes de IA",
    add_completion=False,
    no_args_is_help=True,
)

# Versão
SQUIDY_VERSION = "2.1.8"


def show_banner():
    """Mostra banner premium do Squidy"""
    from squidy.core.i18n import i18n
    
    theme = SquidyTheme()
    
    # Título com gradiente
    title = theme.gradient_text("Squidy", "cyan", "aqua")
    subtitle = Text("squidy.run", style="dim cyan")
    
    # Painel de marca
    brand_content = Text()
    brand_content.append("🦑\n", style="bold bright_cyan")
    brand_content.append(title)
    brand_content.append("\n")
    brand_content.append(subtitle)
    
    brand_panel = Panel(
        brand_content,
        border_style="bright_cyan",
        box=box.DOUBLE,
        padding=(1, 4),
    )
    
    # Painel de descrição (usando i18n)
    desc_content = Text()
    desc_content.append(i18n.t("banner.description") + "\n\n", style="bold white")
    desc_content.append("  ✦ ", style="bright_cyan")
    desc_content.append(i18n.t("banner.feature_1") + "\n", style="white")
    desc_content.append("  ✦ ", style="bright_cyan")
    desc_content.append(i18n.t("banner.feature_2") + "\n", style="white")
    desc_content.append("  ✦ ", style="bright_cyan")
    desc_content.append(i18n.t("banner.feature_3") + "\n\n", style="white")
    desc_content.append("  " + i18n.t("banner.providers"), style="dim")
    
    desc_panel = Panel(
        desc_content,
        border_style="dim",
        box=box.ROUNDED,
        padding=(1, 3),
    )
    
    # Mostra painéis lado a lado
    from rich.columns import Columns
    console.print()
    console.print(Columns([brand_panel, desc_panel], padding=(0, 2)))
    console.print()


@app.callback()
def callback():
    """Squidy - Setup inteligente para projetos com Agentes de IA"""
    pass


@app.command(name="init")
def init_command(
    path: Path = typer.Argument(
        ".",
        help="Caminho do projeto",
        exists=False,
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Simula sem criar arquivos",
    ),
    only_missing: bool = typer.Option(
        False,
        "--only-missing",
        help="Cria apenas arquivos faltantes",
    ),
    manual: bool = typer.Option(
        False,
        "--manual",
        help="Setup manual sem IA",
    ),
    provider: str = typer.Option(
        None,
        "--provider",
        help="Provedor de IA (openai, anthropic). Se omitido, pergunta interativamente.",
    ),
    lang: str = typer.Option(
        None,
        "--lang",
        help="Idioma/Language (pt-BR, en-US)",
    ),
):
    """
    Inicializa estrutura Squidy em um projeto
    
    Example:
        $ squidy init                    # Setup interativo com IA (escolhe idioma)
        $ squidy init ./meu-projeto      # Especifica caminho
        $ squidy init --dry-run          # Simula sem criar
        $ squidy init --manual           # Setup manual
        $ squidy init --lang en-US       # Idioma inglês (pula seleção)
    """
    # 🌍 SELEÇÃO DE IDIOMA (sempre primeiro, antes de tudo)
    if lang:
        # Usa idioma especificado via flag (pula seleção interativa)
        if not i18n.set_language(lang):
            console.print(f"[yellow]⚠️ Idioma '{lang}' não suportado. Usando padrão.[/yellow]\n")
            selected_lang = select_language(console, interactive=True)
            i18n.set_language(selected_lang)
    else:
        # Mostra seleção de idioma imediatamente
        selected_lang = select_language(console, interactive=True)
        i18n.set_language(selected_lang)
    
    # Agora mostra o banner no idioma selecionado
    show_banner()
    
    fs = LocalFileSystem()
    cmd = InitCommand(fs, console)
    
    cmd.execute(
        path=path,
        dry_run=dry_run,
        only_missing=only_missing,
        manual=manual,
        provider=provider,
    )


@app.command(name="audit")
def audit_command(
    path: Path = typer.Argument(
        ".",
        help="Caminho do projeto",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    fix: bool = typer.Option(
        False,
        "--fix",
        help="Aplica correções automáticas",
    ),
    format: str = typer.Option(
        "console",
        "--format",
        "-f",
        help="Formato de saída (console, json, markdown)",
    ),
    checkers: str = typer.Option(
        None,
        "--checkers",
        "-c",
        help="Checkers específicos (comma-separated)",
    ),
):
    """
    Audita projeto Squidy existente
    
    Example:
        $ squidy audit                   # Audita diretório atual
        $ squidy audit ./projeto         # Audita projeto específico
        $ squidy audit --fix             # Aplica correções
        $ squidy audit -f json           # Saída em JSON
    """
    fs = LocalFileSystem()
    cmd = AuditCommand(fs, console)
    
    checker_list = checkers.split(",") if checkers else None
    
    cmd.execute(
        path=path,
        fix=fix,
        output_format=format,
        checkers=checker_list,
    )


@app.command(name="status")
def status_command(
    path: Path = typer.Argument(
        ".",
        help="Caminho do projeto",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
):
    """
    Mostra status rápido do projeto
    
    Example:
        $ squidy status                  # Status do diretório atual
        $ squidy status ./projeto        # Status de projeto específico
    """
    fs = LocalFileSystem()
    cmd = StatusCommand(fs, console)
    cmd.execute(path=path)


@app.command(name="doctor")
def doctor_command(
    path: Path = typer.Argument(
        ".",
        help="Caminho do projeto",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
):
    """
    Diagnóstico completo do projeto
    
    Example:
        $ squidy doctor                  # Diagnóstico do diretório atual
        $ squidy doctor ./projeto        # Diagnóstico de projeto específico
    """
    console.print("\n[bold cyan]🩺 Squidy Doctor[/bold cyan]\n")
    console.print("Executando diagnóstico completo...\n")
    
    # Executa audit com todos os checkers
    fs = LocalFileSystem()
    cmd = AuditCommand(fs, console)
    cmd.execute(
        path=path,
        fix=False,
        output_format="console",
        checkers=None,
    )


def main():
    """Entry point principal"""
    from squidy.core.i18n import i18n
    
    try:
        app()
    except KeyboardInterrupt:
        console.print(f"\n\n[dim]🦑 {i18n.t('errors.keyboard_interrupt')}[/dim]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]{i18n.t('errors.generic', error=e)}[/red]\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
