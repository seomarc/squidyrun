"""
Status Command - Comando de status rápido
"""

from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from squidy.core.ports.filesystem import FileSystemPort


class StatusCommand:
    """Comando de status rápido do projeto"""
    
    def __init__(self, fs: FileSystemPort, console: Console):
        self.fs = fs
        self.console = console
    
    def execute(self, path: Path) -> None:
        """Executa comando status"""
        
        self.console.print(f"\n[bold cyan]📊 Status do Projeto[/bold cyan]\n")
        
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
            status = "[bold green]✅ Estrutura completa[/bold green]"
        elif ok >= total * 0.7:
            status = "[bold yellow]⚠️  Estrutura parcial[/bold yellow]"
        else:
            status = "[bold red]❌ Estrutura incompleta[/bold red]"
        
        content.append(f"{status}\n\n")
        content.append(f"[dim]Caminho:[/dim] [cyan]{path}[/cyan]\n")
        content.append(f"[dim]Arquivos OK:[/dim] {ok}/{total}\n")
        
        panel = Panel(
            content,
            title="🦑 Squidy Project",
            border_style="cyan",
            box=box.ROUNDED,
        )
        
        self.console.print(panel)
        
        # Tabela de arquivos
        table = Table(box=box.ROUNDED)
        table.add_column("Arquivo", style="cyan")
        table.add_column("Status")
        
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
            status = "[green]✓[/green]" if exists else "[red]✗[/red]"
            table.add_row(file, status)
        
        self.console.print()
        self.console.print(table)
        
        # Dicas
        if ok < total:
            self.console.print("\n[dim]💡 Execute 'squidy init --only-missing' para criar arquivos faltantes[/dim]")
        
        self.console.print()
