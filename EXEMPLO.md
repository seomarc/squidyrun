# 🦑 Exemplo de Uso do Squidy

Este documento mostra exemplos práticos de uso do Squidy v2.0.

---

## 🚀 Exemplo 1: Setup com IA (OpenAI)

```bash
# Instala o Squidy
pip install squidy

# Inicializa projeto com IA
squidy init ./meu-app
```

### Diálogo Esperado:

```
🦑 Setup com Agente IA

Como funciona:
  1. Me conte sobre o projeto (uma frase é suficiente)
  2. Farei até 6 perguntas contextuais
  3. Gero automaticamente 10 arquivos de documentação

🔐 Digite a API key para openai:
(a chave não aparece enquanto digita)

> sk-... (sua chave)

✓ Conectado ao OpenAI

🤖 Agente: Olá! Me conte sobre o projeto que você quer configurar.
           Exemplo: "API REST para delivery com Node e PostgreSQL"
   Você: API REST para delivery com Node e PostgreSQL

🤖 Agente: Legal! Qual framework frontend você vai usar?
   Você: React com TypeScript

🤖 Agente: Perfeito! Vai precisar de autenticação?
   Você: Sim, JWT

🤖 Agente: Ótimo! Para autenticação JWT, você prefere usar uma 
           biblioteca específica ou deixar a IA sugerir?
   Você: Deixa a IA sugerir

🤖 Agente: Entendido! Qual o prazo estimado para o MVP?
   Você: 2 semanas

✓ Contexto suficiente coletado (5 perguntas)

Gerando configuração...

✅ Setup concluído!

Arquivos gerados em: /home/user/meu-app

Próximos passos:
  1. Diga ao seu agente: "Acesse /home/user/meu-app/readme-agent.md e siga o ritual"
  2. Revise /home/user/meu-app/doc/constituicao.md
  3. Adicione tarefas em /home/user/meu-app/doc/kanban.md
```

---

## 📝 Exemplo 2: Setup Manual (Sem IA)

```bash
squidy init ./meu-app --manual
```

```
📝 Setup Manual

Nome do projeto (kebab-case): meu-app
Nome apresentável: Meu App
Propósito do projeto (1-2 frases): Aplicativo de delivery para restaurantes locais

Stack Tecnológica:
Frontend [React]: React
Backend [Node.js/Express]: Node.js/Express
Banco de dados [PostgreSQL]: PostgreSQL

Tipo de agente [desenvolvedor-fullstack]: desenvolvedor-fullstack

✅ Setup concluído!
```

---

## 🔍 Exemplo 3: Auditoria de Projeto

```bash
cd meu-app
squidy audit
```

```
🔍 Auditando: /home/user/meu-app

Resumo da Auditoria:

┌─────────────┬───────────┐
│ Severidade  │ Quantidade│
├─────────────┼───────────┤
│ 🟡 Médio    │ 2         │
│ 🟢 Baixo    │ 1         │
│ Total       │ 3         │
└─────────────┴───────────┘

Problemas Encontrados:

┌────────────────────────────────────────────────────────────────┐
│ 🟡 KanbanChecker                                                │
├────────────────────────────────────────────────────────────────┤
│ Kanban desatualizado (última atualização há 12 dias)            │
│                                                                 │
│ Arquivo: doc/kanban.md                                          │
│ Sugestão: Atualize o kanban com o progresso atual               │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ 🟡 FreshnessChecker                                             │
├────────────────────────────────────────────────────────────────┤
│ Contexto de sessão desatualizado (última atualização há 10 dias)│
│                                                                 │
│ Arquivo: doc/contexto-sessao.md                                 │
│ Sugestão: Atualize o contexto ao final de cada sessão           │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ 🟢 KanbanChecker                                                │
├────────────────────────────────────────────────────────────────┤
│ Backlog vazio - adicione tarefas futuras                        │
│                                                                 │
│ Arquivo: doc/kanban.md                                          │
│ Sugestão: Adicione tarefas planejadas ao backlog                │
└────────────────────────────────────────────────────────────────┘

Checkers executados: StructureChecker, KanbanChecker, FreshnessChecker, ConsistencyChecker
Duração: 45ms
```

---

## 📊 Exemplo 4: Status Rápido

```bash
squidy status
```

