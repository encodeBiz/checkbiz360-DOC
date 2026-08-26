# Perfis e níveis de responsabilidade

O CheckBiz360 estrutura o acesso à plataforma através de um sistema de quatro níveis de perfil. Cada nível determina o que um utilizador pode ver e fazer dentro do sistema, desde o funcionário de base até ao proprietário da conta.

Perceber como funcionam os perfis e como se aplicam consoante o âmbito de responsabilidade é fundamental para configurar corretamente a plataforma e garantir que cada pessoa acede apenas à informação que lhe diz respeito.

---

## Os quatro níveis de perfil

### Nível 1 — Worker (Funcionário)

É o nível de acesso mais básico. O worker pode registar entradas e saídas, consultar o seu próprio histórico, solicitar jornadas manuais, ver os seus próprios documentos e criar incidências. Não tem visibilidade sobre os dados do resto da equipa nem capacidade para modificar a configuração da plataforma.

**Casos de utilização típicos:** operário de produção, agente de apoio ao cliente, técnico de campo.

### Nível 2 — Supervisor

O supervisor tem acesso alargado à equipa que lhe está atribuída. Pode consultar o histórico de registos da sua sucursal, validar e corrigir registos, e aceder a determinados documentos da equipa. Algumas das suas permissões são configuráveis pelo manager: a capacidade de criar tarefas, validá-las ou avaliar os trabalhadores pode estar ativada ou não consoante a configuração da empresa.

**Casos de utilização típicos:** encarregado de turno, responsável de equipa numa sucursal, chefe de secção.

### Nível 3 — Manager (Responsável)

O manager dispõe de acesso completo à gestão operacional: pode criar e gerir funcionários, configurar sucursais, validar qualquer registo, gerir documentos, gerar relatórios e aceder à inteligência operacional da empresa. É o perfil habitual do diretor de recursos humanos ou do gestor de área.

**Casos de utilização típicos:** diretor de recursos humanos, gestor de área, responsável de operações.

### Nível 4 — Owner (Proprietário)

O owner tem acesso absoluto à plataforma, incluindo a configuração global da entidade, a gestão da subscrição e todas as funcionalidades do manager. Apenas uma ou poucas pessoas na organização devem ter este nível.

**Casos de utilização típicos:** CEO, sócio fundador, diretor-geral, administrador de sistemas.

---

## Tipo de relação: interno face a colaborador

Independentemente do nível de perfil atribuído, cada funcionário tem um tipo de relação com a empresa:

- **Interno** — Funcionário do quadro com contrato de trabalho em vigor. Faz parte da estrutura habitual da organização.
- **Colaborador** — Pessoa externa que trabalha para a empresa de forma pontual ou recorrente sem pertencer ao quadro. Pode ser um freelancer, um prestador de serviços ou um trabalhador independente.

Ambos os tipos podem ter qualquer nível de perfil, embora na prática os colaboradores costumem operar como workers ou supervisores com um âmbito limitado.

---

## Âmbito de responsabilidade: entidade face a sucursal

O perfil de um funcionário pode aplicar-se a dois âmbitos distintos:

### Responsabilidade ao nível da entidade

Quando se atribui um perfil ao nível da entidade, o utilizador tem esse nível de acesso em toda a empresa, independentemente de quantas sucursais existam. Um manager ao nível da entidade pode gerir funcionários, registos e documentos de todas as sucursais.

### Responsabilidade ao nível da sucursal

Quando se atribui um perfil associado a uma sucursal concreta, o acesso do utilizador fica limitado a essa localização. Um supervisor com responsabilidade na sucursal de Lisboa só verá os registos e a equipa dessa sucursal, sem acesso aos dados de outras localizações.

---

## Um funcionário, vários perfis em simultâneo

O CheckBiz360 permite que o mesmo funcionário tenha perfis distintos em diferentes sucursais. Esta flexibilidade cobre situações reais como as seguintes:

- Uma pessoa pode ser **supervisor** na sucursal do Porto (onde lidera a equipa de turno) e **worker** na sucursal de Lisboa (onde colabora pontualmente).
- Um responsável de recursos humanos pode ter perfil de **manager** ao nível da entidade, ao mesmo tempo que numa sucursal específica atua adicionalmente como supervisor para tarefas de gestão direta.

Para configurar este cenário, aceda ao perfil do funcionário e atribua as responsabilidades correspondentes a cada sucursal.

---

## Atribuição de responsabilidades: quem pode atribuir o quê

Nem todos os utilizadores podem atribuir qualquer perfil. As restrições são as seguintes:

- Um **owner** pode atribuir qualquer nível de perfil a qualquer funcionário em qualquer âmbito.
- Um **manager** pode atribuir perfis até ao nível de supervisor a funcionários dentro do seu âmbito de gestão.
- Um **supervisor** não pode atribuir perfis.
- Um **worker** não pode atribuir perfis.

> **Nota:** recomenda-se rever periodicamente as atribuições de responsabilidades, sobretudo após alterações organizativas como rotações de equipa, promoções ou entrada de novos responsáveis.

---

## Quem pode realizar estas ações

A configuração de perfis e responsabilidades está disponível para os perfis **manager** (nível 3) e **owner** (nível 4).

---

## Artigos relacionados

- [Criar e gerir funcionários](06-criar-e-gerir-funcionarios.md)
- [Matriz de permissões por perfil](08-matriz-de-permissoes-por-perfil.md)
- [Funcionários multi-entidade](11-funcionarios-multi-entidade.md)
- [Exportar a lista de funcionários](12-exportar-lista-de-funcionarios.md)
