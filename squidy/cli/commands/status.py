"""
Status Command - Comando de status rápido
"""

from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from squidy.core.i18n import i18n
from squidy.core.ports.filesystem import FileSystemPort


class StatusCommand:
    """Comando de status rápido do projeto"""
    
    def __init__(self, fs: FileSystemPort, console: Console):
        self.fs = fs
        self.console = console
    
    def execute(self, path: Path) -> None:
        """Executa comando status"""
        
        self.console.print(f"\n[bold cyan]📊 {i18n.t('status.title')}[/bold cyan]\n")
        
        # Verifica estrutura
        checks = self._check_structure(path)
        
        # Mostra resultado
        self._show_status(path, checks)
    
    def _check_structure(self, path: Path) -> dict:
        """Verifica estrutura do projeto"""
        checks = {
            "readme": self.fs.exists(path / "readme-agent.md"),
            "doc_dir": self.fs.exists(path / "doc"),
            "diario_dir": self.fs.exists(path / "diario"),
            "constituicao": self.fs.exists(path / "doc" / "constituicao.md"),
            "kanban": self.fs.exists(path / "doc" / "kanban.md"),
            "oraculo": self.fs.exists(path / "doc" / "oraculo.md"),
            "agent": self.fs.exists(path / "doc" / "AGENT.md"),
        }
        return checks
    
    def _show_status(self, path: Path, checks: dict) -> None:
        """Mostra status formatado"""
        
        # Painel principal
        content = Text()
        
        # Status geral
        total = len(checks)
        ok = sum(checks.values())
        
        if ok == total:
            status = f"[bold green]{i18n.t('status.structure_ok')}[/bold green]"
        elif ok >= total * 0.7:
            status = f"[bold yellow]⚠️  {i18n.t('status.structure_ok')}[/bold yellow]"
        else:
            status = f"[bold red]❌ {i18n.t('status.structure_ok')}[/bold red]"
        
        content.append(f"{status}\n\n")
        content.append(f"[dim]{i18n.t('status.path')}:[/dim] [cyan]{path}[/cyan]\n")
        content.append(f"[dim]{i18n.t('status.files_ok')}:[/dim] {ok}/{total}\n")
        
        panel = Panel(
            content,
            title="🦑 Squidy Project",
            border_style="cyan",
            box=box.ROUNDED,
        )
        
        self.console.print(panel)
        
        # Tabela de arquivos
        table = Table(box=box.ROUNDED)
        table.add_column(i18n.t('status.file'), style="cyan")
        table.add_column(i18n.t('status.status'))
        
        files = [
            ("readme-agent.md", checks["readme"]),
            ("doc/", checks["doc_dir"]),
            ("doc/constituicao.md", checks["constituicao"]),
            ("doc/kanban.md", checks["kanban"]),
            ("doc/oraculo.md", checks["oraculo"]),
            ("doc/AGENT.md", checks["agent"]),
            ("diario/", checks["diario_dir"]),
        ]
        
        for file, exists in files:
            status = f"[green]{i18n.t('status.status_ok')}[/green]" if exists else f"[red]{i18n.t('status.status_missing')}[/red]"
            table.add_row(file, status)
        
        self.console.print()
        self.console.print(table)
        
        # Dicas
        if ok < total:
            self.console.print(f"\n[dim]💡 {i18n.t('init.dry_run_run_without')}.[/dim]")
        
        self.console.print()