```
📊 Status do Projeto

┌────────────────────────────────────────────────────────────────┐
│ 🦑 Squidy Project                                               │
├────────────────────────────────────────────────────────────────┤
│ ✅ Estrutura completa                                           │
│                                                                 │
│ Caminho: /home/user/meu-app                                     │
│ Arquivos OK: 7/7                                                │
└────────────────────────────────────────────────────────────────┘

┌────────────────────┬────────┐
│ Arquivo            │ Status │
├────────────────────┼────────┤
│ readme-agent.md    │ ✓      │
│ doc/               │ ✓      │
│ doc/constituicao.md│ ✓      │
│ doc/kanban.md      │ ✓      │
│ doc/oraculo.md     │ ✓      │
│ doc/AGENT.md       │ ✓      │
│ diario/            │ ✓      │
└────────────────────┴────────┘
```

---

## 📋 Exemplo 5: Estrutura Gerada

```
meu-app/
├── readme-agent.md          # 🤖 Guia completo para o agente
├── doc/
│   ├── AGENT.md             # 🎯 Referência rápida
│   ├── constituicao.md      # ⚖️  Princípios e proibições
│   ├── oraculo.md           # 🧙 Decisões de arquitetura
│   ├── politicas.md         # 📋 Stack e convenções
│   ├── kanban.md            # 📊 Gestão de tarefas
│   ├── emergencia.md        # 🚨 Registro de bloqueios
│   ├── indice-diario.md     # 📑 Índice do histórico
│   └── contexto-sessao.md   # 💾 Cache do estado atual
└── diario/
    └── 2026-02.md           # 📅 Log de decisões
```

---

## 🎯 Exemplo 6: Como Usar com Claude/Cursor

Após rodar `squidy init`:

### No Claude/Cursor, digite:

```
Acesse /home/user/meu-app/readme-agent.md e siga o ritual de inicialização
```

### O agente vai responder:

```
✅ Agente inicializado para Meu App
📅 2026-02-21 14:30:00
🎯 Modo: desenvolvedor-fullstack

Executando leitura obrigatória...
✓ doc/constituicao.md - Princípios e proibições
✓ doc/oraculo.md - Decisões de arquitetura
✓ doc/emergencia.md - Nenhum bloqueio ativo
✓ doc/kanban.md - TASK-001 disponível
✓ doc/contexto-sessao.md - Estado atual carregado

Registrando no diário...
✓ Entrada criada em diario/2026-02.md

🎯 Pronto para trabalhar!

Próxima ação: TASK-001 - Setup JWT
O que você gostaria que eu fizesse?
```

---

## 🔧 Exemplo 7: Auditoria com Correção Automática

```bash
squidy audit --fix
```

```
🔍 Auditando: /home/user/meu-app

✅ Correções aplicadas:
  ✓ Criado arquivo faltante: doc/emergencia.md
  ✓ Criado arquivo faltante: doc/indice-diario.md

⚠️  Problemas que precisam de atenção manual:
  🟡 Kanban desatualizado
  🟡 Contexto de sessão desatualizado
```

---

## 📈 Exemplo 8: Exportar Auditoria

```bash
# JSON
squidy audit -f json > auditoria.json

# Markdown
squidy audit -f markdown > auditoria.md
```

---

## 💡 Dicas

### 1. Dry Run

```bash
# Veja o que seria criado antes de criar
squidy init --dry-run
```

### 2. Apenas Arquivos Faltantes

```bash
# Cria apenas arquivos que não existem
squidy init --only-missing
```

### 3. Checkers Específicos

```bash
# Audit apenas estrutura e kanban
squidy audit -c structure,kanban
```

### 4. Provedor Diferente

```bash
# Usar Anthropic (Claude)
squidy init --provider anthropic

# Usar OpenRouter (modelos gratuitos)
squidy init --provider openrouter
```

---

## 🎓 Fluxo de Trabalho Completo

```bash
# 1. Cria projeto
mkdir meu-app && cd meu-app

# 2. Inicializa com Squidy
squidy init

# 3. Abre no VS Code com Cursor/Claude
code .

# 4. Diga ao agente para seguir o ritual
# "Acesse readme-agent.md e siga o ritual"

# 5. Desenvolve com o agente

# 6. Ao final da sessão, atualiza contexto
# (O agente faz isso automaticamente)

# 7. Audita periodicamente
squidy audit

# 8. Repete!
```

---

## 📚 Recursos

- [Documentação Completa](https://docs.squidy.run)
- [README Principal](README.md)
- [Guia de Contribuição](CONTRIBUTING.md)

---

**Dúvidas?** Abra uma issue no GitHub ou entre em contato!
