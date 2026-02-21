"""
Squidy Theme - Paleta de cores e estilos visuais

Define a identidade visual do Squidy CLI.
"""

from rich.text import Text
from rich.style import Style


class SquidyTheme:
    """
    Tema visual do Squidy
    
    Paleta "Oceano Digital" - cores modernas e profissionais.
    """
    
    # Cores principais
    OCEAN = "#00D4AA"
    CORAL = "#FF6B9D"
    DEEP = "#0A1628"
    AQUA = "#00F5FF"
    ELECTRIC = "#7B61FF"
    MYSTIC = "#C084FC"
    
    # Cores semânticas
    SUCCESS = "#00E676"
    WARNING = "#FFC107"
    ERROR = "#FF5252"
    INFO = "#2196F3"
    
    # Cores neutras
    WHITE = "#FFFFFF"
    GRAY_100 = "#F5F5F5"
    GRAY_300 = "#E0E0E0"
    GRAY_500 = "#9E9E9E"
    GRAY_700 = "#616161"
    GRAY_900 = "#212121"
    
    @classmethod
    def gradient_text(cls, text: str, start_color: str, end_color: str) -> Text:
        """
        Cria texto com gradiente de cores
        
        Args:
            text: Texto
            start_color: Cor inicial (hex)
            end_color: Cor final (hex)
            
        Returns:
            Text com gradiente
        """
        # Simplificação: retorna texto colorido com cor intermediária
        result = Text(text)
        
        # Calcula cor intermediária
        if start_color == "cyan" and end_color == "aqua":
            result.stylize("bold bright_cyan")
        elif start_color == "purple" and end_color == "pink":
            result.stylize("bold magenta")
        else:
            result.stylize(f"bold {start_color}")
        
        return result
    
    @classmethod
    def get_style(cls, name: str) -> Style:
        """Retorna estilo por nome"""
        styles = {
            "title": Style(color=cls.OCEAN, bold=True),
            "subtitle": Style(color=cls.GRAY_500),
            "success": Style(color=cls.SUCCESS, bold=True),
            "warning": Style(color=cls.WARNING, bold=True),
            "error": Style(color=cls.ERROR, bold=True),
            "info": Style(color=cls.INFO),
            "dim": Style(color=cls.GRAY_500),
            "highlight": Style(color=cls.AQUA, bold=True),
        }
        return styles.get(name, Style())
    
    @classmethod
    def severity_color(cls, severity: str) -> str:
        """Retorna cor para severidade"""
        colors = {
            "critical": cls.ERROR,
            "high": "#FF9800",
            "medium": cls.WARNING,
            "low": cls.SUCCESS,
            "info": cls.INFO,
        }
        return colors.get(severity, cls.GRAY_500)
