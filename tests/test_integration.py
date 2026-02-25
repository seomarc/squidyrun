"""
Testes de integração do Squidy
"""

import pytest
from pathlib import Path
from datetime import datetime

from squidy.adapters.filesystem.mock_fs import MockFileSystem
from squidy.core.domain.config import ProjectConfig
from squidy.core.i18n import I18nManager, i18n
from squidy.generation.file_generator import FileGenerator
from squidy.audit.engine import AuditEngine
from squidy.audit.checkers.structure_checker import StructureChecker
from squidy.audit.detectors.heuristic_detector import HeuristicDetector


class TestI18nIntegration:
    """Testes de integração de internacionalização"""
    
    def setup_method(self):
        """Setup para cada teste"""
        I18nManager._instance = None
    
    def test_file_generation_with_language_pt(self):
        """Testa geração de arquivos em português"""
        i18n.set_language("pt-BR")
        fs = MockFileSystem()
        generator = FileGenerator(fs)
        
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Projeto de teste",
        )
        
        output_dir = Path("/test-output")
        generator.generate_all(config, output_dir, progress=False)
        
        # Verifica conteúdo em português
        readme_content = fs.read_text(output_dir / "readme-agent.md")
        assert "Ritual de Inicialização" in readme_content
        assert "Contexto do Projeto" in readme_content
    
    def test_file_generation_with_language_en(self):
        """Testa geração de arquivos em inglês"""
        i18n.set_language("en-US")
        fs = MockFileSystem()
        generator = FileGenerator(fs)
        
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Test purpose",
        )
        
        output_dir = Path("/test-output")
        generator.generate_all(config, output_dir, progress=False)
        
        # Verifica conteúdo em inglês
        readme_content = fs.read_text(output_dir / "readme-agent.md")
        assert "Initialization Ritual" in readme_content
        assert "Project Context" in readme_content
    
    def test_manifest_contains_language(self):
        """Testa que manifest.json contém o idioma"""
        i18n.set_language("en-US")
        fs = MockFileSystem()
        generator = FileGenerator(fs)
        
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Test purpose",
        )
        
        output_dir = Path("/test-output")
        generator.generate_all(config, output_dir, progress=False)
        
        # Verifica manifest
        import json
        manifest_content = fs.read_text(output_dir / ".squidy" / "manifest.json")
        manifest = json.loads(manifest_content)
        
        assert manifest["language"] == "en-US"
    
    def test_switching_language_between_generations(self):
        """Testa alternar idioma entre gerações"""
        fs = MockFileSystem()
        generator = FileGenerator(fs)
        
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Test",
        )
        
        # Gera em português
        i18n.set_language("pt-BR")
        output_dir_pt = Path("/test-output-pt")
        generator.generate_all(config, output_dir_pt, progress=False)
        
        # Gera em inglês
        i18n.set_language("en-US")
        output_dir_en = Path("/test-output-en")
        generator.generate_all(config, output_dir_en, progress=False)
        
        # Verifica diferenças
        readme_pt = fs.read_text(output_dir_pt / "readme-agent.md")
        readme_en = fs.read_text(output_dir_en / "readme-agent.md")
        
        assert "Ritual de Inicialização" in readme_pt
        assert "Initialization Ritual" in readme_en
        assert readme_pt != readme_en


class TestFileGeneration:
    """Testes de geração de arquivos"""
    
    def test_generate_all_files(self):
        """Testa geração completa de arquivos"""
        fs = MockFileSystem()
        generator = FileGenerator(fs)
        
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Projeto de teste",
            stack={
                "frontend": "React",
                "backend": "Node.js",
                "banco": "PostgreSQL",
            },
        )
        
        output_dir = Path("/test-output")
        generated = generator.generate_all(config, output_dir, progress=False)
        
        # Verifica se todos os arquivos foram gerados
        assert len(generated) == 10  # 9 arquivos + diário
        
        # Verifica se arquivos existem no filesystem mock
        assert fs.exists(output_dir / "readme-agent.md")
        assert fs.exists(output_dir / "doc" / "constituicao.md")
        assert fs.exists(output_dir / "doc" / "kanban.md")
        assert fs.exists(output_dir / "diario")
    
    def test_generate_single_file(self):
        """Testa geração de arquivo único"""
        fs = MockFileSystem()
        generator = FileGenerator(fs)
        
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Projeto de teste",
        )
        
        output_dir = Path("/test-output")
        path = generator.generate_single(config, output_dir, "readme-agent.md")
        
        assert path == "readme-agent.md"
        assert fs.exists(output_dir / "readme-agent.md")


class TestAudit:
    """Testes de auditoria"""
    
    def test_structure_checker_finds_missing_files(self):
        """Testa que StructureChecker encontra arquivos faltantes"""
        fs = MockFileSystem()
        checker = StructureChecker(fs)
        
        # Cria diretório vazio
        project_path = Path("/test-project")
        fs.mkdir(project_path / "doc", parents=True)
        fs.mkdir(project_path / "diario", parents=True)
        
        # Executa checker
        findings = checker.check(project_path)
        
        # Deve encontrar arquivos faltantes
        assert len(findings) > 0
        assert any("readme-agent.md" in f.message for f in findings)
    
    def test_structure_checker_passes_complete_project(self):
        """Testa que StructureChecker passa em projeto completo"""
        fs = MockFileSystem()
        generator = FileGenerator(fs)
        
        # Gera projeto completo
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Projeto de teste",
        )
        
        project_path = Path("/test-project")
        generator.generate_all(config, project_path, progress=False)
        
        # Executa checker
        checker = StructureChecker(fs)
        findings = checker.check(project_path)
        
        # Não deve haver findings críticos
        critical = [f for f in findings if f.severity.value == "critical"]
        assert len(critical) == 0
    
    def test_heuristic_detector(self):
        """Testa detector heurístico"""
        fs = MockFileSystem()
        detector = HeuristicDetector(fs)
        
        # Sem arquivos - não deve detectar
        project_path = Path("/empty-project")
        fs.mkdir(project_path, parents=True)
        
        assert not detector.detect(project_path)
        assert detector.get_confidence(project_path) == 0.0
        
        # Com arquivos característicos - deve detectar
        fs.write_text(project_path / "readme-agent.md", "# Test")
        fs.write_text(project_path / "doc" / "constituicao.md", "# Test")
        fs.write_text(project_path / "doc" / "kanban.md", "# Test")
        
        assert detector.detect(project_path)
        assert detector.get_confidence(project_path) > 0.5


