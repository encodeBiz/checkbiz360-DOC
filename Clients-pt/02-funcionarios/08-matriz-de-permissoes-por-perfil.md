# Matriz de permissões por perfil

O CheckBiz360 aplica um modelo de controlo de acesso baseado em perfis que determina com precisão o que cada utilizador pode fazer dentro da plataforma. Esta matriz é a referência definitiva para perceber que ações estão disponíveis para cada nível e em que condições.

Consulte esta tabela ao configurar novos perfis, ao esclarecer dúvidas sobre o acesso a funcionalidades ou ao rever a política de permissões da sua organização.

---

## Tabela de permissões

| Ação | Worker | Supervisor | Manager | Owner |
|---|---|---|---|---|
| Criar registo próprio | Sim | Sim | Sim | Sim |
| Ver histórico próprio | Sim | Sim | Sim | Sim |
| Ver histórico da equipa | Não | Sim (sucursal) | Sim | Sim |
| Solicitar jornada manual | Sim | Sim | Sim | Sim |
| Validar e corrigir registos | Não | Sim (sucursal) | Sim | Sim |
| Criar tarefas | Não | Configurável | Sim | Sim |
| Validar tarefas | Não | Configurável | Sim | Sim |
| Avaliar trabalhadores | Não | Configurável | Sim | Sim |
| Carregar documentos | Não | Não | Sim | Sim |
| Ver documentos próprios | Sim | Sim | Sim | Sim |
| Ver documentos da equipa | Não | Sim (por perfil) | Sim | Sim |
| Ver recibos de vencimento e contratos | Apenas os próprios | Apenas os próprios | Equipa | Todos |
| Criar incidências | Sim | Sim | Sim | Sim |
| Configurar sucursal | Não | Não | Sim | Sim |
| Gerir funcionários | Não | Não | Sim | Sim |
| Ver inteligência operacional | Não | Parcial | Sim | Sim |
| Gerar relatórios | Não | Não | Sim | Sim |
| Configurar entidade | Não | Não | Não | Sim |

---

## Notas sobre a tabela

### Permissões de supervisor configuráveis

Algumas permissões do perfil **supervisor** estão marcadas como «Configurável» na tabela. Isto significa que o comportamento por omissão pode ser ativado ou desativado pelo manager ou pelo owner consoante as necessidades operacionais da empresa. Em concreto:

- **Criar tarefas** — Por omissão, os supervisores não podem criar tarefas. O manager pode ativar esta capacidade para supervisores específicos.
- **Validar tarefas** — Tal como a criação: desativado por omissão, ativável pelo manager.
- **Avaliar trabalhadores** — Permite ao supervisor registar avaliações de desempenho sobre os workers da sua equipa. Desativado por omissão.

Para modificar estas permissões, aceda ao perfil do supervisor em causa e ajuste a configuração de permissões avançadas.

### Âmbito por sucursal no perfil supervisor

Quando na tabela aparece «Sim (sucursal)», significa que o supervisor apenas pode exercer essa ação sobre os funcionários ou dados pertencentes à sucursal onde tem atribuída a responsabilidade de supervisor. Não tem visibilidade nem capacidade de atuação sobre outras sucursais.

### Visualização de documentos da equipa por supervisores

A coluna do supervisor indica «Sim (por perfil)» para a visualização de documentos da equipa. Isto significa que o supervisor pode ver documentos do pessoal que tenha atribuído sob a sua responsabilidade, desde que esses documentos tenham sido marcados como acessíveis ao seu nível de perfil pelo manager que os carregou.

### Ver recibos de vencimento e contratos

Esta permissão tem um comportamento diferenciado consoante o perfil:

- **Worker e Supervisor** — Só podem ver os seus próprios documentos de vencimento e contrato.
- **Manager** — Pode ver os documentos de vencimento e contrato de todos os funcionários da sua equipa ou das sucursais que lhe estão atribuídas.
- **Owner** — Tem acesso a todos os documentos de vencimento e contratos da entidade, sem restrição de sucursal nem de equipa.

### Inteligência operacional para supervisores

O acesso «Parcial» do supervisor à inteligência operacional implica que pode consultar métricas e estatísticas básicas da equipa da sua sucursal (como horas trabalhadas ou taxas de assiduidade), mas não tem acesso aos painéis de análise estratégica, comparações entre sucursais nem indicadores financeiros agregados que estão disponíveis para o manager e o owner.

### Configurar entidade

Esta ação está reservada em exclusivo ao perfil **owner**. Inclui a configuração de parâmetros globais da empresa como o nome da entidade, o fuso horário, as integrações com sistemas externos e a gestão da subscrição.

---

## Considerações sobre a segurança de acesso

A atribuição de perfis deve ser revista com regularidade, sobretudo nos seguintes momentos:

- Quando um funcionário muda de função ou de responsabilidades.
- Quando um supervisor passa a gerir uma sucursal diferente.
- Quando um funcionário sai da empresa.
- Após reestruturações organizativas ou aberturas de novas sucursais.

> **Nota:** atribuir um nível de perfil superior ao necessário pode comprometer a confidencialidade da informação. Recomenda-se aplicar o princípio do privilégio mínimo: cada funcionário deve ter apenas o nível de acesso de que precisa para desempenhar as suas funções.

---

## Quem pode consultar esta configuração

A visualização e modificação das permissões de perfil está disponível para os perfis **manager** (nível 3) e **owner** (nível 4).

---

## Artigos relacionados

- [Perfis e níveis de responsabilidade](07-perfis-e-niveis-de-responsabilidade.md)
- [Criar e gerir funcionários](06-criar-e-gerir-funcionarios.md)
- [Permissões de acesso documental](../05-gestao-documental/37-permissoes-de-acesso-documental.md)
- [O que é a inteligência operacional](../07-inteligencia-operacional/49-o-que-e-a-inteligencia-operacional.md)
