"""
Template Engine

Motor de templates usando Jinja2 para gerar arquivos de documentação.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import BaseLoader, Environment, TemplateNotFound


class TemplateLoader(BaseLoader):
    """
    Loader de templates em memória
    
    Carrega templates de strings (não de arquivos).
    """
    
    def __init__(self, templates: dict[str, str]):
        self.templates = templates
    
    def get_source(self, environment, template):
        if template in self.templates:
            source = self.templates[template]
            return source, None, lambda: True
        raise TemplateNotFound(template)


class TemplateEngine:
    """
    Motor de templates para geração de arquivos
    
    Usa Jinja2 com templates embutidos.
    Suporta múltiplos idiomas (pt-BR, en-US).
    
    Example:
        >>> engine = TemplateEngine()
        >>> content = engine.render("readme-agent.md", language="en-US", config={...})
    """
    
    # Idioma padrão
    DEFAULT_LANGUAGE = "pt-BR"
    
    def __init__(self):
        # Templates por idioma
        self._templates_pt = self._get_templates_pt()
        self._templates_en = self._get_templates_en()
        
        # Carregadores por idioma
        self._loaders = {
            "pt-BR": TemplateLoader(self._templates_pt),
            "en-US": TemplateLoader(self._templates_en),
        }
        
        # Environments por idioma
        self._envs = {}
        for lang, loader in self._loaders.items():
            self._envs[lang] = Environment(
                loader=loader,
                trim_blocks=True,
                lstrip_blocks=True,
            )
            # Filtros customizados
            self._envs[lang].filters["kebab_case"] = self._kebab_case
            self._envs[lang].filters["pascal_case"] = self._pascal_case
            self._envs[lang].filters["snake_case"] = self._snake_case
    
    def render(self, template_name: str, language: str = "pt-BR", **kwargs) -> str:
        """
        Renderiza um template
        
        Args:
            template_name: Nome do template
            language: Idioma do template (pt-BR, en-US)
            **kwargs: Variáveis para o template
            
        Returns:
            Conteúdo renderizado
        """
        # Fallback para pt-BR se idioma não suportado
        if language not in self._envs:
            language = self.DEFAULT_LANGUAGE
        
        env = self._envs[language]
        template = env.get_template(template_name)
        
        # Adiciona variáveis padrão
        context = {
            "now": datetime.now(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "month": datetime.now().strftime("%Y-%m"),
            "language": language,
        }
        context.update(kwargs)
        
        return template.render(**context)
    
    def list_templates(self) -> list[str]:
        """Lista templates disponíveis"""
        return list(self.loader.templates.keys())
    
    def _kebab_case(self, value: str) -> str:
        """Converte para kebab-case"""
        return value.lower().replace(" ", "-").replace("_", "-")
    
    def _pascal_case(self, value: str) -> str:
        """Converte para PascalCase"""
        return "".join(word.capitalize() for word in value.replace("-", " ").replace("_", " ").split())
    
    def _snake_case(self, value: str) -> str:
        """Converte para snake_case"""
        return value.lower().replace(" ", "_").replace("-", "_")
    
    def _get_templates_pt(self) -> dict[str, str]:
        """Retorna dicionário de templates em Português"""
        return {
            "readme-agent.md": self._readme_agent_template(),
            "constituicao.md": self._constituicao_template(),
            "kanban.md": self._kanban_template(),
            "oraculo.md": self._oraculo_template(),
            "politicas.md": self._politicas_template(),
            "emergencia.md": self._emergencia_template(),
            "indice-diario.md": self._indice_diario_template(),
            "contexto-sessao.md": self._contexto_sessao_template(),
            "AGENT.md": self._agent_template(),
            "diario.md": self._diario_template(),
        }
    
    def _get_templates_en(self) -> dict[str, str]:
        """Retorna dicionário de templates em Inglês"""
        return {
            "readme-agent.md": self._readme_agent_template_en(),
            "constituicao.md": self._constitution_template_en(),
            "kanban.md": self._kanban_template_en(),
            "oraculo.md": self._oracle_template_en(),
            "politicas.md": self._policies_template_en(),
            "emergencia.md": self._emergency_template_en(),
            "indice-diario.md": self._diary_index_template_en(),
            "contexto-sessao.md": self._session_context_template_en(),
            "AGENT.md": self._agent_template_en(),
            "diario.md": self._diary_template_en(),
        }
    
    def _readme_agent_template(self) -> str:
        """Template readme-agent.md v2.0"""
        return '''# 👋 Bem-vindo! - {{ display_name }}

> **🤖 Para o Agente de IA:** Este é seu guia completo. Leia atentamente antes de começar.

---

## 🎯 Ritual de Inicialização

Antes de qualquer ação, você DEVE:

### 1️⃣ Confirmar Inicialização
Responda exatamente:
```
✅ Agente inicializado para {{ display_name }}
📅 {{ timestamp }}
🎯 Modo: {{ agent_type }}
```

### 2️⃣ Executar Leitura Obrigatória
Leia NA ORDEM:
1. `doc/constituicao.md` - Princípios e proibições
2. `doc/oraculo.md` - Decisões de arquitetura
3. `doc/emergencia.md` - Bloqueios ativos
4. `doc/kanban.md` - Tarefas disponíveis
5. `doc/contexto-sessao.md` - Estado atual

### 3️⃣ Preencher o Kanban Inicial
> ⚠️ **Faça isso apenas se o `doc/kanban.md` ainda contiver placeholders (ex: `[Nome do Épico]`).**

Com base na `doc/constituicao.md` que você acabou de ler, popule o `doc/kanban.md` com as tarefas reais do projeto:

**a) Identifique os Épicos**
Quebre o propósito do projeto em 3-6 grandes funcionalidades. Cada uma vira um ÉPICO.
```
ÉPICO-001: [Funcionalidade central 1]
ÉPICO-002: [Funcionalidade central 2]
...
```

**b) Crie as Tasks do Backlog**
Para cada Épico, crie 2-5 tasks concretas e acionáveis:
```
TASK-001: [Ação específica] [ÉPICO-001]  → Complexidade M, Prioridade P0
TASK-002: [Ação específica] [ÉPICO-001]  → Complexidade S, Prioridade P1
...
```

**c) Regras ao preencher**
- Use verbos no infinitivo: "Implementar", "Criar", "Configurar", "Integrar"
- Mantenha tasks com escopo de 1-8h (use XL apenas se inevitável)
- Defina critérios de aceitação claros e verificáveis
- Priorize as tasks de infraestrutura/setup como P0

**d) Atualize o Próximo ID**
Após criar todas as tasks, atualize o campo `**Próximo ID:**` no topo do kanban.

### 4️⃣ Registrar no Diário
Crie entrada em `diario/{{ month }}.md`:
```markdown
### [{{ now.strftime("%H:%M") }}] BOOT - Agente iniciado
**Contexto:** [Resumo do contexto-sessao.md]
**Kanban:** [Quantos épicos/tasks foram criados ou já existiam]
**Tarefa alvo:** TASK-XXX
**Estado encontrado:** [O que está em progresso/bloqueado]
```

---

## 📋 Contexto do Projeto

**Nome:** {{ display_name }}  
**Tipo:** {{ agent_type }}  
**Gerado:** {{ timestamp }}

### 🎯 Missão
{{ proposito }}

### 🛠️ Stack Tecnológica
- **Frontend:** {{ stack.frontend }}
- **Backend:** {{ stack.backend }}
- **Banco de Dados:** {{ stack.banco }}

### 📜 Princípios (SEMPRE seguir)
{% for principio in principios %}
- {{ principio }}
{% endfor %}

### 🚫 Proibições (NUNCA fazer)
{% for proibicao in proibicoes %}
- {{ proibicao }}
{% endfor %}

### ✅ Definition of Done
{% for criterio in dod %}
- [ ] {{ criterio }}
{% endfor %}

---

## 📊 Como Trabalhar com o Kanban

### Hierarquia de Tarefas

```
ÉPICO (Grande funcionalidade)
└── TASK (Unidade de trabalho)
    └── SUBTAREFA (Passo específico)
```

### Fluxo de Trabalho

1. **ESCOLHER** tarefa do BACKLOG
2. **MOVER** para EM PROGRESSO (atualize kanban.md)
3. **CRIAR** subtarefas se necessário
4. **COMMITAR** com referência: `feat(auth): add login [TASK-001]`
5. **ATUALIZAR** contexto-sessao.md ao final
6. **MOVER** para CONCLUÍDO quando pronto

### Regras de Ouro
- ✅ Sempre vincule trabalho a TASK-ID
- ✅ Atualize kanban ANTES de começar
- ✅ Crie subtarefas para trabalho > 2h
- ✅ Referencie task no commit

---

## 🚨 Regras de Ouro

1. **NUNCA** programe antes de ler a Constituição
2. **NUNCA** ignore `emergencia.md`
3. **SEMPRE** vincule a TASK-ID
4. **SEMPRE** atualize `contexto-sessao.md`
5. **SEMPRE** registre no diário

---

## 🆘 Em Caso de Dúvida

| Dúvida sobre | Consulte |
|--------------|----------|
| Arquitetura | `doc/oraculo.md` |
| Regras | `doc/constituicao.md` |
| Convenções | `doc/politicas.md` |
| Tarefas | `doc/kanban.md` |
| Bloqueios | `doc/emergencia.md` |

**Se ainda tiver dúvida:** Registre em `emergencia.md` ANTES de prosseguir.

---

*Gerado com 🦑 Squidy v{{ version }} em {{ timestamp }}*
'''
    
    def _constituicao_template(self) -> str:
        """Template constituicao.md v2.0"""
        return '''# CONSTITUIÇÃO - {{ display_name }}

**Gerado em:** {{ timestamp }}  
**Tipo de Agente:** {{ agent_type }}

---

## §1 - PROPÓSITO (Por que este projeto existe?)

{{ proposito }}

{% if contexto_negocio %}
### Contexto de Negócio
- **Problema:** {{ contexto_negocio.problema }}
- **Usuários Alvo:** {{ contexto_negocio.usuarios_alvo }}
- **Valor Principal:** {{ contexto_negocio.valor_principal }}
{% endif %}

---

## §2 - PRINCÍPIOS (O que SEMPRE fazer)

{% for principio in principios %}
### {{ loop.index }}. {{ principio }}

**✅ FAZER:**
- [Ação específica relacionada]

**❌ EVITAR:**
- [Anti-padrão comum]

{% endfor %}

---

## §3 - PROIBIÇÕES (O que NUNCA fazer)

{% for proibicao in proibicoes %}
### {{ loop.index }}. {{ proibicao }}

**Por quê:** [Explicação do risco]  
**Consequência:** [O que acontece se quebrar]  
**Como detectar:** [Como identificar]  
**Exceção:** [Quando pode quebrar, se aplicável]

{% endfor %}

---

## §4 - CONVENÇÕES

### Nomenclatura

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Variáveis | {{ convencoes.variaveis }} | `{% if convencoes.variaveis == "camelCase" %}usuarioAtual{% else %}usuario_atual{% endif %}` |
| Funções | {{ convencoes.funcoes }} | `{% if convencoes.funcoes == "camelCase" %}calcularTotal{% else %}calcular_total{% endif %}()` |
| Classes | {{ convencoes.classes }} | `{% if convencoes.classes == "PascalCase" %}UsuarioService{% else %}usuario_service{% endif %}` |
| Constantes | {{ convencoes.constantes }} | `{% if convencoes.constantes == "UPPER_SNAKE" %}MAX_TENTATIVAS{% else %}max_tentativas{% endif %}` |
| Arquivos | {{ convencoes.arquivos }} | `{% if convencoes.arquivos == "kebab-case" %}usuario-service{% else %}usuario_service{% endif %}.js` |
| Banco | {{ convencoes.banco }} | `{% if convencoes.banco == "snake_case" %}usuario_id{% else %}usuarioId{% endif %}` |

### Commits (Conventional Commits)

```
tipo(escopo): descrição curta

[corpo opcional]

[rodapé opcional]
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `test`: Testes
- `refactor`: Refatoração
- `chore`: Tarefas diversas

---

## §5 - DEFINITION OF DONE

{% for criterio in dod %}
- [ ] {{ criterio }}
{% endfor %}

---

## §6 - STACK TECNOLÓGICA

- **Frontend:** {{ stack.frontend }}
- **Backend:** {{ stack.backend }}
- **Banco de Dados:** {{ stack.banco }}

{% if arquitetura %}
### Arquitetura
- **Padrão:** {{ arquitetura.padrao }}
- **Camadas:** {{ arquitetura.camadas | join(", ") }}
{% if arquitetura.integracoes %}
- **Integrações:** {{ arquitetura.integracoes | join(", ") }}
{% endif %}
{% endif %}

{% if qualidade %}
### Qualidade
- **Cobertura de Testes:** {{ qualidade.cobertura_testes }}
- **Ferramentas:** {{ qualidade.ferramentas | join(", ") }}
- **CI/CD:** {{ "Sim" if qualidade.ci_cd else "Não" }}
{% endif %}

---

*Gerado automaticamente pelo 🦑 Squidy v{{ version }}*
'''
    
    def _kanban_template(self) -> str:
        """Template kanban.md v2.0"""
        return '''# KANBAN - {{ display_name }}

**Gerado em:** {{ timestamp }}
**Próximo ID:** TASK-001

---

> ## 🤖 INSTRUÇÃO PARA O AGENTE — SETUP INICIAL
>
> **Este arquivo foi gerado com placeholders.** Na primeira sessão do projeto, você deve substituí-los por tarefas reais antes de qualquer desenvolvimento.
>
> ### Como preencher:
> 1. **Leia `doc/constituicao.md`** para entender o propósito e escopo do projeto
> 2. **Identifique 3-6 Épicos** — grandes funcionalidades que compõem o produto
> 3. **Para cada Épico, crie 2-5 Tasks** no BACKLOG com:
>    - Nome em verbo no infinitivo (`Implementar`, `Configurar`, `Criar`...)
>    - Complexidade realista (XS/S/M/L — evite XL)
>    - Critérios de aceitação verificáveis
>    - Prioridade (P0 = bloqueia release, P1 = importante, P2 = desejável)
> 4. **Remova os placeholders** (`[Nome do Épico]`, `[Nome da Task]`, etc.)
> 5. **Atualize o campo `Próximo ID`** no cabeçalho deste arquivo
>
> ⚠️ **Não comece a desenvolver antes de preencher o kanban.**

---

## 📋 GUIA RÁPIDO

### Hierarquia
- **ÉPICO** → Funcionalidade grande (ex: "Sistema de Auth")
- **TASK** → Unidade de trabalho (ex: "Login com JWT")
- **SUBTAREFA** → Passo específico (ex: "Criar endpoint")

### Prioridades
- **P0** → Crítico (bloqueia release)
- **P1** → Alto (importante)
- **P2** → Médio (desejável)
- **P3** → Baixo (nice to have)

### Complexidade
- **XS** → < 1h
- **S** → 1-2h
- **M** → 2-4h
- **L** → 4-8h
- **XL** → > 8h (quebrar em tasks menores)

---

## 🔥 ÉPICOS

### ÉPICO-001: [Nome do Épico]
**Descrição:** [Descrição curta]  
**Prioridade:** P0  
**Complexidade:** M  
**Critérios de Aceitação:**
- [ ] Critério 1
- [ ] Critério 2

**Tasks Relacionadas:**
- [ ] TASK-001
- [ ] TASK-002

---

## 📋 BACKLOG

### TASK-001: [Nome da Task] [ÉPICO-001]
**Complexidade:** M  
**Prioridade:** P0  
**Tempo Estimado:** 4h  
**Descrição:** [Descrição detalhada]

**Critérios de Aceitação:**
- [ ] Critério 1
- [ ] Critério 2

**Subtarefas:**
- [ ] SUB-001: [Descrição] (XS - 30min)
- [ ] SUB-002: [Descrição] (S - 1h)

**Notas:**
- [Informações adicionais]

---

## 🏗️ EM PROGRESSO (WIP: 0/3)

*[Mover tasks do BACKLOG para cá antes de começar]*

---

## ✅ CONCLUÍDO

- [x] **TASK-000** Setup inicial do projeto Squidy
  - **Concluído em:** {{ timestamp }}
  - **Agente:** Squidy Setup
  - **Notas:** Estrutura inicial gerada automaticamente

---

## ⏸️ BLOQUEADO

*[Registrar bloqueios com motivo e data]*

---

## 📊 MÉTRICAS

- **WIP:** 0/3 (limite: 3 tarefas simultâneas)
- **Velocidade:** Calculando...
- **Taxa de Conclusão:** Calculando...
- **Bloqueios:** 0
- **Próximo ID:** TASK-001

---

*Mantenha este kanban atualizado - mova tarefas conforme progresso*
'''
    
    def _oraculo_template(self) -> str:
        """Template oraculo.md"""
        return '''# ORÁCULO - Decisões de Arquitetura (ADRs)

**Projeto:** {{ display_name }}  
**Gerado em:** {{ timestamp }}

---

## ADR-001: Stack Técnica Principal

**Data:** {{ date }}  
**Status:** Aceito  
**Contexto:** Definição da stack tecnológica baseada nos requisitos do projeto.

**Decisão:**
- **Frontend:** {{ stack.frontend }}
- **Backend:** {{ stack.backend }}
- **Banco de Dados:** {{ stack.banco }}

**Consequências:**
- ✅ Stack alinhada com requisitos do projeto
- ✅ Ferramentas e bibliotecas bem estabelecidas
- ⚠️ Equipe precisa de conhecimento nas tecnologias escolhidas

{% if arquitetura %}
### Detalhes da Arquitetura
- **Padrão:** {{ arquitetura.padrao }}
- **Camadas:** {{ arquitetura.camadas | join(", ") }}
{% if arquitetura.integracoes %}
- **Integrações:** {{ arquitetura.integracoes | join(", ") }}
{% endif %}
{% endif %}

---

## ADR-002: Restrições Técnicas

**Data:** {{ date }}  
**Status:** Aceito

**Restrições identificadas:**
{% for restricao in restricoes %}
- {{ restricao }}
{% else %}
- Nenhuma restrição técnica específica definida
{% endfor %}

**Consequências:**
- ✅ Requisitos não-funcionais documentados
- ⚠️ Podem impactar escolhas de implementação futuras

---

## ADR-003: Convenções de Código

**Data:** {{ date }}  
**Status:** Aceito

**Decisão:** Adotar as seguintes convenções:

| Elemento | Convenção |
|----------|-----------|
| Variáveis | {{ convencoes.variaveis }} |
| Funções | {{ convencoes.funcoes }} |
| Classes | {{ convencoes.classes }} |
| Constantes | {{ convencoes.constantes }} |
| Arquivos | {{ convencoes.arquivos }} |
| Banco | {{ convencoes.banco }} |

**Motivação:** Manter consistência e legibilidade do código.

---

*Adicione novos ADRs conforme decisões importantes forem tomadas*
'''
    
    def _politicas_template(self) -> str:
        """Template politicas.md"""
        return '''# POLÍTICAS - {{ display_name }}

**Gerado em:** {{ timestamp }}

---

## 🔧 Políticas de Desenvolvimento

### Commits e Versionamento

- **Convenção:** Conventional Commits (feat:, fix:, docs:, etc)
- **Branches:**
  - `main` → Produção
  - `develop` → Desenvolvimento
  - `feature/*` → Funcionalidades
  - `hotfix/*` → Correções urgentes
- **Pull Requests:** Obrigatórios para merge em `main`

### Code Review

- **Mínimo de aprovações:** 1 revisor
- **Checklist de Review:**
  - [ ] Código segue padrões do projeto
  - [ ] Testes adequados incluídos
  - [ ] Documentação atualizada
  - [ ] Sem credenciais ou secrets hardcoded

### Testes

{% if qualidade %}
- **Cobertura mínima:** {{ qualidade.cobertura_testes }}
- **Ferramentas:** {{ qualidade.ferramentas | join(", ") }}
{% else %}
- **Cobertura mínima:** 70%
- **Tipos:** Unitários (obrigatórios), Integração (quando aplicável)
{% endif %}
- **CI/CD:** Testes devem passar antes de merge

---

## 📦 Políticas de Deploy

### Ambientes

- **Development:** Deploy automático de `develop`
- **Staging:** Deploy manual para validação
- **Production:** Deploy após aprovação e testes em staging

### Rollback

- Manter última versão funcional sempre deployável
- Procedure de rollback documentado
- Feature flags para funcionalidades críticas

---

## 🔒 Políticas de Segurança

### Credenciais

- ❌ NUNCA commitar API keys, tokens, passwords
- ✅ Usar variáveis de ambiente ou secret managers
- ✅ Rotacionar secrets regularmente
- ✅ Usar `.env.example` sem valores reais

### Dependências

- Revisar dependências antes de adicionar
- Manter dependências atualizadas (security patches)
- Usar ferramentas de scan de vulnerabilidades (Dependabot, Snyk)

### Código

- Validar inputs em todas as APIs
- Usar prepared statements para SQL
- Escapar outputs em templates
- Implementar rate limiting

---

*Políticas podem ser ajustadas conforme o projeto evolui*
'''
    
    def _emergencia_template(self) -> str:
        """Template emergencia.md"""
        return '''# EMERGÊNCIA - {{ display_name }}

**Última atualização:** {{ timestamp }}

---

## 🚨 Bloqueios Ativos

*Nenhum bloqueio registrado no momento*

---

## 📋 Template de Registro de Bloqueio

### BLOCK-XXX: [Título do bloqueio]

**Data:** YYYY-MM-DD HH:MM  
**Severidade:** 🔴 Crítico | 🟡 Importante | 🟢 Baixa  
**Impacto:** Qual tarefa/funcionalidade está bloqueada?

**Descrição:**
Detalhe o problema encontrado.

**Tentativas de Resolução:**
1. O que já foi tentado?
2. Por que não funcionou?

**Contexto Adicional:**
- Logs relevantes
- Mensagens de erro
- Configurações envolvidas

**Resolução:**
*A ser preenchido quando resolvido*

---

## 📚 Bloqueios Resolvidos

### BLOCK-000: Exemplo de bloqueio resolvido

**Data:** {{ timestamp }}  
**Severidade:** 🟢 Baixa  
**Resolução:** Este é apenas um exemplo para ilustrar o formato

---

*Use este arquivo apenas para bloqueios que impedem progresso - não para bugs comuns*
'''
    
    def _indice_diario_template(self) -> str:
        """Template indice-diario.md"""
        return '''# ÍNDICE DO DIÁRIO - {{ display_name }}

---

## 📅 Arquivos de Diário

### {{ now.strftime("%Y") }}

- [{{ month }}.md](../diario/{{ month }}.md) - Ativo

---

## 🔍 Busca Rápida

### Por Tipo de Entrada

- **Decisões importantes:** Busque por "DECISÃO:" no diário
- **Problemas resolvidos:** Busque por "RESOLVIDO:"
- **Bloqueios:** Veja `emergencia.md`
- **Refatorações:** Busque por "REFACTOR:"

### Por Tarefa

- **TASK-XXX:** Use o ID da tarefa como palavra-chave
- **ÉPICO-XXX:** Busque pelo ID do épico

---

## 📝 Como Registrar no Diário

### Formato Padrão

```markdown
### [HH:MM] TASK-XXX - Título curto

**Contexto:** [O que estava fazendo]

**Ação:** [O que foi feito]

**Resultado:** [O que aconteceu]

**Próximos passos:** [O que falta fazer]

**Notas:** [Informações adicionais]
```

### Exemplos

```markdown
### [14:30] TASK-001 - Setup JWT

**Contexto:** Iniciando implementação de autenticação

**Ação:** Instalei biblioteca jsonwebtoken e configurei middleware

**Resultado:** Middleware criado e testado localmente

**Próximos passos:** Criar endpoint /login

**Notas:** Usar algoritmo RS256 em produção
```

---

*Este índice é atualizado automaticamente conforme novos arquivos são criados*
'''
    
    def _contexto_sessao_template(self) -> str:
        """Template contexto-sessao.md"""
        return '''# CONTEXTO DE SESSÃO - {{ display_name }}

**Gerado em:** {{ timestamp }}  
**Agente:** setup-squidy-ai  
**Tarefa Atual:** TASK-001  
**Fase:** Planejamento/Setup Inicial

---

## 📊 Estado Atual (Resumo Executivo)

Projeto "{{ display_name }}" foi configurado com sucesso usando o Squidy Setup AI.

**Stack Técnica:**
- Frontend: {{ stack.frontend }}
- Backend: {{ stack.backend }}
- Banco: {{ stack.banco }}

**Bloqueios:** Nenhum  
**Dependências:** Conforme stack escolhida

---

## 📚 Referências Rápidas

- **Constituição:** Revisar propósito e princípios antes de começar
- **Oráculo:** ADR-001 define stack técnica
- **Políticas:** Seguir convenções de commit e code review
- **Kanban:** TASK-001 disponível para início

---

## 🧠 Memória de Curto Prazo

1. Projeto configurado automaticamente via entrevista AI
2. Estrutura Squidy completa gerada
3. Pronto para desenvolvimento começar

---

## ⚠️ Alertas Ativos

🔔 **LEMBRETE:** Revisar e ajustar configurações conforme necessidade  
🔔 **ATENÇÃO:** Adicionar primeira tarefa real ao kanban (substituir TASK-001)

---

## 🎯 Próxima Ação Esperada

Revisar estrutura e começar desenvolvimento da TASK-001

---

*Atualize este arquivo ao final de cada sessão de trabalho*
'''
    
    def _agent_template(self) -> str:
        """Template AGENT.md (referência rápida)"""
        return '''# AGENT - Referência Rápida

**Projeto:** {{ display_name }}  
**Tipo:** {{ agent_type }}  
**Gerado:** {{ timestamp }}

---

## 🎯 Quem Você É

{{ agent_type.replace("-", " ").title() }} responsável por {{ display_name }}

## 🎯 Missão

{{ proposito }}

---

## 📜 Regras (SEMPRE seguir)

{% for principio in principios %}
- {{ principio }}
{% endfor %}

---

## 🚫 Proibições (NUNCA fazer)

{% for proibicao in proibicoes %}
- {{ proibicao }}
{% endfor %}

---

## ✅ Definition of Done

{% for criterio in dod %}
- [ ] {{ criterio }}
{% endfor %}

---

## 🛠️ Stack

- **Frontend:** {{ stack.frontend }}
- **Backend:** {{ stack.backend }}
- **Banco:** {{ stack.banco }}

---

## 🧭 Navegação Rápida

| Arquivo | Conteúdo |
|---------|----------|
| `constituicao.md` | Princípios e proibições completos |
| `oraculo.md` | Decisões arquiteturais (ADRs) |
| `politicas.md` | Convenções de código e deploy |
| `kanban.md` | Tarefas em aberto |
| `emergencia.md` | Bloqueios críticos |
| `contexto-sessao.md` | Estado atual do projeto |

---

*Para inicialização completa, leia `../readme-agent.md` na raiz*
'''
    
    def _diario_template(self) -> str:
        """Template diário mensal"""
        return '''# DIÁRIO - {{ display_name }} - {{ month }}

---

## {{ date }}

### Setup Inicial do Projeto

**Timestamp:** {{ timestamp }}  
**Agente:** squidy-setup-ai  
**Ação:** Geração automática da estrutura Squidy v2.0  
**Contexto:** Projeto configurado via entrevista interativa com IA

**Decisões tomadas:**
- Stack técnica definida: {{ stack.frontend }} + {{ stack.backend }} + {{ stack.banco }}
- Tipo de agente: {{ agent_type }}
- Propósito documentado na Constituição
- {{ principios | length }} princípios definidos
- {{ proibicoes | length }} proibições estabelecidas

**Próximos passos:**
1. Revisar arquivos gerados (especialmente `constituicao.md`)
2. Ajustar `kanban.md` com tarefas reais do projeto
3. Configurar ambiente de desenvolvimento
4. Começar TASK-001

---

*Formato: ### [HH:MM] TASK-XXX - Descrição*
'''

    
    # =========================================================================
    # ENGLISH TEMPLATES (v2.0)
    # =========================================================================
    
    def _readme_agent_template_en(self) -> str:
        """Template readme-agent.md v2.0 - English"""
        return '''# 👋 Welcome! - {{ display_name }}

> **🤖 For the AI Agent:** This is your complete guide. Read carefully before starting.

---

## 🎯 Initialization Ritual

Before any action, you MUST:

### 1️⃣ Confirm Initialization
Respond exactly:
```
✅ Agent initialized for {{ display_name }}
📅 {{ timestamp }}
🎯 Mode: {{ agent_type }}
```

### 2️⃣ Execute Required Reading
Read IN ORDER:
1. `doc/constitution.md` - Principles and prohibitions
2. `doc/oracle.md` - Architecture decisions
3. `doc/emergency.md` - Active blockers
4. `doc/kanban.md` - Available tasks
5. `doc/session-context.md` - Current state

### 3️⃣ Fill Initial Kanban
> ⚠️ **Only do this if `doc/kanban.md` still contains placeholders (e.g., `[Epic Name]`).**

Based on `doc/constitution.md` you just read, populate `doc/kanban.md` with real project tasks:

**a) Identify Epics**
Break down the project purpose into 3-6 major features. Each becomes an EPIC.
```
EPIC-001: [Core feature 1]
EPIC-002: [Core feature 2]
...
```

**b) Create Backlog Tasks**
For each Epic, create 2-5 concrete, actionable tasks:
```
TASK-001: [Specific action] [EPIC-001]  → Complexity M, Priority P0
TASK-002: [Specific action] [EPIC-001]  → Complexity S, Priority P1
...
```

**c) Rules when filling**
- Use infinitive verbs: "Implement", "Create", "Configure", "Integrate"
- Keep tasks with 1-8h scope (use XL only if inevitable)
- Define clear, verifiable acceptance criteria
- Prioritize infrastructure/setup tasks as P0

**d) Update Next ID**
After creating all tasks, update the `**Next ID:**` field at the top of the kanban.

### 4️⃣ Register in Diary
Create entry in `diary/{{ month }}.md`:
```markdown
### [{{ now.strftime("%H:%M") }}] BOOT - Agent started
**Context:** [Summary from session-context.md]
**Kanban:** [How many epics/tasks were created or already existed]
**Target task:** TASK-XXX
**State found:** [What's in progress/blocked]
```

---

## 📋 Project Context

**Name:** {{ display_name }}  
**Type:** {{ agent_type }}  
**Generated:** {{ timestamp }}

### 🎯 Mission
{{ proposito }}

### 🛠️ Technology Stack
- **Frontend:** {{ stack.frontend }}
- **Backend:** {{ stack.backend }}
- **Database:** {{ stack.banco }}

### 📜 Principles (ALWAYS follow)
{% for principio in principios %}
- {{ principio }}
{% endfor %}

### 🚫 Prohibitions (NEVER do)
{% for proibicao in proibicoes %}
- {{ proibicao }}
{% endfor %}

### ✅ Definition of Done
{% for criterio in dod %}
- [ ] {{ criterio }}
{% endfor %}

---

## 📊 How to Work with the Kanban

### Task Hierarchy

```
EPIC (Major feature)
└── TASK (Work unit)
    └── SUBTASK (Specific step)
```

### Workflow

1. **CHOOSE** task from BACKLOG
2. **MOVE** to IN PROGRESS (update kanban.md)
3. **CREATE** subtasks if needed
4. **COMMIT** with reference: `feat(auth): add login [TASK-001]`
5. **UPDATE** session-context.md at the end
6. **MOVE** to COMPLETED when done

### Golden Rules
- ✅ Always link work to TASK-ID
- ✅ Update kanban BEFORE starting
- ✅ Create subtasks for work > 2h
- ✅ Reference task in commit

---

## 🚨 Golden Rules

1. **NEVER** code before reading the Constitution
2. **NEVER** ignore `emergency.md`
3. **ALWAYS** link to TASK-ID
4. **ALWAYS** update `session-context.md`
5. **ALWAYS** register in diary

---

## 🆘 In Case of Doubt

| Doubt about | Consult |
|-------------|---------|
| Architecture | `doc/oracle.md` |
| Rules | `doc/constitution.md` |
| Conventions | `doc/policies.md` |
| Tasks | `doc/kanban.md` |
| Blockers | `doc/emergency.md` |

**If still in doubt:** Register in `emergency.md` BEFORE proceeding.

---

*Generated with 🦑 Squidy v{{ version }} at {{ timestamp }}*
'''
    
    def _constitution_template_en(self) -> str:
        """Template constitution.md v2.0 - English"""
        return '''# CONSTITUTION - {{ display_name }}

**Generated at:** {{ timestamp }}  
**Agent Type:** {{ agent_type }}

---

## §1 - PURPOSE (Why does this project exist?)

{{ proposito }}

{% if contexto_negocio %}
### Business Context
- **Problem:** {{ contexto_negocio.problema }}
- **Target Users:** {{ contexto_negocio.usuarios_alvo }}
- **Main Value:** {{ contexto_negocio.valor_principal }}
{% endif %}

---

## §2 - PRINCIPLES (What to ALWAYS do)

{% for principio in principios %}
### {{ loop.index }}. {{ principio }}

**✅ DO:**
- [Specific related action]

**❌ AVOID:**
- [Common anti-pattern]

{% endfor %}

---

## §3 - PROHIBITIONS (What to NEVER do)

{% for proibicao in proibicoes %}
### {{ loop.index }}. {{ proibicao }}

**Why:** [Risk explanation]  
**Consequence:** [What happens if broken]  
**How to detect:** [How to identify]  
**Exception:** [When it can be broken, if applicable]

{% endfor %}

---

## §4 - CONVENTIONS

### Naming

| Element | Convention | Example |
|---------|------------|---------|
| Variables | {{ convencoes.variaveis }} | `{% if convencoes.variaveis == "camelCase" %}currentUser{% else %}current_user{% endif %}` |
| Functions | {{ convencoes.funcoes }} | `{% if convencoes.funcoes == "camelCase" %}calculateTotal{% else %}calculate_total{% endif %}()` |
| Classes | {{ convencoes.classes }} | `{% if convencoes.classes == "PascalCase" %}UserService{% else %}user_service{% endif %}` |
| Constants | {{ convencoes.constantes }} | `{% if convencoes.constantes == "UPPER_SNAKE" %}MAX_RETRIES{% else %}max_retries{% endif %}` |
| Files | {{ convencoes.arquivos }} | `{% if convencoes.arquivos == "kebab-case" %}user-service{% else %}user_service{% endif %}.js` |
| Database | {{ convencoes.banco }} | `{% if convencoes.banco == "snake_case" %}user_id{% else %}userId{% endif %}` |

### Commits (Conventional Commits)

```
type(scope): short description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Refactoring
- `chore`: Miscellaneous tasks

---

## §5 - DEFINITION OF DONE

{% for criterio in dod %}
- [ ] {{ criterio }}
{% endfor %}

---

## §6 - TECHNOLOGY STACK

- **Frontend:** {{ stack.frontend }}
- **Backend:** {{ stack.backend }}
- **Database:** {{ stack.banco }}

{% if arquitetura %}
### Architecture
- **Pattern:** {{ arquitetura.padrao }}
- **Layers:** {{ arquitetura.camadas | join(", ") }}
{% if arquitetura.integracoes %}
- **Integrations:** {{ arquitetura.integracoes | join(", ") }}
{% endif %}
{% endif %}

{% if qualidade %}
### Quality
- **Test Coverage:** {{ qualidade.cobertura_testes }}
- **Tools:** {{ qualidade.ferramentas | join(", ") }}
- **CI/CD:** {{ "Yes" if qualidade.ci_cd else "No" }}
{% endif %}

---

*Generated automatically by 🦑 Squidy v{{ version }}*
'''

    
    def _kanban_template_en(self) -> str:
        """Template kanban.md v2.0 - English"""
        return '''# KANBAN - {{ display_name }}

**Generated at:** {{ timestamp }}
**Next ID:** TASK-001

---

> ## 🤖 AGENT INSTRUCTION — INITIAL SETUP
>
> **This file was generated with placeholders.** In the first project session, you must replace them with real tasks before any development.
>
> ### How to fill:
> 1. **Read `doc/constitution.md`** to understand the project purpose and scope
> 2. **Identify 3-6 Epics** — major features that compose the product
> 3. **For each Epic, create 2-5 Tasks** in the BACKLOG with:
>    - Name in infinitive verb (\`Implement\`, \`Configure\`, \`Create\`...)
>    - Realistic complexity (XS/S/M/L — avoid XL)
>    - Verifiable acceptance criteria
>    - Priority (P0 = blocks release, P1 = important, P2 = desirable)
> 4. **Remove placeholders** (\`[Epic Name]\`, \`[Task Name]\`, etc.)
> 5. **Update the \`Next ID\`** field in the header of this file
>
> ⚠️ **Don't start developing before filling the kanban.**

---

## 📋 QUICK GUIDE

### Hierarchy
- **EPIC** → Major feature (ex: "Auth System")
- **TASK** → Work unit (ex: "JWT Login")
- **SUBTASK** → Specific step (ex: "Create endpoint")

### Priorities
- **P0** → Critical (blocks release)
- **P1** → High (important)
- **P2** → Medium (desirable)
- **P3** → Low (nice to have)

### Complexity
- **XS** → < 1h
- **S** → 1-2h
- **M** → 2-4h
- **L** → 4-8h
- **XL** → > 8h (break into smaller tasks)

---

## 🔥 EPICS

### EPIC-001: [Epic Name]
**Description:** [Short description]  
**Priority:** P0  
**Complexity:** M  
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Related Tasks:**
- [ ] TASK-001
- [ ] TASK-002

---

## 📋 BACKLOG

### TASK-001: [Task Name] [EPIC-001]
**Complexity:** M  
**Priority:** P0  
**Estimated Time:** 4h  
**Description:** [Detailed description]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Subtasks:**
- [ ] SUB-001: [Description] (XS - 30min)
- [ ] SUB-002: [Description] (S - 1h)

**Notes:**
- [Additional information]

---

## 🏗️ IN PROGRESS (WIP: 0/3)

*[Move tasks from BACKLOG here before starting]*

---

## ✅ COMPLETED

- [x] **TASK-000** Initial Squidy project setup
  - **Completed at:** {{ timestamp }}
  - **Agent:** Squidy Setup
  - **Notes:** Initial structure automatically generated

---

## ⏸️ BLOCKED

*[Register blockers with reason and date]*

---

## 📊 METRICS

- **WIP:** 0/3 (limit: 3 simultaneous tasks)
- **Velocity:** Calculating...
- **Completion Rate:** Calculating...
- **Blockers:** 0
- **Next ID:** TASK-001

---

*Keep this kanban updated — move tasks as progress happens*
'''
    
    def _oracle_template_en(self) -> str:
        """Template oracle.md (ADRs) - English"""
        return '''# ORACLE - Architecture Decisions (ADRs)

**Project:** {{ display_name }}  
**Generated at:** {{ timestamp }}

---

## ADR-001: Main Technology Stack

**Date:** {{ date }}  
**Status:** Accepted  
**Context:** Definition of technology stack based on project requirements.

**Decision:**
- **Frontend:** {{ stack.frontend }}
- **Backend:** {{ stack.backend }}
- **Database:** {{ stack.banco }}

**Consequences:**
- ✅ Stack aligned with project requirements
- ✅ Well-established tools and libraries
- ⚠️ Team needs knowledge in chosen technologies

{% if arquitetura %}
### Architecture Details
- **Pattern:** {{ arquitetura.padrao }}
- **Layers:** {{ arquitetura.camadas | join(", ") }}
{% if arquitetura.integracoes %}
- **Integrations:** {{ arquitetura.integracoes | join(", ") }}
{% endif %}
{% endif %}

---

## ADR-002: Technical Restrictions

**Date:** {{ date }}  
**Status:** Accepted

**Identified Restrictions:**
{% for restricao in restricoes %}
- {{ restricao }}
{% else %}
- No specific technical restrictions defined
{% endfor %}

**Consequences:**
- ✅ Non-functional requirements documented
- ⚠️ May impact future implementation choices

---

## ADR-003: Code Conventions

**Date:** {{ date }}  
**Status:** Accepted

**Decision:** Adopt the following conventions:

| Element | Convention |
|---------|------------|
| Variables | {{ convencoes.variaveis }} |
| Functions | {{ convencoes.funcoes }} |
| Classes | {{ convencoes.classes }} |
| Constants | {{ convencoes.constantes }} |
| Files | {{ convencoes.arquivos }} |
| Database | {{ convencoes.banco }} |

**Motivation:** Maintain code consistency and readability.

---

*Add new ADRs as important decisions are made*
'''

    
    def _policies_template_en(self) -> str:
        """Template policies.md - English"""
        return '''# POLICIES - {{ display_name }}

**Generated at:** {{ timestamp }}

---

## 🔧 Development Policies

### Commits and Versioning

- **Convention:** Conventional Commits (feat:, fix:, docs:, etc)
- **Branches:**
  - `main` → Production
  - `develop` → Development
  - `feature/*` → Features
  - `hotfix/*` → Urgent fixes
- **Pull Requests:** Required for merge into `main`

### Code Review

- **Minimum approvals:** 1 reviewer
- **Review Checklist:**
  - [ ] Code follows project standards
  - [ ] Adequate tests included
  - [ ] Documentation updated
  - [ ] No hardcoded credentials or secrets

### Tests

{% if qualidade %}
- **Minimum coverage:** {{ qualidade.cobertura_testes }}
- **Tools:** {{ qualidade.ferramentas | join(", ") }}
{% else %}
- **Minimum coverage:** 70%
- **Types:** Unit (required), Integration (when applicable)
{% endif %}
- **CI/CD:** Tests must pass before merge

---

## 📦 Deployment Policies

### Environments

- **Development:** Automatic deploy from `develop`
- **Staging:** Manual deploy for validation
- **Production:** Deploy after approval and staging tests

### Rollback

- Keep last functional version always deployable
- Documented rollback procedure
- Feature flags for critical features

---

## 🔒 Security Policies

### Credentials

- ❌ NEVER commit API keys, tokens, passwords
- ✅ Use environment variables or secret managers
- ✅ Rotate secrets regularly
- ✅ Use `.env.example` without real values

### Dependencies

- Review dependencies before adding
- Keep dependencies updated (security patches)
- Use vulnerability scanning tools (Dependabot, Snyk)

### Code

- Validate inputs in all APIs
- Use prepared statements for SQL
- Escape outputs in templates
- Implement rate limiting

---

*Policies can be adjusted as the project evolves*
'''
    
    def _emergency_template_en(self) -> str:
        """Template emergency.md - English"""
        return '''# EMERGENCY - {{ display_name }}

**Last updated:** {{ timestamp }}

---

## 🚨 Active Blockers

*No blockers registered at the moment*

---

## 📋 Block Registration Template

### BLOCK-XXX: [Block Title]

**Date:** YYYY-MM-DD HH:MM  
**Severity:** 🔴 Critical | 🟡 Important | 🟢 Low  
**Impact:** Which task/feature is blocked?

**Description:**
Detail the problem found.

**Resolution Attempts:**
1. What was already tried?
2. Why didn't it work?

**Additional Context:**
- Relevant logs
- Error messages
- Involved configurations

**Resolution:**
*To be filled when resolved*

---

## 📚 Resolved Blockers

### BLOCK-000: Example of resolved blocker

**Date:** {{ timestamp }}  
**Severity:** 🟢 Low  
**Resolution:** This is just an example to illustrate the format

---

*Use this file only for blockers that prevent progress — not for common bugs*
'''
    
    def _diary_index_template_en(self) -> str:
        """Template diary-index.md - English"""
        return '''# DIARY INDEX - {{ display_name }}

---

## 📅 Diary Files

### {{ now.strftime("%Y") }}

- [{{ month }}.md](../diary/{{ month }}.md) - Active

---

## 🔍 Quick Search

### By Entry Type

- **Important decisions:** Search for "DECISION:" in diary
- **Resolved problems:** Search for "RESOLVED:"
- **Blockers:** See `emergency.md`
- **Refactorings:** Search for "REFACTOR:"

### By Task

- **TASK-XXX:** Use task ID as keyword
- **EPIC-XXX:** Search by epic ID

---

## 📝 How to Register in the Diary

### Standard Format

```markdown
### [HH:MM] TASK-XXX - Short title

**Context:** [What you were doing]

**Action:** [What was done]

**Result:** [What happened]

**Next steps:** [What remains to be done]

**Notes:** [Additional information]
```

### Examples

```markdown
### [14:30] TASK-001 - Setup JWT

**Context:** Starting authentication implementation

**Action:** Installed jsonwebtoken library and configured middleware

**Result:** Middleware created and tested locally

**Next steps:** Create /login endpoint

**Notes:** Use RS256 algorithm in production
```

---

*This index is automatically updated as new files are created*
'''

    
    def _session_context_template_en(self) -> str:
        """Template session-context.md - English"""
        return '''# SESSION CONTEXT - {{ display_name }}

**Generated at:** {{ timestamp }}  
**Agent:** setup-squidy-ai  
**Current Task:** TASK-001  
**Phase:** Planning/Initial Setup

---

## 📊 Current State (Executive Summary)

Project "{{ display_name }}" was successfully configured using Squidy Setup AI.

**Technology Stack:**
- Frontend: {{ stack.frontend }}
- Backend: {{ stack.backend }}
- Database: {{ stack.banco }}

**Blockers:** None  
**Dependencies:** According to chosen stack

---

## 📚 Quick References

- **Constitution:** Review purpose and principles before starting
- **Oracle:** ADR-001 defines technology stack
- **Policies:** Follow commit and code review conventions
- **Kanban:** TASK-001 available to start

---

## 🧠 Short-term Memory

1. Project automatically configured via AI interview
2. Complete Squidy structure generated
3. Ready for development to begin

---

## ⚠️ Active Alerts

🔔 **REMINDER:** Review and adjust settings as needed  
🔔 **ATTENTION:** Add first real task to kanban (replace TASK-001)

---

## 🎯 Next Expected Action

Review structure and start development of TASK-001

---

*Update this file at the end of each work session*
'''
    
    def _agent_template_en(self) -> str:
        """Template AGENT.md (quick reference) - English"""
        return '''# AGENT - Quick Reference

**Project:** {{ display_name }}  
**Type:** {{ agent_type }}  
**Generated:** {{ timestamp }}

---

## 🎯 Who You Are

{{ agent_type.replace("-", " ").title() }} responsible for {{ display_name }}

## 🎯 Mission

{{ proposito }}

---

## 📜 Rules (ALWAYS follow)

{% for principio in principios %}
- {{ principio }}
{% endfor %}

---

## 🚫 Prohibitions (NEVER do)

{% for proibicao in proibicoes %}
- {{ proibicao }}
{% endfor %}

---

## ✅ Definition of Done

{% for criterio in dod %}
- [ ] {{ criterio }}
{% endfor %}

---

## 🛠️ Stack

- **Frontend:** {{ stack.frontend }}
- **Backend:** {{ stack.backend }}
- **Database:** {{ stack.banco }}

---

## 🧭 Quick Navigation

| File | Content |
|------|---------|
| `constitution.md` | Complete principles and prohibitions |
| `oracle.md` | Architecture decisions (ADRs) |
| `policies.md` | Code and deployment conventions |
| `kanban.md` | Open tasks |
| `emergency.md` | Critical blockers |
| `session-context.md` | Current project state |

---

*For complete initialization, read `../readme-agent.md` in root*
'''
    
    def _diary_template_en(self) -> str:
        """Template diary.md (monthly) - English"""
        return '''# DIARY - {{ display_name }} - {{ month }}

---

## {{ date }}

### Project Initial Setup

**Timestamp:** {{ timestamp }}  
**Agent:** squidy-setup-ai  
**Action:** Automatic generation of Squidy v2.0 structure  
**Context:** Project configured via interactive AI interview

**Decisions made:**
- Technology stack defined: {{ stack.frontend }} + {{ stack.backend }} + {{ stack.banco }}
- Agent type: {{ agent_type }}
- Purpose documented in Constitution
- {{ principios | length }} principles defined
- {{ proibicoes | length }} prohibitions established

**Next steps:**
1. Review generated files (especially `constitution.md`)
2. Adjust `kanban.md` with real project tasks
3. Configure development environment
4. Start TASK-001

---

*Format: ### [HH:MM] TASK-XXX - Description*
'''
