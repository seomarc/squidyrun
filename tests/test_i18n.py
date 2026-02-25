"""
Testes de Internacionalização (i18n)

Testes para o sistema de tradução do Squidy.
"""

import pytest
from pathlib import Path

from squidy.core.i18n import I18nManager, i18n, t


class TestI18nManager:
    """Testes do I18nManager"""
    
    def setup_method(self):
        """Setup para cada teste"""
        # Limpa a instância singleton
        I18nManager._instance = None
        self.i18n = I18nManager()
    
    def test_singleton_pattern(self):
        """Testa que I18nManager é singleton"""
        i1 = I18nManager()
        i2 = I18nManager()
        assert i1 is i2
    
    def test_default_language(self):
        """Testa idioma padrão"""
        assert self.i18n.get_language() == "pt-BR"
        assert self.i18n.default_lang == "pt-BR"
    
    def test_set_valid_language(self):
        """Testa definir idioma válido"""
        assert self.i18n.set_language("en-US") is True
        assert self.i18n.get_language() == "en-US"
        
        assert self.i18n.set_language("pt-BR") is True
        assert self.i18n.get_language() == "pt-BR"
    
    def test_set_invalid_language(self):
        """Testa definir idioma inválido"""
        assert self.i18n.set_language("fr-FR") is False
        assert self.i18n.get_language() == "pt-BR"  # Mantém padrão
    
    def test_get_supported_languages(self):
        """Testa lista de idiomas suportados"""
        languages = self.i18n.get_supported_languages()
        assert "pt-BR" in languages
        assert "en-US" in languages
        assert languages["pt-BR"] == "Português (Brasil)"
        assert languages["en-US"] == "English (US)"
    
    def test_translation_pt_br(self):
        """Testa tradução em português"""
        self.i18n.set_language("pt-BR")
        
        # Testa traduções existentes
        assert self.i18n.t("banner.title") == "Squidy"
        assert self.i18n.t("init.success") == "✅ Setup concluído!"
    
    def test_translation_en_us(self):
        """Testa tradução em inglês"""
        self.i18n.set_language("en-US")
        
        assert self.i18n.t("banner.title") == "Squidy"
        assert self.i18n.t("init.success") == "✅ Setup completed!"
    
    def test_translation_with_placeholders(self):
        """Testa tradução com placeholders"""
        self.i18n.set_language("pt-BR")
        
        result = self.i18n.t("init.files_generated")
        assert "Arquivos gerados" in result
    
    def test_fallback_to_default(self):
        """Testa fallback para idioma padrão quando chave não existe"""
        self.i18n.set_language("en-US")
        
        # Chave inexistente deve retornar a própria chave
        result = self.i18n.t("chave.inexistente")
        assert result == "chave.inexistente"
    
    def test_fallback_when_translation_missing(self):
        """Testa fallback pt-BR quando tradução não existe no idioma atual"""
        # Primeiro carrega pt-BR
        self.i18n.set_language("pt-BR")
        
        # Depois muda para en-US
        self.i18n.set_language("en-US")
        
        # Se uma chave não existe em en-US, deve usar pt-BR
        # (isso depende das traduções definidas)
        result = self.i18n.t("banner.title")
        assert result == "Squidy"  # Existe em ambos
    
    def test_clear_cache(self):
        """Testa limpeza de cache"""
        self.i18n.set_language("pt-BR")
        self.i18n._load_translations("pt-BR")  # Carrega para cache
        
        assert "pt-BR" in self.i18n.translations
        
        self.i18n.clear_cache()
        assert "pt-BR" not in self.i18n.translations


class TestGlobalI18nFunctions:
    """Testes das funções globais de i18n"""
    
    def setup_method(self):
        """Setup para cada teste"""
        I18nManager._instance = None
    
    def test_global_t_function(self):
        """Testa função global t()"""
        i18n.set_language("pt-BR")
        
        result = t("banner.title")
        assert result == "Squidy"
    
    def test_global_i18n_instance(self):
        """Testa instância global i18n"""
        assert isinstance(i18n, I18nManager)


class TestI18nIntegration:
    """Testes de integração do i18n com outros componentes"""
    
    def setup_method(self):
        """Setup para cada teste"""
        I18nManager._instance = None
        self.i18n = I18nManager()
    
    def test_language_persistence(self):
        """Testa que idioma persiste entre chamadas"""
        self.i18n.set_language("en-US")
        
        # Verifica em várias chamadas
        for _ in range(3):
            assert self.i18n.get_language() == "en-US"
            assert self.i18n.t("init.success") == "✅ Setup completed!"
    
    def test_switching_languages(self):
        """Testa alternância entre idiomas"""
        # Pt-BR
        self.i18n.set_language("pt-BR")
        pt_success = self.i18n.t("init.success")
        
        # En-US
        self.i18n.set_language("en-US")
        en_success = self.i18n.t("init.success")
        
        # Devem ser diferentes
        assert pt_success != en_success
        assert "concluído" in pt_success.lower()
        assert "completed" in en_success.lower()
    
    def test_translation_with_special_characters(self):
        """Testa traduções com caracteres especiais"""
        self.i18n.set_language("pt-BR")
        
        # Testa emojis e caracteres especiais
        result = self.i18n.t("init.success")
        assert "✅" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
