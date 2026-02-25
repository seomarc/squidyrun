"""
File Generator

Gera todos os arquivos de documentação do Squidy.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from squidy.core.domain.config import ProjectConfig
from squidy.core.i18n import i18n
from squidy.core.ports.filesystem import FileSystemPort
from squidy.generation.template_engine import TemplateEngine

console = Console()


class FileGenerator:
    """
    Gerador de arquivos Squidy
    
    Gera todos os 10 arquivos de documentação a partir
    da configuração do projeto.
    
    Example:
        >>> config = ProjectConfig(...)
        >>> generator = FileGenerator(fs)
        >>> generator.generate_all(config, Path("./meu-projeto"))
    """
    
    # Arquivos a serem gerados
    FILES = [
        ("readme-agent.md", "readme-agent.md", True),      # (template, output, root)
        ("AGENT.md", "AGENT.md", False),
        ("constituicao.md", "constituicao.md", False),
        ("oraculo.md", "oraculo.md", False),
        ("politicas.md", "politicas.md", False),
        ("kanban.md", "kanban.md", False),
        ("emergencia.md", "emergencia.md", False),
        ("indice-diario.md", "indice-diario.md", False),
        ("contexto-sessao.md", "contexto-sessao.md", False),
    ]
    
    def __init__(self, fs: FileSystemPort):
        """
        Inicializa gerador
        
        Args:
            fs: Adaptador de filesystem
        """
        self.fs = fs
        self.template_engine = TemplateEngine()
    
    def generate_all(
        self,
        config: ProjectConfig,
        output_dir: Path,
        progress: bool = True,
    ) -> list[str]:
        """
        Gera todos os arquivos
        
        Args:
            config: Configuração do projeto
            output_dir: Diretório de saída
            progress: Mostrar barra de progresso
            
        Returns:
            Lista de arquivos gerados
        """
        generated = []
        
        # Cria diretórios
        self._create_directories(output_dir)
        
        # Prepara contexto para templates
        context = self._prepare_context(config)
        
        if progress:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress_bar:
                task = progress_bar.add_task(
                    "[bright_cyan]🦑 Gerando arquivos Squidy...",
                    total=len(self.FILES) + 2,  # +1 para diário, +1 para manifest
                )
                
                for template_name, output_name, is_root in self.FILES:
                    self._generate_file(
                        output_dir,
                        template_name,
                        output_name,
                        is_root,
                        context,
                    )
                    generated.append(output_name if is_root else f"doc/{output_name}")
                    progress_bar.advance(task)
                
                # Gera arquivo de diário
                self._generate_diary(output_dir, context)
                generated.append(f"diario/{context['month']}.md")
                progress_bar.advance(task)
                
                # Gera manifest
                self._generate_manifest(output_dir, config)
                generated.append(".squidy/manifest.json")
                progress_bar.advance(task)
        else:
            for template_name, output_name, is_root in self.FILES:
                self._generate_file(
                    output_dir,
                    template_name,
                    output_name,
                    is_root,
                    context,
                )
                generated.append(output_name if is_root else f"doc/{output_name}")
            
            # Gera arquivo de diário
            self._generate_diary(output_dir, context)
            generated.append(f"diario/{context['month']}.md")
            
            # Gera manifest
            self._generate_manifest(output_dir, config)
            generated.append(".squidy/manifest.json")
        
        return generated
    
    def generate_single(
        self,
        config: ProjectConfig,
        output_dir: Path,
        template_name: str,
    ) -> str:
        """
        Gera um único arquivo
        
        Args:
            config: Configuração do projeto
            output_dir: Diretório de saída
            template_name: Nome do template
            
        Returns:
            Caminho do arquivo gerado
        """
        context = self._prepare_context(config)
        
        # Encontra o template na lista
        for tmpl, output, is_root in self.FILES:
            if tmpl == template_name:
                self._generate_file(
                    output_dir,
                    tmpl,
                    output,
                    is_root,
                    context,
                )
                return output if is_root else f"doc/{output}"
        
        raise ValueError(f"Template não encontrado: {template_name}")
    
    def _create_directories(self, output_dir: Path) -> None:
        """Cria estrutura de diretórios"""
        self.fs.mkdir(output_dir, parents=True, exist_ok=True)
        self.fs.mkdir(output_dir / ".squidy", parents=True, exist_ok=True)
        self.fs.mkdir(output_dir / "doc", parents=True, exist_ok=True)
        self.fs.mkdir(output_dir / "diario", parents=True, exist_ok=True)
    
    def _prepare_context(self, config: ProjectConfig) -> dict[str, Any]:
        """Prepara contexto para templates"""
        now = datetime.now()
        
        context = {
            **config.to_dict(),
            "now": now,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "month": now.strftime("%Y-%m"),
        }
        
        return context
    
    def _generate_file(
        self,
        output_dir: Path,
        template_name: str,
        output_name: str,
        is_root: bool,
        context: dict[str, Any],
    ) -> None:
        """Gera um arquivo individual"""
        # Renderiza template com idioma atual
        language = i18n.get_language()
        content = self.template_engine.render(template_name, language=language, **context)
        
        # Determina caminho de saída
        if is_root:
            output_path = output_dir / output_name
        else:
            output_path = output_dir / "doc" / output_name
        
        # Escreve arquivo
        self.fs.write_text(output_path, content)
    
    def _generate_diary(self, output_dir: Path, context: dict[str, Any]) -> None:
        """Gera arquivo de diário mensal"""
        language = i18n.get_language()
        content = self.template_engine.render("diario.md", language=language, **context)
        output_path = output_dir / "diario" / f"{context['month']}.md"
        self.fs.write_text(output_path, content)
    
    def _generate_manifest(
        self,
        output_dir: Path,
        config: ProjectConfig,
    ) -> None:
        """
        Gera arquivo manifest.json
        
        Args:
            output_dir: Diretório de saída
            config: Configuração do projeto
        """
        manifest = {
            "name": config.project_name,
            "display_name": config.display_name,
            "version": config.version,
            "language": i18n.get_language(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "squidy_version": "2.1.0",
            "agent_type": config.agent_type,
            "stack": {
                "frontend": config.stack.frontend if config.stack else None,
                "backend": config.stack.backend if config.stack else None,
                "database": config.stack.banco if config.stack else None,
            },
        }
        
        output_path = output_dir / ".squidy" / "manifest.json"
        self.fs.write_text(output_path, json.dumps(manifest, indent=2, ensure_ascii=False))
