"""
🌍 Sistema de Internacionalização (i18n) do Squidy

Módulo responsável por gerenciar traduções e localização
de strings, templates e mensagens da CLI.

Suporta múltiplos idiomas com fallback automático para pt-BR.

Example:
    >>> from squidy.core.i18n import i18n
    >>> i18n.set_language("en-US")
    >>> print(i18n.t("welcome.message"))
    "Welcome to Squidy!"
"""

import os
from pathlib import Path
from typing import Any

import yaml


class I18nManager:
    """
    Gerenciador de internacionalização do Squidy.
    
    Responsável por carregar traduções, fornecer strings
    localizadas e gerenciar o idioma atual.
    
    Attributes:
        current_lang: Idioma atual (ex: "pt-BR", "en-US")
        default_lang: Idioma padrão de fallback
        translations: Cache de traduções carregadas
        _instance: Singleton instance
    """
    
    _instance: "I18nManager | None" = None
    
    # Idiomas suportados
    SUPPORTED_LANGUAGES = {
        "pt-BR": "Português (Brasil)",
        "en-US": "English (US)",
    }
    
    # Idioma padrão para fallback
    DEFAULT_LANGUAGE = "pt-BR"
    
    def __new__(cls) -> "I18nManager":
        """Singleton pattern para garantir instância única"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa o gerenciador de i18n (apenas uma vez)"""
        if self._initialized:
            return
        
        self.current_lang: str = self.DEFAULT_LANGUAGE
        self.default_lang: str = self.DEFAULT_LANGUAGE
        self.translations: dict[str, dict] = {}
        self._locales_dir: Path | None = None
        
        self._initialized = True
    
    def set_language(self, lang_code: str) -> bool:
        """
        Define o idioma atual.
        
        Args:
            lang_code: Código do idioma (ex: "en-US", "pt-BR")
            
        Returns:
            True se idioma foi definido, False se não suportado
            
        Example:
            >>> i18n.set_language("en-US")
            True
            >>> i18n.set_language("fr-FR")
            False
        """
        if lang_code not in self.SUPPORTED_LANGUAGES:
            return False
        
        self.current_lang = lang_code
        # Pré-carrega traduções
        self._load_translations(lang_code)
        return True
    
    def get_language(self) -> str:
        """Retorna o idioma atual"""
        return self.current_lang
    
    def get_language_name(self, lang_code: str | None = None) -> str:
        """
        Retorna o nome legível do idioma.
        
        Args:
            lang_code: Código do idioma (default: idioma atual)
        """
        code = lang_code or self.current_lang
        return self.SUPPORTED_LANGUAGES.get(code, code)
    
    def t(self, key: str, **kwargs) -> str:
        """
        Traduz uma chave para o idioma atual.
        
        Implementa fallback para o idioma padrão se a chave
        não for encontrada no idioma atual.
        
        Args:
            key: Chave de tradução (ex: "welcome.message")
            **kwargs: Placeholders para substituição
            
        Returns:
            String traduzida ou a própria chave se não encontrada
            
        Example:
            >>> i18n.t("welcome.message", name="Squidy")
            "Welcome, Squidy!"
        """
        # Tenta no idioma atual
        translation = self._get_translation(self.current_lang, key)
        
        # Fallback para idioma padrão
        if translation is None and self.current_lang != self.default_lang:
            translation = self._get_translation(self.default_lang, key)
        
        # Se não encontrou, retorna a chave
        if translation is None:
            return key
        
        # Substitui placeholders
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except KeyError:
                # Placeholder não fornecido, mantém como está
                pass
        
        return translation
    
    def _get_translation(self, lang_code: str, key: str) -> str | None:
        """
        Busca tradução em um idioma específico.
        
        Args:
            lang_code: Código do idioma
            key: Chave de tradução (pode ser aninhada com ".")
            
        Returns:
            String traduzida ou None se não encontrada
        """
        translations = self._load_translations(lang_code)
        
        # Navega no dicionário aninhado
        keys = key.split(".")
        value = translations
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        
        return str(value) if not isinstance(value, dict) else None
    
    def _load_translations(self, lang_code: str) -> dict:
        """
        Carrega traduções de um idioma.
        
        Usa cache para evitar leituras repetidas.
        
        Args:
            lang_code: Código do idioma
            
        Returns:
            Dicionário de traduções
        """
        if lang_code in self.translations:
            return self.translations[lang_code]
        
        translations = {}
        locales_dir = self._get_locales_dir()
        lang_dir = locales_dir / lang_code
        
        # Carrega todos os arquivos YAML do idioma
        if lang_dir.exists():
            for yaml_file in sorted(lang_dir.glob("*.yaml")):
                try:
                    with open(yaml_file, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict):
                            # Merge direto no dicionário raiz (sem namespace por arquivo)
                            translations.update(data)
                except Exception:
                    # Ignora arquivos com erro
                    pass
        
        self.translations[lang_code] = translations
        return translations
    
    def _get_locales_dir(self) -> Path:
        """Retorna o diretório de locales"""
        if self._locales_dir is None:
            # Diretório padrão: squidy/locales/
            module_dir = Path(__file__).parent.parent
            self._locales_dir = module_dir / "locales"
        return self._locales_dir
    
    def set_locales_dir(self, path: Path) -> None:
        """Define diretório customizado de locales (útil para testes)"""
        self._locales_dir = path
        self.translations.clear()  # Limpa cache
    
    def get_supported_languages(self) -> dict[str, str]:
        """Retorna dicionário de idiomas suportados"""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def clear_cache(self) -> None:
        """Limpa cache de traduções"""
        self.translations.clear()


# Instância global (singleton)
i18n = I18nManager()


# Função de conveniência para traduzir
def t(key: str, **kwargs) -> str:
    """
    Função shorthand para traduzir strings.
    
    Example:
        >>> from squidy.core.i18n import t
        >>> t("welcome.message")
        "Bem-vindo!"
    """
    return i18n.t(key, **kwargs)
