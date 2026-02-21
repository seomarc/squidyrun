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
    
    Example:
        >>> engine = TemplateEngine()
        >>> content = engine.render("readme-agent.md", config={...})
    """
    
    def __init__(self):
        self.loader = TemplateLoader(self._get_templates())
        self.env = Environment(
            loader=self.loader,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # Filtros customizados
        self.env.filters["kebab_case"] = self._kebab_case
        self.env.filters["pascal_case"] = self._pascal_case
        self.env.filters["snake_case"] = self._snake_case
    
    def render(self, template_name: str, **kwargs) -> str:
        """
        Renderiza um template
        
        Args:
            template_name: Nome do template
            **kwargs: Variáveis para o template
            
        Returns:
            Conteúdo renderizado
        """
        template = self.env.get_template(template_name)
        
        # Adiciona variáveis padrão
        context = {
            "now": datetime.now(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "month": datetime.now().strftime("%Y-%m"),
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
    
    def _get_templates(self) -> dict[str, str]:
        """Retorna dicionário de templates"""
        return {
            # Templates serão adicionados aqui
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

### 3️⃣ Registrar no Diário
Crie entrada em `diario/{{ month }}.md`:
```markdown
### [{{ now.strftime("%H:%M") }}] BOOT - Agente iniciado
**Contexto:** [Resumo do contexto-sessao.md]
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
