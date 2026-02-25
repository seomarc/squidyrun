"""
Language Selector UI

Interface para seleção de idioma durante a inicialização.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

from squidy.core.i18n import i18n

console = Console()


def select_language(console: Console, interactive: bool = True) -> str:
    """
    Interface de seleção de idioma.
    
    Args:
        console: Console Rich para output
        interactive: Se True, mostra prompt interativo
        
    Returns:
        Código do idioma selecionado (ex: "pt-BR", "en-US")
    """
    languages = i18n.get_supported_languages()
    
    # Título
    title = Text()
    title.append("🌍 ", style="bold")
    title.append("Selecione o idioma / Select language", style="bold cyan")
    
    console.print()
    console.print(title)
    console.print()
    
    # Mostra opções
    lang_list = list(languages.items())
    for idx, (code, name) in enumerate(lang_list, 1):
        flag = "🇧🇷" if code == "pt-BR" else "🇺🇸" if code == "en-US" else "🌐"
        console.print(f"  [{idx}] {flag} {name}")
    
    console.print()
    
    if not interactive:
        # Retorna padrão se não interativo
        return i18n.DEFAULT_LANGUAGE
    
    # Prompt
    while True:
        try:
            choice = console.input("  > ")
            
            # Valida entrada
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(lang_list):
                    selected_code = lang_list[idx][0]
                    selected_name = lang_list[idx][1]
                    
                    # Configura idioma
                    i18n.set_language(selected_code)
                    
                    # Confirmação
                    console.print(f"\n  ✓ {i18n.t('language.selected')}: [bold]{selected_name}[/bold]\n")
                    
                    return selected_code
            
            # Tentativa de código direto
            if choice in languages:
                i18n.set_language(choice)
                console.print(f"\n  ✓ {i18n.t('language.selected')}: [bold]{languages[choice]}[/bold]\n")
                return choice
            
            console.print(f"  [red]{i18n.t('language.invalid')}[/red]\n")
            
        except KeyboardInterrupt:
            console.print()
            return i18n.DEFAULT_LANGUAGE
        except Exception:
            console.print(f"  [red]{i18n.t('language.invalid')}[/red]\n")


def detect_system_language() -> str:
    """
    Detecta idioma do sistema operacional.
    
    Returns:
        Código do idioma detectado ou idioma padrão
    """
    import locale
    
    try:
        system_locale = locale.getdefaultlocale()[0]
        
        if system_locale:
            # Mapeia locales comuns
            locale_map = {
                "pt_BR": "pt-BR",
                " Portuguese_Brazil": "pt-BR",
                "en_US": "en-US",
                "en_GB": "en-US",
                "English_United States": "en-US",
            }
            
            for key, value in locale_map.items():
                if key in system_locale:
                    return value
    except Exception:
        pass
    
    return i18n.DEFAULT_LANGUAGE


def show_language_banner(console: Console, lang_code: str) -> None:
    """
    Mostra banner com idioma atual.
    
    Args:
        console: Console Rich
        lang_code: Código do idioma
    """
    lang_name = i18n.get_language_name(lang_code)
    
    content = Text()
    content.append(f"🌍 {i18n.t('language.current')}: ", style="dim")
    content.append(lang_name, style="cyan")
    
    panel = Panel(
        content,
        border_style="dim cyan",
        box=box.ROUNDED,
        padding=(0, 2),
    )
    
    console.print(panel)
