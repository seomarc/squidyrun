"""
Audit Command - Comando de auditoria de projeto
"""

import json
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from squidy.adapters.filesystem.local_fs import LocalFileSystem
from squidy.audit.checkers.consistency_checker import ConsistencyChecker
from squidy.audit.checkers.freshness_checker import FreshnessChecker
from squidy.audit.checkers.kanban_checker import KanbanChecker
from squidy.audit.checkers.structure_checker import StructureChecker
from squidy.audit.detectors.heuristic_detector import HeuristicDetector
from squidy.audit.detectors.manifest_detector import ManifestDetector
from squidy.audit.engine import AuditEngine
from squidy.core.domain.audit_result import Severity
from squidy.core.ports.filesystem import FileSystemPort


class AuditCommand:
    """Comando de auditoria de projeto Squidy"""
    
    def __init__(self, fs: FileSystemPort, console: Console):
        self.fs = fs
        self.console = console
    
    def execute(
        self,
        path: Path,
        fix: bool = False,
        output_format: str = "console",
        checkers: list[str] | None = None,
    ) -> None:
        """Executa comando audit"""
        
        # Verifica se é projeto Squidy
        is_squidy, confidence = self._detect_project(path)
        
        if not is_squidy:
            self.console.print(f"\n[yellow]⚠️  Não parece ser um projeto Squidy: {path}[/yellow]")
            self.console.print("[dim]Execute 'squidy init' primeiro.[/dim]\n")
            return
        
        # Configura engine de auditoria
        engine = AuditEngine(self.fs)
        
        # Registra checkers
        engine.register_checker(StructureChecker)
        engine.register_checker(KanbanChecker)
        engine.register_checker(FreshnessChecker)
        engine.register_checker(ConsistencyChecker)
        
        # Executa auditoria
        self.console.print(f"\n[bold cyan]🔍 Auditando:[/bold cyan] {path}\n")
        
        result = engine.audit(
            path=path,
            checkers=checkers,
        )
        
        # Mostra resultados
        if output_format == "json":
            self._output_json(result)
        elif output_format == "markdown":
            self._output_markdown(result)
        else:
            self._output_console(result, fix)
    
    def _detect_project(self, path: Path) -> tuple[bool, float]:
        """Detecta se é projeto Squidy"""
        detector = ManifestDetector(self.fs)
        if detector.detect(path):
            return True, 1.0
        
        detector = HeuristicDetector(self.fs)
        if detector.detect(path):
            return True, detector.get_confidence(path)
        
        return False, 0.0
    
    def _output_console(self, result, fix: bool) -> None:
        """Saída em formato console (rich)"""
        
        # Resumo
        summary = result.summary
        
        self.console.print("[bold]Resumo da Auditoria:[/bold]\n")
        
        # Tabela de severidade
        table = Table(box=box.ROUNDED)
        table.add_column("Severidade", style="bold")
        table.add_column("Quantidade", justify="right")
        
        severities = [
            ("🔴 Crítico", summary["critical"], "red"),
            ("🟠 Alto", summary["high"], "orange3"),
            ("🟡 Médio", summary["medium"], "yellow"),
            ("🟢 Baixo", summary["low"], "green"),
            ("🔵 Info", summary["info"], "blue"),
        ]
        
        for label, count, color in severities:
            if count > 0:
                table.add_row(f"[{color}]{label}[/{color}]", str(count))
        
        table.add_row("[bold]Total[/bold]", str(summary["total"]), style="bold")
        
        self.console.print(table)
        self.console.print()
        
        # Lista de findings
        if result.findings:
            self.console.print("[bold]Problemas Encontrados:[/bold]\n")
            
            for finding in result.findings:
                self._print_finding(finding)
            
            # Auto-fix
            if fix and result.auto_fixable_count > 0:
                self.console.print(f"\n[yellow]⚠️  {result.auto_fixable_count} problema(s) podem ser corrigidos automaticamente[/yellow]")
                self.console.print("[dim]Execute 'squidy audit --fix' para aplicar correções.[/dim]")
        else:
            self.console.print("[bold green]✅ Nenhum problema encontrado![/bold green]\n")
        
        # Checkers executados
        self.console.print(f"[dim]Checkers executados: {', '.join(result.checkers_run)}[/dim]")
        self.console.print(f"[dim]Duração: {result.duration_ms}ms[/dim]\n")
    
    def _print_finding(self, finding) -> None:
        """Printa um finding formatado"""
        emoji = {
            Severity.CRITICAL: "🔴",
            Severity.HIGH: "🟠",
            Severity.MEDIUM: "🟡",
            Severity.LOW: "🟢",
            Severity.INFO: "🔵",
        }.get(finding.severity, "⚪")
        
        # Painel para cada finding
        content = Text()
        content.append(f"{finding.message}\n\n", style="white")
        
        if finding.file:
            content.append(f"Arquivo: ", style="dim")
            content.append(f"{finding.file}\n", style="cyan")
        
        if finding.suggestion:
            content.append(f"Sugestão: ", style="dim")
            content.append(finding.suggestion, style="green")
        
        if finding.auto_fixable:
            content.append(f"\n[auto-fixable]", style="yellow")
        
        panel = Panel(
            content,
            title=f"{emoji} {finding.checker}",
            border_style=self._severity_color(finding.severity),
            box=box.ROUNDED,
        )
        
        self.console.print(panel)
    
    def _severity_color(self, severity: Severity) -> str:
        """Retorna cor para severidade"""
        colors = {
            Severity.CRITICAL: "red",
            Severity.HIGH: "orange3",
            Severity.MEDIUM: "yellow",
            Severity.LOW: "green",
            Severity.INFO: "blue",
        }
        return colors.get(severity, "white")
    
    def _output_json(self, result) -> None:
        """Saída em formato JSON"""
        output = result.to_dict()
        self.console.print(json.dumps(output, indent=2, ensure_ascii=False))
    
    def _output_markdown(self, result) -> None:
        """Saída em formato Markdown"""
        lines = [
            "# Relatório de Auditoria Squidy",
            "",
            f"**Projeto:** {result.project_path}",
            f"**Data:** {result.timestamp.isoformat()}",
            f"**Duração:** {result.duration_ms}ms",
            "",
            "## Resumo",
            "",
            f"- 🔴 Crítico: {result.summary['critical']}",
            f"- 🟠 Alto: {result.summary['high']}",
            f"- 🟡 Médio: {result.summary['medium']}",
            f"- 🟢 Baixo: {result.summary['low']}",
            f"- 🔵 Info: {result.summary['info']}",
            f"- **Total: {result.summary['total']}**",
            "",
        ]
        
        if result.findings:
            lines.extend(["## Problemas Encontrados", ""])
            
            for finding in result.findings:
                emoji = {
                    Severity.CRITICAL: "🔴",
                    Severity.HIGH: "🟠",
                    Severity.MEDIUM: "🟡",
                    Severity.LOW: "🟢",
                    Severity.INFO: "🔵",
                }.get(finding.severity, "⚪")
                
                lines.append(f"### {emoji} {finding.message}")
                if finding.file:
                    lines.append(f"**Arquivo:** `{finding.file}`")
                if finding.suggestion:
                    lines.append(f"**Sugestão:** {finding.suggestion}")
                lines.append("")
        
        lines.extend([
            "## Checkers Executados",
            "",
            f"{', '.join(result.checkers_run)}",
        ])
        
        self.console.print("\n".join(lines))
