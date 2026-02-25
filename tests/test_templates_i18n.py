"""
Testes de Templates com Internacionalização

Testes para verificar renderização de templates em múltiplos idiomas.
"""

import pytest
from pathlib import Path

from squidy.generation.template_engine import TemplateEngine
from squidy.core.i18n import I18nManager


class TestTemplateEngineI18n:
    """Testes da TemplateEngine com suporte a i18n"""
    
    def setup_method(self):
        """Setup para cada teste"""
        I18nManager._instance = None
        self.engine = TemplateEngine()
        self.sample_config = {
            "display_name": "Test Project",
            "proposito": "Test purpose",
            "agent_type": "fullstack-developer",
            "stack": {
                "frontend": "React",
                "backend": "Node.js",
                "banco": "PostgreSQL",
            },
            "principios": ["Clean code", "Tests"],
            "proibicoes": ["No bugs"],
            "dod": ["Tests pass"],
            "convencoes": {
                "variaveis": "camelCase",
                "funcoes": "camelCase",
                "classes": "PascalCase",
                "constantes": "UPPER_SNAKE",
                "arquivos": "kebab-case",
                "banco": "snake_case",
            },
            "version": "2.1.0",
        }
    
    def test_templates_available_both_languages(self):
        """Testa que templates existem em ambos idiomas"""
        # Verifica templates pt-BR
        assert len(self.engine._templates_pt) == 10
        
        # Verifica templates en-US
        assert len(self.engine._templates_en) == 10
        
        # Verifica que todos os templates existem em ambos
        for key in self.engine._templates_pt:
            assert key in self.engine._templates_en
    
    def test_render_readme_agent_pt_br(self):
        """Testa renderização do readme-agent em pt-BR"""
        content = self.engine.render(
            "readme-agent.md",
            language="pt-BR",
            **self.sample_config
        )
        
        # Verifica elementos em português
        assert "Ritual de Inicialização" in content
        assert "Contexto do Projeto" in content
        assert "Regras de Ouro" in content
        assert "📜 Princípios" in content
    
    def test_render_readme_agent_en_us(self):
        """Testa renderização do readme-agent em en-US"""
        content = self.engine.render(
            "readme-agent.md",
            language="en-US",
            **self.sample_config
        )
        
        # Verifica elementos em inglês
        assert "Initialization Ritual" in content
        assert "Project Context" in content
        assert "Golden Rules" in content
        assert "📜 Principles" in content
    
    def test_render_constitution_pt_br(self):
        """Testa renderização da constituição em pt-BR"""
        content = self.engine.render(
            "constituicao.md",
            language="pt-BR",
            **self.sample_config
        )
        
        assert "CONSTITUIÇÃO" in content
        assert "PRINCÍPIOS" in content
        assert "PROIBIÇÕES" in content
        assert "DEFINITION OF DONE" in content  # Mantido em inglês técnico
    
    def test_render_constitution_en_us(self):
        """Testa renderização da constituição em en-US"""
        content = self.engine.render(
            "constituicao.md",
            language="en-US",
            **self.sample_config
        )
        
        assert "CONSTITUTION" in content
        assert "PRINCIPLES" in content
        assert "PROHIBITIONS" in content
        assert "DEFINITION OF DONE" in content
    
    def test_render_kanban_pt_br(self):
        """Testa renderização do kanban em pt-BR"""
        content = self.engine.render(
            "kanban.md",
            language="pt-BR",
            **self.sample_config
        )
        
        assert "ÉPICOS" in content
        assert "BACKLOG" in content
        assert "EM PROGRESSO" in content
        assert "CONCLUÍDO" in content
    
    def test_render_kanban_en_us(self):
        """Testa renderização do kanban em en-US"""
        content = self.engine.render(
            "kanban.md",
            language="en-US",
            **self.sample_config
        )
        
        assert "EPICS" in content
        assert "BACKLOG" in content
        assert "IN PROGRESS" in content
        assert "COMPLETED" in content
    
    def test_render_oracle_pt_br(self):
        """Testa renderização do oráculo em pt-BR"""
        content = self.engine.render(
            "oraculo.md",
            language="pt-BR",
            **self.sample_config
        )
        
        assert "ORÁCULO" in content or "Decisões de Arquitetura" in content
    
    def test_render_oracle_en_us(self):
        """Testa renderização do oráculo em en-US"""
        content = self.engine.render(
            "oraculo.md",
            language="en-US",
            **self.sample_config
        )
        
        assert "ORACLE" in content or "Architecture Decisions" in content
    
    def test_fallback_to_pt_br(self):
        """Testa fallback para pt-BR quando idioma inválido"""
        content = self.engine.render(
            "readme-agent.md",
            language="invalid-lang",
            **self.sample_config
        )
        
        # Deve usar pt-BR como fallback
        assert "Ritual de Inicialização" in content
    
    def test_all_templates_render_successfully_pt(self):
        """Testa que todos os templates renderizam em pt-BR"""
        templates = [
            "readme-agent.md",
            "constituicao.md",
            "kanban.md",
            "oraculo.md",
            "politicas.md",
            "emergencia.md",
            "indice-diario.md",
            "contexto-sessao.md",
            "AGENT.md",
            "diario.md",
        ]
        
        for template in templates:
            content = self.engine.render(template, language="pt-BR", **self.sample_config)
            assert len(content) > 100  # Conteúdo não vazio
            assert "{{" not in content  # Não deve haver tags não renderizadas
    
    def test_all_templates_render_successfully_en(self):
        """Testa que todos os templates renderizam em en-US"""
        templates = [
            "readme-agent.md",
            "constituicao.md",
            "kanban.md",
            "oraculo.md",
            "politicas.md",
            "emergencia.md",
            "indice-diario.md",
            "contexto-sessao.md",
            "AGENT.md",
            "diario.md",
        ]
        
        for template in templates:
            content = self.engine.render(template, language="en-US", **self.sample_config)
            assert len(content) > 100
            assert "{{" not in content
    
    def test_template_content_different_languages(self):
        """Testa que conteúdo é diferente entre idiomas"""
        pt_content = self.engine.render(
            "readme-agent.md",
            language="pt-BR",
            **self.sample_config
        )
        
        en_content = self.engine.render(
            "readme-agent.md",
            language="en-US",
            **self.sample_config
        )
        
        # Devem ser diferentes
        assert pt_content != en_content
        
        # Verifica diferenças específicas
        assert "Ritual" in pt_content
        assert "Ritual" not in en_content
        assert "Ritual" in en_content or "Initialization" in en_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
