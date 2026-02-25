# 🦑 Squidy v2.1.0

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/i18n-🇧🇷🇺🇸-green.svg" alt="i18n">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/code%20style-black-black.svg" alt="Code style: black">
  <img src="https://img.shields.io/github/stars/seomarc/squidyrun?style=social" alt="Stars">
</p>

<p align="center">
  <b>Setup inteligente para projetos com Agentes de IA</b><br>
  Governança, Auditoria e Documentação Automática para Claude, GPT-4, Cursor e mais
</p>

<p align="center">
  <a href="#-instalação">Instalação</a> •
  <a href="#-como-usar">Como Usar</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-documentação">Documentação</a> •
  <a href="#-contribuindo">Contribuindo</a>
</p>

---

## 🎯 O Problema

Você usa **Claude**, **ChatGPT** ou **Cursor** para programar, mas:

- 🤯 **A IA esquece tudo** na próxima conversa (perda de contexto)
- 📝 **Você reescreve** os mesmos requisitos toda semana
- 🎨 **O agente fica "criativo"** e muda sua arquitetura sem avisar
- 📂 **Seu projeto vira bagunça** porque ninguém documenta nada
- ⏱️ **Gasta 30 min** configurando prompt antes de começar a codar

**O Squidy resolve isso em 2 minutos.**

---

## ✨ O Que é o Squidy?

O **Squidy** é uma CLI premium que cria automaticamente a estrutura de governança para projetos com Agentes de IA.

### 🚀 Em vez de digitar 20 mensagens explicando seu projeto toda vez:

1. 🎤 **Converse com IA** sobre seu projeto (5-6 perguntas inteligentes)
2. 🧠 **Deixe a IA entender** seu stack, regras e convenções
3. 📋 **Receba 10 arquivos de documentação** prontos para usar
4. 🔒 **Crie um "contrato"** entre você e a IA: regras, proibições, DoD

**Resultado:** Sua IA nunca mais perde o contexto ou sai do escopo.

---

## 🎬 Demo

```bash
$ squidy init

🦑 Setup com Agente IA

Como funciona:
  1. Me conte sobre o projeto (uma frase é suficiente)
  2. Farei até 6 perguntas contextuais
  3. Gero automaticamente 10 arquivos de documentação

🤖 Agente: Olá! Me conte sobre o projeto que você quer configurar.
           Exemplo: "API REST para delivery com Node e PostgreSQL"
   Você: API REST para delivery com Node e PostgreSQL

🤖 Agente: Legal! Qual framework frontend você vai usar?
   Você: React com TypeScript

🤖 Agente: Perfeito! Vai precisar de autenticação?
   Você: Sim, JWT

... (mais 2-3 perguntas) ...

✅ Configuração gerada com sucesso!

🦑 10 arquivos gerados em /home/user/delivery-api

Próximos passos:
  1. Diga ao seu agente: "Acesse /home/user/delivery-api/readme-agent.md e siga o ritual"
  2. Revise /home/user/delivery-api/doc/constituicao.md
  3. Adicione tarefas em /home/user/delivery-api/doc/kanban.md
```

---

## 📦 Instalação

### Via pip (recomendado)

```bash
pip install squidy
squidy --version
```

### Via pipx (isolado)

```bash
pipx install squidy
squidy --version
```

### Desenvolvimento

```bash
git clone https://github.com/seomarc/squidyrun.git
cd squidyrun
python -m venv venv && source venv/bin/activate  # Linux/Mac
# ou: python -m venv venv && venv\Scripts\activate  # Windows
pip install -e ".[dev]"
squidy --version
```

**Requisitos:** Python 3.9+

---

## 🎮 Como Usar

### Setup com IA (Recomendado)

```bash
# Setup interativo com entrevista IA
squidy init

# Especificar caminho
squidy init ./meu-projeto

# Simular sem criar arquivos (dry-run)
squidy init --dry-run

# Setup manual (sem IA)
squidy init --manual

# Escolher idioma (pt-BR ou en-US)
squidy init --lang en-US
```

### 🌍 Idiomas Suportados

O Squidy v2.1+ suporta múltiplos idiomas! Toda a documentação e interface são geradas no idioma selecionado:

| Idioma | Código | Status |
|--------|--------|--------|
| 🇧🇷 Português (Brasil) | `pt-BR` | ✅ Completo |
| 🇺🇸 English (US) | `en-US` | ✅ Completo |

