# 🦑 Squidy v2.1.2

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.2-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/i18n-🇧🇷🇺🇸-green.svg" alt="i18n">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/code%20style-black-black.svg" alt="Code style: black">
  <img src="https://img.shields.io/github/stars/seomarc/squidyrun?style=social" alt="Stars">
</p>

<p align="center">
  <b>Smart Setup for AI Agent Projects</b><br>
  Governance, Audit, and Automatic Documentation for Claude, GPT-4, Cursor, and more
</p>

<p align="center">
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-features">Features</a> •
  <a href="#-documentation">Documentation</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=seomarc/squidyrun&type=date&legend=top-left)](https://www.star-history.com/#seomarc/squidyrun&type=date&legend=top-left)

---

## 🎯 The Problem

You use **Claude**, **ChatGPT**, or **Cursor** to code, but:

- 🤯 **AI forgets everything** in the next conversation (context loss)
- 📝 **You rewrite** the same requirements every week
- 🎨 **The agent gets "creative"** and changes your architecture without warning
- 📂 **Your project becomes a mess** because no one documents anything
- ⏱️ **You spend 30 min** setting up prompts before you start coding

**Squidy solves this in 2 minutes.**

---

## ✨ What is Squidy?

**Squidy** is a premium CLI that automatically creates a governance structure for AI Agent projects.

### 🚀 Instead of typing 20 messages explaining your project every time:

1. 🎤 **Chat with AI** about your project (5-6 smart questions)
2. 🧠 **Let the AI understand** your stack, rules, and conventions
3. 📋 **Get 10 documentation files** ready to use
4. 🔒 **Create a "contract"** between you and the AI: rules, prohibitions, DoD

**Result:** Your AI never loses context or goes out of scope.

---

## 🎬 Demo

```bash
$ squidy init

🦑 AI Agent Setup

How it works:
  1. Tell me about your project (one sentence is enough)
  2. I'll ask up to 6 contextual questions
  3. Automatically generate 10 documentation files

🤖 Agent: Hi! Tell me about the project you want to configure.
         Example: "REST API for delivery with Node and PostgreSQL"
   You: REST API for delivery with Node and PostgreSQL

🤖 Agent: Great! Which frontend framework will you use?
   You: React with TypeScript

🤖 Agent: Perfect! Will you need authentication?
   You: Yes, JWT

... (2-3 more questions) ...

✅ Configuration generated successfully!

🦑 10 files generated at /home/user/delivery-api

Next steps:
  1. Tell your agent: "Access /home/user/delivery-api/readme-agent.md and follow the ritual"
  2. Review /home/user/delivery-api/doc/constitution.md
  3. Add tasks to /home/user/delivery-api/doc/kanban.md
```

---

## 📦 Installation

### Via pip (recommended)

```bash
pip install squidy
squidy --version
```

### Via pipx (isolated)

```bash
pipx install squidy
squidy --version
```

### Development

```bash
git clone https://github.com/seomarc/squidyrun.git
cd squidyrun
python -m venv venv && source venv/bin/activate  # Linux/Mac
# or: python -m venv venv && venv\Scripts\activate  # Windows
pip install -e ".[dev]"
squidy --version
```

**Requirements:** Python 3.9+

---

## 🎮 Usage

### Setup with AI (Recommended)

```bash
# Interactive setup with AI interview
squidy init

# Specify path
squidy init ./my-project

# Simulate without creating files (dry-run)
squidy init --dry-run

# Manual setup (without AI)
squidy init --manual

# Choose language (pt-BR or en-US)
squidy init --lang en-US
```

### 🌍 Supported Languages

Squidy v2.1+ supports multiple languages! All documentation and interface are generated in the selected language:

| Language | Code | Status |
|----------|------|--------|
| 🇧🇷 Portuguese (Brazil) | `pt-BR` | ✅ Complete |
| 🇺🇸 English (US) | `en-US` | ✅ Complete |

**How to use:**
```bash
# Select language via flag
squidy init --lang en-US

# Or let Squidy prompt you to choose
squidy init

# 🌍 Select your language:
# [1] 🇧🇷 Português (Brasil)
# [2] 🇺🇸 English (US)
```

📖 **[Complete Internationalization Guide](docs/I18N.md)**

**What is translated:**
- ✅ Complete CLI interface
- ✅ All 10 documentation templates
- ✅ AI interview prompts
- ✅ Audit and status messages

### Project Audit

```bash
# Audit current directory
squidy audit

# Audit specific project
squidy audit ./my-project

# JSON output
squidy audit -f json

# Apply automatic fixes
squidy audit --fix
```

### Quick Status

```bash
# Show project status
squidy status

# Complete diagnosis
squidy doctor
```

---

## 🏗️ What Does Squidy Create?

Squidy generates a complete governance structure:

```
my-project/
├── readme-agent.md          # 🤖 Complete guide for the AI agent
├── .squidy/
│   └── manifest.json        # 📋 Project manifest
├── doc/
│   ├── AGENT.md             # 🎯 Quick reference for the agent
│   ├── constitution.md      # ⚖️  Principles, prohibitions, DoD
│   ├── oracle.md            # 🧙 Architecture decisions (ADRs)
│   ├── policies.md          # 📋 Stack, conventions, policies
│   ├── kanban.md            # 📊 Task management (Epics → Tasks → Subtasks)
│   ├── emergency.md         # 🚨 Critical blocker registry
│   ├── diary-index.md       # 📑 History index
│   └── session-context.md   # 💾 Current state cache
└── diary/
    └── 2026-02.md           # 📅 Automatic decision log
```

### 📋 Kanban Structure

```markdown
## 🔥 EPICS
### EPIC-001: Authentication System
**Priority:** P0 | **Complexity:** M
**Tasks:** TASK-001, TASK-002

## 📋 BACKLOG
### TASK-001: Setup JWT [EPIC-001]
**Complexity:** S | **Priority:** P0
**Subtasks:**
- [ ] SUB-001: Install library (XS - 30min)
- [ ] SUB-002: Configure middleware (S - 1h)

## 🏗️ IN PROGRESS (WIP: 1/3)
- [ ] TASK-001: Setup JWT

## ✅ COMPLETED
- [x] TASK-000: Initial setup
```

---

## 🎨 Features

### ✨ v2.1 - New Features

- 🌍 **Multi-language** - Full support for Portuguese and English (pt-BR, en-US)
- 📋 **Bilingual Templates** - Documentation generated in selected language
- 🤖 **Multi-language AI** - Interview and configuration in Portuguese or English

### ✨ v2.0 - New Features

- 🎨 **Premium UI/UX** - Modern interface with Rich, gradients, and animations
- 🤖 **Smart Interview** - 5 structured phases with contextual follow-ups
- 📊 **Complete Audit** - Checks structure, kanban, freshness, and consistency
- 🔌 **Clean Architecture** - Ports & Adapters, extensible and testable
- 📋 **Templates v2.0** - More complete and actionable documentation
- 🧪 **Tests** - pytest suite, 10/10 passing

### 🤖 Supported AI Providers

| Provider | Models | Cost |
|----------|--------|------|
| **OpenAI** | GPT-4o-mini | Paid |
| **Anthropic** | Claude 3 Haiku/Sonnet | Paid |

### 🔍 Audit

Squidy can audit existing projects:

- ✅ **StructureChecker** - Checks required files
- ✅ **KanbanChecker** - Analyzes WIP limit, blocked tasks
- ✅ **FreshnessChecker** - Identifies outdated files
- ✅ **ConsistencyChecker** - Checks consistency between files

---

## 🛠️ Tech Stack

- **Python 3.9+** - Main language
- **Typer** - CLI framework
- **Rich** - UI components and formatting
- **Pydantic v2** - Data validation
- **Jinja2** - Templates
- **OpenAI / Anthropic** - AI providers

---

## 📚 Documentation

- 📖 [Complete Documentation](https://docs.squidy.run)
- 🌍 **[Internationalization Guide](docs/I18N.md)** - Multi-language (pt-BR, en-US)
- 🚀 [Quick Start Guide](https://docs.squidy.run/quickstart)
- 🏗️ [Architecture](https://docs.squidy.run/architecture)
- 🤝 [Contributing](CONTRIBUTING.md)
- 🌐 [Contributing with Translations](CONTRIBUTING-I18N.md)

---

## 🤝 Contributing

Contributions are welcome! Read our [Contributing Guide](CONTRIBUTING.md).

### Development

```bash
# Clone
git clone https://github.com/seomarc/squidyrun.git
cd squidyrun

# Setup
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"

# Tests
pytest

# Lint
black squidy/
isort squidy/
mypy squidy/

# Commit
pre-commit run --all-files
```

---

## 🔗 Links

<p align="center">
  <a href="https://squidy.run">🌐 Website</a> •
  <a href="https://pypi.org/project/squidy/">📦 PyPI</a> •
  <a href="https://github.com/seomarc/squidyrun">💻 GitHub</a> •
  <a href="https://www.youtube.com/@seomarcos">▶️ YouTube</a> •
  <a href="https://www.linkedin.com/in/seomarc/">💼 LinkedIn</a> •
  <a href="https://buymeacoffee.com/seomarcos">☕ Buy Me a Coffee</a>
</p>

### 👤 Developer

- **Marcos Tadeu** - [Personal Website](https://www.marcostadeu.com.br/)
- **SearchOps** - [searchops.io](https://searchops.io/)

---

## 💖 Support the Project

If Squidy helped you, consider:

- ⭐ Give a star on [GitHub](https://github.com/seomarc/squidyrun)
- 🐦 Share on Twitter
- 💼 Use it at your company
- 🤝 Contribute with code
- ☕ [Buy Me a Coffee](https://buymeacoffee.com/seomarcos)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with 🦑 by <a href="https://github.com/seomarc">Marcos Tadeu</a> • <a href="https://github.com/seomarc/squidyrun">💻 Project GitHub</a>
</p>

<p align="center">
  <a href="https://squidy.run">🌐 squidy.run</a> •
  <a href="https://pypi.org/project/squidy/">📦 PyPI</a> •
  <a href="https://github.com/seomarc/squidyrun">💻 GitHub</a> •
  <a href="https://www.youtube.com/@seomarcos">▶️ YouTube</a> •
  <a href="https://www.linkedin.com/in/seomarc/">💼 LinkedIn</a> •
  <a href="https://www.marcostadeu.com.br/">👤 Developer</a> •
  <a href="https://searchops.io/">🏢 SearchOps</a> •
  <a href="mailto:contato@squidy.run">✉️ Contact</a>
</p>
