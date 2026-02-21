# 🤝 Contribuindo com o Squidy

Obrigado por seu interesse em contribuir com o Squidy! 🦑

## 📋 Como Contribuir

### 1. Reportando Bugs

- Use o [GitHub Issues](https://github.com/seomarc/squidy/issues)
- Descreva o bug detalhadamente
- Inclua passos para reproduzir
- Informe versão do Python e SO

### 2. Sugerindo Features

- Abra uma issue com label `enhancement`
- Explique o problema que a feature resolve
- Descreva a solução proposta

### 3. Pull Requests

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 🛠️ Setup de Desenvolvimento

```bash
# Clone
git clone https://github.com/seomarc/squidy.git
cd squidy

# Cria ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instala dependências
pip install -e ".[dev]"

# Verifica instalação
squidy --version
```

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Com cobertura
pytest --cov=squidy --cov-report=html

# Testes específicos
pytest tests/test_integration.py -v
```

## 🎨 Code Style

Usamos:
- **Black** - Formatação
- **isort** - Ordenação de imports
- **mypy** - Type checking
- **pylint** - Linting

```bash
# Formata código
black squidy/ tests/

# Ordena imports
isort squidy/ tests/

# Type check
mypy squidy/

# Lint
pylint squidy/

# Roda tudo
pre-commit run --all-files
```

## 📝 Convenções de Commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(escopo): descrição

[corpo opcional]

[rodapé opcional]
```

**Tipos:**
- `feat`: Nova feature
- `fix`: Bug fix
- `docs`: Documentação
- `test`: Testes
- `refactor`: Refatoração
- `chore`: Tarefas diversas

**Exemplos:**
```
feat(audit): adiciona KanbanChecker
fix(cli): corrige erro no banner
docs(readme): atualiza instruções de instalação
```

## 🏗️ Arquitetura

O Squidy segue **Clean Architecture**:

```
squidy/
├── cli/          # Interface (Typer + Rich)
├── core/         # Regras de negócio
│   ├── domain/   # Entidades
│   ├── ports/    # Interfaces
│   └── use_cases/# Casos de uso
├── adapters/     # Implementações
│   ├── filesystem/
│   └── providers/
├── audit/        # Sistema de auditoria
├── generation/   # Geração de arquivos
└── plugins/      # Sistema de plugins
```

### Adicionando um Novo Checker

1. Crie classe em `squidy/audit/checkers/`
2. Herde de `BaseChecker`
3. Implemente método `check()`
4. Registre em `AuditEngine`

**Exemplo:**
```python
from squidy.audit.checkers.base import BaseChecker
from squidy.core.domain.audit_result import Finding, Severity

class MeuChecker(BaseChecker):
    name = "MeuChecker"
    
    def check(self, project_path, project_name=None):
        findings = []
        
        # Lógica de verificação
        if problema:
            findings.append(self._create_finding(
                message="Descrição do problema",
                severity=Severity.MEDIUM,
                suggestion="Como corrigir",
            ))
        
        return findings
```

### Adicionando um Novo Provider

1. Crie classe em `squidy/adapters/providers/`
2. Herde de `AIProviderPort`
3. Implemente métodos obrigatórios

## 🎯 Prioridades

1. **Bugs críticos** - Segurança, crashes
2. **Features core** - Funcionalidades principais
3. **DX** - Developer experience
4. **Docs** - Documentação
5. **Refactoring** - Melhorias de código

## 💬 Comunidade

- 💬 [Discord](https://discord.gg/squidy)
- 🐦 [Twitter](https://twitter.com/squidydev)
- 📧 [Email](mailto:contato@squidy.run)

## 📜 Código de Conduta

- Seja respeitoso
- Aceite críticas construtivas
- Foque no que é melhor para a comunidade
- Mostre empatia

---

**Perguntas?** Abra uma issue ou entre em contato!

Obrigado por contribuir! 🦑✨
