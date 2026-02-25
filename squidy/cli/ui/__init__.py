"""
UI module - Componentes visuais da CLI
"""

from squidy.cli.ui.theme import SquidyTheme
from squidy.cli.ui.language_selector import select_language, detect_system_language, show_language_banner

__all__ = ["SquidyTheme", "select_language", "detect_system_language", "show_language_banner"]
