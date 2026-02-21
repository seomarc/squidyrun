# Changelog

Todas as mudanças notáveis neste projeto são documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [2.0.0] - 2026-02-21

### 🎉 Lançamento Major

Squidy v2.0 - Refatoração completa com arquitetura profissional, auditoria e UI/UX premium.

### ✨ Novidades

#### 🎨 UI/UX Premium
- Interface completamente redesenhada com Rich
- Banner premium com ASCII art e gradientes
- Menu com hierarquia visual e badge "★ POPULAR"
- Fluxo de entrevista imersivo com barra de progresso
- Tela de conclusão celebrativa
- Temas personalizáveis (Oceano Digital)

#### 🤖 Agente de IA Aprimorado
- Entrevista em 5 fases estruturadas
- Follow-ups inteligentes e sugestões contextuais
- Prompts otimizados para melhor qualidade
- JSON enriquecido com contexto de negócio, arquitetura e qualidade
- Templates v2.0 mais completos e acionáveis

#### 🔍 Sistema de Auditoria
- `squidy audit` - Audita projetos existentes
- `squidy status` - Status rápido
- `squidy doctor` - Diagnóstico completo
- Checkers: Structure, Kanban, Freshness, Consistency
- Detectors: Manifest e Heuristic
- Saída em console, JSON e Markdown

#### 🏗️ Arquitetura Profissional
- Clean Architecture + Ports & Adapters
- Separação clara: CLI → Core → Adapters
- Sistema de plugins extensível
- Testabilidade com MockFileSystem
- Código type-hinted e documentado

#### 📋 Templates v2.0
- `readme-agent.md` - Guia completo com hierarquia de tarefas
- `kanban.md` - Épicos → Tasks → Subtarefas
- `constituicao.md` - Convenções de nomenclatura completas
- `oraculo.md` - ADRs estruturados
- Todos os templates enriquecidos e mais úteis

### 🔧 Melhorias Técnicas

- **CLI**: Migrado para Typer com comandos organizados
- **Providers**: Adapters para OpenAI, Anthropic e OpenRouter
- **Filesystem**: Port abstrato para facilitar testes
- **Config**: Validação com Pydantic
- **Templates**: Engine Jinja2 com filtros customizados

### 📁 Nova Estrutura

```
squidy/
├── cli/              # Interface (Typer + Rich)
├── core/             # Regras de negócio
│   ├── domain/       # Entidades (Project, Config, AuditResult)
│   ├── ports/        # Interfaces (FileSystem, AIProvider, Storage)
│   └── use_cases/    # Casos de uso
├── adapters/         # Implementações
│   ├── filesystem/   # LocalFileSystem, MockFileSystem
│   └── providers/    # OpenAI, Anthropic, OpenRouter adapters
├── audit/            # Sistema de auditoria
│   ├── checkers/     # Structure, Kanban, Freshness, Consistency
│   ├── detectors/    # Manifest, Heuristic
│   └── engine.py     # AuditEngine
├── generation/       # Geração de arquivos
│   ├── file_generator.py
│   └── template_engine.py
└── plugins/          # Sistema de plugins
```

### 🚀 Comandos

```bash
# Inicialização
squidy init                      # Setup com IA
squidy init --dry-run            # Simulação
squidy init --manual             # Setup manual
squidy init --only-missing       # Cria apenas faltantes

# Auditoria
squidy audit                     # Audita diretório atual
squidy audit ./projeto           # Audita projeto
squidy audit --fix               # Aplica correções
squidy audit -f json             # Saída JSON
squidy audit -c structure,kanban # Checkers específicos

# Status
squidy status                    # Status rápido
squidy doctor                    # Diagnóstico completo
```

### 📝 Templates

Todos os templates foram reescritos:

- `readme-agent.md` - Tom mais acolhedor, guia completo do kanban
- `constituicao.md` - Convenções de nomenclatura, exemplos práticos
- `kanban.md` - Hierarquia completa, métricas, prioridades
- `oraculo.md` - ADRs mais estruturados
- `politicas.md` - Políticas de segurança e deploy
- `emergencia.md` - Template de bloqueios melhorado
- `indice-diario.md` - Guia de como registrar
- `contexto-sessao.md` - Estado atual mais detalhado
- `AGENT.md` - Referência rápida consolidada

### 🧪 Testes

- Testes de integração com MockFileSystem
- Cobertura de FileGenerator, AuditEngine, Checkers
- Validação de ProjectConfig

### 📚 Documentação

- README.md completo
- CONTRIBUTING.md com guia de contribuição
- CHANGELOG.md (este arquivo)
- Licença MIT

### ⚠️ Breaking Changes

Esta é uma versão major (2.0.0) com mudanças incompatíveis:

- Estrutura de pastas completamente nova
- Comandos CLI diferentes (typer ao invés de menu interativo)
- Formato de configuração enriquecido
- Templates incompatíveis com v1.x

**Para migrar de v1.x:**
1. Faça backup dos arquivos existentes
2. Execute `squidy init` na pasta do projeto
3. Copie informações relevantes dos arquivos antigos

---

## [1.0.2] - 2026-02-13

### 🐛 Correções

- Restaurado doc/AGENT.md alongside readme-agent.md

## [1.0.0] - 2026-02-13

### 🎉 Lançamento Inicial

- Setup com Agente IA via entrevista adaptativa (5-6 perguntas)
- Suporte a 3 provedores: OpenAI, Anthropic, OpenRouter
- Geração automática de 9 arquivos de documentação
- Setup manual/offline sem necessidade de API key
- Gerenciamento seguro de credenciais (getpass + limpeza de memória)
- Interface CLI com Rich: banner, menus, spinners, progresso

---

## Legenda

- 🎉 Lançamento
- ✨ Novo
- 🚀 Melhoria
- 🐛 Correção
- 📝 Documentação
- ⚠️ Breaking Change