class TestProjectConfig:
    """Testes de configuração"""
    
    def test_config_validation(self):
        """Testa validação de configuração"""
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Teste",
        )
        
        assert config.project_name == "test-project"
        assert config.display_name == "Test Project"
        assert len(config.principios) > 0  # Valores padrão
        assert len(config.proibicoes) > 0
        assert len(config.dod) > 0
    
    def test_config_to_dict(self):
        """Testa conversão para dicionário"""
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Teste",
        )
        
        data = config.to_dict()
        
        assert data["project_name"] == "test-project"
        assert data["display_name"] == "Test Project"
        assert "stack" in data


class TestFileGeneration:

    
    def test_generate_all_files(self):
        """Testa geração completa de arquivos"""
        fs = MockFileSystem()
        generator = FileGenerator(fs)
        
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Projeto de teste",
            stack={
                "frontend": "React",
                "backend": "Node.js",
                "banco": "PostgreSQL",
            },
        )
        
        output_dir = Path("/test-output")
        generated = generator.generate_all(config, output_dir, progress=False)
        
        # Verifica se todos os arquivos foram gerados (10 templates + 1 diário + 1 manifest)
        assert len(generated) == 12
        
        # Verifica se arquivos existem no filesystem mock
        assert fs.exists(output_dir / "readme-agent.md")
        assert fs.exists(output_dir / "doc" / "constituicao.md")
        assert fs.exists(output_dir / "doc" / "kanban.md")
        assert fs.exists(output_dir / "diario")
        assert fs.exists(output_dir / ".squidy" / "manifest.json")
    
    def test_generate_single_file(self):
        """Testa geração de arquivo único"""
        fs = MockFileSystem()
        generator = FileGenerator(fs)
        
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Projeto de teste",
        )
        
        output_dir = Path("/test-output")
        path = generator.generate_single(config, output_dir, "readme-agent.md")
        
        assert path == "readme-agent.md"
        assert fs.exists(output_dir / "readme-agent.md")


class TestAudit:
    """Testes de auditoria"""
    
    def test_structure_checker_finds_missing_files(self):
        """Testa que StructureChecker encontra arquivos faltantes"""
        fs = MockFileSystem()
        checker = StructureChecker(fs)
        
        # Cria diretório vazio
        project_path = Path("/test-project")
        fs.mkdir(project_path / "doc", parents=True)
        fs.mkdir(project_path / "diario", parents=True)
        
        # Executa checker
        findings = checker.check(project_path)
        
        # Deve encontrar arquivos faltantes
        assert len(findings) > 0
        assert any("readme-agent.md" in f.message for f in findings)
    
    def test_structure_checker_passes_complete_project(self):
        """Testa que StructureChecker passa em projeto completo"""
        fs = MockFileSystem()
        generator = FileGenerator(fs)
        
        # Gera projeto completo
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Projeto de teste",
        )
        
        project_path = Path("/test-project")
        generator.generate_all(config, project_path, progress=False)
        
        # Executa checker
        checker = StructureChecker(fs)
        findings = checker.check(project_path)
        
        # Não deve haver findings críticos
        critical = [f for f in findings if f.severity.value == "critical"]
        assert len(critical) == 0
    
    def test_heuristic_detector(self):
        """Testa detector heurístico"""
        fs = MockFileSystem()
        detector = HeuristicDetector(fs)
        
        # Sem arquivos - não deve detectar
        project_path = Path("/empty-project")
        fs.mkdir(project_path, parents=True)
        
        assert not detector.detect(project_path)
        assert detector.get_confidence(project_path) == 0.0
        
        # Com arquivos característicos - deve detectar
        fs.write_text(project_path / "readme-agent.md", "# Test")
        fs.write_text(project_path / "doc" / "constituicao.md", "# Test")
        fs.write_text(project_path / "doc" / "kanban.md", "# Test")
        
        assert detector.detect(project_path)
        assert detector.get_confidence(project_path) > 0.5


class TestProjectConfig:
    """Testes de configuração"""
    
    def test_config_validation(self):
        """Testa validação de configuração"""
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Teste",
        )
        
        assert config.project_name == "test-project"
        assert config.display_name == "Test Project"
        assert len(config.principios) > 0  # Valores padrão
        assert len(config.proibicoes) > 0
        assert len(config.dod) > 0
    
    def test_config_to_dict(self):
        """Testa conversão para dicionário"""
        config = ProjectConfig(
            project_name="test-project",
            display_name="Test Project",
            proposito="Teste",
        )
        
        data = config.to_dict()
        
        assert data["project_name"] == "test-project"
        assert data["display_name"] == "Test Project"
        assert "stack" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