**Como usar:**
```bash
# Selecionar idioma via flag
squidy init --lang en-US

# Ou deixe o Squidy detectar automaticamente
squidy init

# 🌍 Selecione o idioma / Select language:
# [1] 🇧🇷 Português (Brasil)
# [2] 🇺🇸 English (US)
```

📖 **[Guia Completo de Internacionalização](docs/I18N.md)**

**O que é traduzido:**
- ✅ Interface CLI completa
- ✅ Todos os 10 templates de documentação
- ✅ Prompts de entrevista com IA
- ✅ Mensagens de auditoria e status

### Auditoria de Projeto

```bash
# Audita diretório atual
squidy audit

# Audita projeto específico
squidy audit ./meu-projeto

# Saída em JSON
squidy audit -f json

# Aplicar correções automáticas
squidy audit --fix
```

### Status Rápido

```bash
# Mostra status do projeto
squidy status

# Diagnóstico completo
squidy doctor
```

---

## 🏗️ O Que o Squidy Cria?

O Squidy gera uma estrutura de governança completa:

```
meu-projeto/
├── readme-agent.md          # 🤖 Guia completo para o agente de IA
├── .squidy/
│   └── manifest.json        # 📋 Manifesto do projeto
├── doc/
│   ├── AGENT.md             # 🎯 Referência rápida do agente
│   ├── constituicao.md      # ⚖️  Princípios, proibições, DoD
│   ├── oraculo.md           # 🧙 Decisões de arquitetura (ADRs)
│   ├── politicas.md         # 📋 Stack, convenções, políticas
│   ├── kanban.md            # 📊 Gestão de tarefas (Épicos → Tasks → Subtarefas)
│   ├── emergencia.md        # 🚨 Registro de bloqueios críticos
│   ├── indice-diario.md     # 📑 Índice do histórico
│   └── contexto-sessao.md   # 💾 Cache do estado atual
└── diario/
    └── 2026-02.md           # 📅 Log automático de decisões
```

### 📋 Estrutura do Kanban

```markdown
## 🔥 ÉPICOS
### ÉPICO-001: Sistema de Autenticação
**Prioridade:** P0 | **Complexidade:** M
**Tasks:** TASK-001, TASK-002

## 📋 BACKLOG
### TASK-001: Setup JWT [ÉPICO-001]
**Complexidade:** S | **Prioridade:** P0
**Subtarefas:**
- [ ] SUB-001: Instalar biblioteca (XS - 30min)
- [ ] SUB-002: Configurar middleware (S - 1h)

## 🏗️ EM PROGRESSO (WIP: 1/3)
- [ ] TASK-001: Setup JWT

## ✅ CONCLUÍDO
- [x] TASK-000: Setup inicial
```

---

## 🎨 Funcionalidades

### ✨ v2.1 - Novidades

- 🌍 **Multi-idioma** - Suporte completo a Português e Inglês (pt-BR, en-US)
- 📋 **Templates Bilíngues** - Documentação gerada no idioma selecionado
- 🤖 **IA Multi-idioma** - Entrevista e configuração em português ou inglês

### ✨ v2.0 - Novidades

- 🎨 **UI/UX Premium** - Interface moderna com Rich, gradientes e animações
- 🤖 **Entrevista Inteligente** - 5 fases estruturadas com follow-ups contextuais
- 📊 **Auditoria Completa** - Verifica estrutura, kanban, freshness e consistência
- 🔌 **Arquitetura Limpa** - Ports & Adapters, extensível e testável
- 📋 **Templates v2.0** - Documentação mais completa e acionável
- 🧪 **Testes** - Suite com pytest, 10/10 passando

### 🤖 Provedores de IA Suportados

| Provedor | Modelos | Custo |
|----------|---------|-------|
| **OpenAI** | GPT-4o-mini | Pago |
| **Anthropic** | Claude 3 Haiku/Sonnet | Pago |

### 🔍 Auditoria

O Squidy pode auditar projetos existentes:

- ✅ **StructureChecker** - Verifica arquivos obrigatórios
- ✅ **KanbanChecker** - Analisa WIP limit, tarefas bloqueadas
- ✅ **FreshnessChecker** - Identifica arquivos desatualizados
- ✅ **ConsistencyChecker** - Verifica consistência entre arquivos

