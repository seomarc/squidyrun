# 🤝 Guia de Contribuição - Traduções

Obrigado por querer contribuir com traduções para o Squidy! Este guia explica como adicionar novos idiomas ou melhorar traduções existentes.

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Como Contribuir](#como-contribuir)
3. [Estrutura de Tradução](#estrutura-de-tradução)
4. [Checklist de Qualidade](#checklist-de-qualidade)
5. [Testando Traduções](#testando-traduções)

---

## Visão Geral

O Squidy usa um sistema de tradução baseado em arquivos YAML:

- **`messages.yaml`** - Mensagens da interface CLI
- **`templates.yaml`** - Termos usados na documentação gerada
- **`prompts.yaml`** - Prompts para os provedores de IA

---

## Como Contribuir

### 1. Criar Nova Tradução

```bash
# 1. Fork o repositório
# 2. Clone seu fork
git clone https://github.com/seu-usuario/squidyrun.git
cd squidyrun

# 3. Crie uma branch
git checkout -b feat/translate-xx-XX

# 4. Crie o diretório do idioma
mkdir -p squidy/locales/xx-XX

# 5. Copie os arquivos base (recomendado: use en-US)
cp squidy/locales/en-US/*.yaml squidy/locales/xx-XX/

# 6. Traduza os arquivos
# ... edite os arquivos YAML ...

# 7. Adicione o idioma ao I18nManager
# Edite squidy/core/i18n.py

# 8. Teste
pytest tests/test_i18n.py tests/test_templates_i18n.py -v

# 9. Commit e push
git add .
git commit -m "feat(i18n): add XX-XX language support"
git push origin feat/translate-xx-XX

# 10. Crie um Pull Request
```

### 2. Melhorar Tradução Existente

```bash
# 1. Edite o arquivo diretamente
# squidy/locales/pt-BR/messages.yaml

# 2. Teste
pytest tests/test_i18n.py -v

# 3. Commit
git commit -m "fix(i18n): improve pt-BR translations"
```

---

## Estrutura de Tradução

### messages.yaml

```yaml
# Seção: init (comando init)
init:
  title: "🤖 Setup com IA"
  success: "✅ Setup concluído!"
  next_steps: "Próximos passos"
  # Use {placeholder} para valores dinâmicos
  next_step_1: "Diga ao seu agente: 'Acesse {path}/readme-agent.md'"

# Seção: audit (comando audit)
audit:
  title: "🔍 Auditando"
  severity_critical: "🔴 Crítico"
  severity_high: "🟠 Alto"
```

### templates.yaml

```yaml
# Termos para seções de documentação
doc_sections:
  constitution: "CONSTITUTION"
  kanban: "KANBAN"

# Seções do kanban
kanban_sections:
  epics: "EPICS"
  backlog: "BACKLOG"
```

### prompts.yaml

```yaml
interview:
  system_prompt: |
    You are a Senior Software Architect...
    
config:
  system_prompt: |
    Generate Squidy configuration JSON...
    
  required_fields:
    - project_name
    - display_name
```

---

## Checklist de Qualidade

Antes de enviar sua contribuição:

### ✅ Sintaxe YAML

```bash
# Valide sintaxe
python -c "import yaml; yaml.safe_load(open('squidy/locales/xx-XX/messages.yaml'))"
```

### ✅ Cobertura

- [ ] `messages.yaml` 100% traduzido
- [ ] `templates.yaml` 100% traduzido
- [ ] `prompts.yaml` 100% traduzido

### ✅ Testes

```bash
# Execute testes de i18n
pytest tests/test_i18n.py -v

# Execute testes de templates
pytest tests/test_templates_i18n.py -v

# Execute todos os testes
pytest
```

### ✅ Consistência

- [ ] Termos técnicos mantidos quando apropriado
- [ ] Placeholders `{name}` preservados
- [ ] Emojis mantidos
- [ ] Formatação Markdown preservada

---

## Testando Traduções

### Teste Manual

```bash
# Instale em modo desenvolvimento
pip install -e ".[dev]"

# Teste o novo idioma
squidy init --lang xx-XX --dry-run
```

### Teste de Renderização

```python
from squidy.generation.template_engine import TemplateEngine

engine = TemplateEngine()

# Teste cada template
templates = [
    "readme-agent.md",
    "constituicao.md",
    "kanban.md",
    # ... todos os templates
]

for template in templates:
    content = engine.render(template, language="xx-XX", display_name="Test")
    assert "{{" not in content  # Não deve haver tags não renderizadas
    print(f"✓ {template}")
```

---

## Convenções

### Termos Técnicos

Mantenha em inglês quando for padrão da indústria:

```yaml
# Mantido em inglês
- commit, merge, pull request
- frontend, backend, API
- camelCase, PascalCase, snake_case
- MVP, CI/CD, JWT
```

### Placeholders

Sempre use `{placeholder}` para valores dinâmicos:

```yaml
# Correto
path_message: "Files generated at {path}"

# Incorreto
path_message: "Files generated at PATH"
```

### Tom de Voz

**Português:** Formal mas acolhedor
```yaml
init:
  title: "🤖 Setup com IA"
  greeting: "Olá! Pronto para começar?"
```

**Inglês:** Profissional mas amigável
```yaml
init:
  title: "🤖 Setup with AI"
  greeting: "Hi! Ready to get started?"
```

---

## Dúvidas?

Abra uma issue em https://github.com/seomarc/squidyrun/issues

---

Obrigado por contribuir! 🦑