---

## 🛠️ Stack Tecnológica

- **Python 3.9+** - Linguagem principal
- **Typer** - CLI framework
- **Rich** - UI components e formatação
- **Pydantic v2** - Validação de dados
- **Jinja2** - Templates
- **OpenAI / Anthropic** - Provedores de IA

---

## 📚 Documentação

- 📖 [Documentação Completa](https://docs.squidy.run)
- 🌍 **[Guia de Internacionalização](docs/I18N.md)** - Multi-idioma (pt-BR, en-US)
- 🚀 [Guia de Início Rápido](https://docs.squidy.run/quickstart)
- 🏗️ [Arquitetura](https://docs.squidy.run/architecture)
- 🤝 [Contribuindo](CONTRIBUTING.md)
- 🌐 [Contribuindo com Traduções](CONTRIBUTING-I18N.md)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Leia nosso [Guia de Contribuição](CONTRIBUTING.md).

### Desenvolvimento

```bash
# Clone
git clone https://github.com/seomarc/squidyrun.git
cd squidyrun

# Setup
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"

# Testes
pytest

# Lint
black squidy/
isort squidy/
mypy squidy/

# Commit
pre-commit run --all-files
```

---

## 📈 Roadmap

### v2.1 ✅ Lançado!
- [x] 🌍 **Suporte Multi-idioma** - Português e Inglês
- [ ] Templates para mais stacks (Vue, Svelte, Go, Rust)
- [ ] Integração com GitHub/GitLab
- [ ] Sync com Notion/Confluence

### v2.2 (Próximo)
- [ ] Dashboard web (Squidy Cloud)
- [ ] Mais idiomas (Espanhol, Francês, Alemão)
- [ ] Plugins oficiais (Git, Jira, Slack)
- [ ] API REST
- [ ] CLI autocompletion
- [ ] Temas customizáveis

### v2.2
- [ ] Plugins oficiais (Git, Jira, Slack)
- [ ] API REST
- [ ] CLI autocompletion
- [ ] Temas customizáveis

### v3.0
- [ ] Squidy Cloud (SaaS)
- [ ] Colaboração em tempo real
- [ ] Analytics de projeto
- [ ] Enterprise features

---

## 🔗 Links

<p align="center">
  <a href="https://squidy.run">🌐 Site</a> •
  <a href="https://pypi.org/project/squidy/">📦 PyPI</a> •
  <a href="https://github.com/seomarc/squidyrun">💻 GitHub</a> •
  <a href="https://www.youtube.com/@seomarcos">▶️ YouTube</a> •
  <a href="https://www.linkedin.com/in/seomarc/">💼 LinkedIn</a> •
  <a href="https://buymeacoffee.com/seomarcos">☕ Buy Me a Coffee</a>
</p>

### 👤 Desenvolvedor

- **Marcos Tadeu** - [Site Pessoal](https://www.marcostadeu.com.br/)
- **SearchOps** - [searchops.io](https://searchops.io/)

---

## 💖 Apoie o Projeto

Se o Squidy te ajudou, considere:

- ⭐ Dar uma estrela no [GitHub](https://github.com/seomarc/squidyrun)
- 🐦 Compartilhar no Twitter
- 💼 Usar na sua empresa
- 🤝 Contribuir com código
- ☕ [Buy Me a Coffee](https://buymeacoffee.com/seomarcos)

---

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

<p align="center">
  Feito com 🦑 por <a href="https://github.com/seomarc">Marcos Tadeu</a> • <a href="https://github.com/seomarc/squidyrun">💻 GitHub do Projeto</a>
</p>

<p align="center">
  <a href="https://squidy.run">🌐 squidy.run</a> •
  <a href="https://pypi.org/project/squidy/">📦 PyPI</a> •
  <a href="https://github.com/seomarc/squidyrun">💻 GitHub</a> •
  <a href="https://www.youtube.com/@seomarcos">▶️ YouTube</a> •
  <a href="https://www.linkedin.com/in/seomarc/">💼 LinkedIn</a> •
  <a href="https://www.marcostadeu.com.br/">👤 Desenvolvedor</a> •
  <a href="https://searchops.io/">🏢 SearchOps</a> •
  <a href="mailto:contato@squidy.run">✉️ Contato</a>
</p>
