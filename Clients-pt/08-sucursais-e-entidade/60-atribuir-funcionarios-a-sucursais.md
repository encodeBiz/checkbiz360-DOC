# Atribuir funcionários a sucursais

A atribuição de um funcionário a uma sucursal é o mecanismo pelo qual o CheckBiz360 associa uma pessoa a um local de trabalho concreto. Esta associação determina a partir de que sucursal o funcionário pode registar, que horários se aplicam, que responsáveis supervisionam os seus registos e que geocerca se usa para validar a sua localização. Este artigo explica como realizar esta atribuição, como gerir funcionários que trabalham em várias sucursais e que impacto tem a atribuição no sistema.

## Conceitos prévios: responsabilidades e atribuição a sucursal

Cada funcionário no CheckBiz360 tem associadas uma ou várias **responsabilidades**. Cada responsabilidade define o contexto em que esse funcionário opera: a atribuição a uma sucursal, o perfil que tem nela e, opcionalmente, o projeto ou área funcional.

A atribuição a uma sucursal é o vínculo que une um funcionário a uma sucursal. Quando o funcionário regista a partir da aplicação, o sistema identifica a que sucursal pertence esse registo a partir desta atribuição. Se um funcionário não tiver qualquer responsabilidade com sucursal atribuída, não poderá registar.

## Atribuir um funcionário a uma sucursal

### A partir da ficha do funcionário

1. Aceda ao backoffice web e navegue até **Funcionários** no menu lateral.
2. Localize o funcionário que pretende atribuir e clique no seu nome para abrir a sua ficha.
3. Desça até à secção **Responsabilidades** ou **Atribuições**.
4. Prima **Adicionar responsabilidade**.
5. Selecione a sucursal na lista **Sucursal**. A listagem mostra apenas as sucursais ativas da sua entidade.
6. Atribua o perfil que o funcionário terá nessa sucursal: **Worker**, **Supervisor** ou **Manager**.
7. Se for o caso, selecione o calendário efetivo que se aplicará a este funcionário nessa sucursal.
8. Prima **Guardar**. A atribuição aplica-se de imediato.

### A partir da gestão da sucursal

Também pode atribuir funcionários diretamente a partir da ficha da sucursal:

1. Navegue até **Sucursais** e abra a sucursal pretendida.
2. Aceda ao separador **Funcionários** dentro da ficha da sucursal.
3. Prima **Atribuir funcionário** e introduza o nome ou o correio eletrónico do funcionário na pesquisa.
4. Selecione o perfil e o calendário e prima **Confirmar**.

### Adicionar uma equipa inteira

Se a mesma equipa de trabalho trabalha em vários projetos, não é preciso associar cada pessoa em separado. Na lista de funcionários da ficha da sucursal, **Aplicar equipa** adiciona de uma vez todos os membros de uma equipa, cada um com a sua responsabilidade, função e valor, e ignora quem já lá estava. **Guardar como equipa** faz o contrário: converte o pessoal da sucursal numa equipa reutilizável. Consulte [Equipas](../02-funcionarios/99-equipas.md).

## Multi-sucursal: um funcionário em várias sucursais

O CheckBiz360 admite que o mesmo funcionário esteja atribuído a várias sucursais em simultâneo, com perfis distintos em cada uma. Esta funcionalidade foi concebida para cobrir casos como:

- Um funcionário que trabalha em duas lojas de forma alternada.
- Um responsável que atua como Supervisor na sua sucursal habitual e como Manager numa sucursal de menor dimensão.
- Equipas de campo que se deslocam entre instalações consoante o planeamento semanal.

### Como funciona o multi-sucursal

Quando um funcionário com várias responsabilidades regista a partir da aplicação, o sistema determina automaticamente em que sucursal está a registar, comparando a localização GPS do dispositivo com as coordenadas e os raios de cada sucursal atribuída. Se o funcionário estiver dentro do raio da sucursal A, o registo é gravado na sucursal A; se estiver no raio da sucursal B, é gravado na sucursal B.

Caso o funcionário esteja fora do raio de todas as suas sucursais atribuídas e a geocerca não esteja desativada, o registo será recusado com o código `checklog/out_of_radius`.

> **Aviso:** se os raios de duas sucursais se sobrepuserem geograficamente, pode haver ambiguidade na atribuição do registo. Nesses casos, o sistema prioriza a sucursal cujo centro esteja mais próximo da posição real do funcionário. Reveja os raios configurados se detetar atribuições incorretas de forma recorrente.

### Perfis distintos por sucursal

Cada responsabilidade é independente. O mesmo funcionário pode ser Worker numa sucursal e Supervisor noutra. As permissões que se aplicam em cada contexto são as do perfil dessa responsabilidade concreta, e não as do perfil mais elevado do funcionário.

## Impacto da atribuição no calendário efetivo

Ao atribuir um funcionário a uma sucursal, o sistema associa essa atribuição ao calendário efetivo selecionado. O calendário define os dias úteis, os feriados próprios dessa sucursal e os turnos de trabalho. Esta associação tem as seguintes implicações:

- Os registos do funcionário são comparados com os turnos do calendário para detetar anomalias (chegadas tardias, ausências, saídas antecipadas).
- O cômputo de horas trabalhadas é calculado em relação aos turnos previstos nesse calendário.
- As notificações de ausência ou de jornada incompleta são geradas em função dos turnos do calendário dessa sucursal.

Se um funcionário trabalhar em duas sucursais com calendários distintos, cada registo é validado contra o calendário da sucursal em que ocorre.

## Impacto da atribuição nos registos

Assim que o funcionário tiver uma ou mais responsabilidades ativas, a aplicação mostrará automaticamente o botão de registo e a informação da sucursal correspondente. O funcionário não precisa de selecionar manualmente a sua sucursal na aplicação; o sistema deteta-a por GPS.

Se o funcionário não tiver qualquer atribuição ativa ou a sua única sucursal atribuída estiver inativa, a aplicação mostrará uma mensagem de erro e não lhe permitirá registar.

## Eliminar ou modificar uma atribuição

Para desassociar um funcionário de uma sucursal:

1. Abra a ficha do funcionário em **Funcionários**.
2. Localize a responsabilidade que pretende eliminar na secção **Responsabilidades**.
3. Prima o ícone de eliminação junto à responsabilidade correspondente.
4. Confirme a operação. O funcionário deixará de poder registar nessa sucursal a partir desse momento. O histórico de registos anteriores nessa sucursal conserva-se intacto.

---

> **Nota de perfil:** a atribuição de funcionários a sucursais está disponível para os perfis **Owner** e **Manager**. O perfil **Supervisor** pode visualizar as atribuições dos funcionários da sua equipa, mas não as pode criar nem modificar.

## Artigos relacionados

- [Criar e gerir sucursais](57-criar-e-gerir-sucursais.md)
- [Equipas](../02-funcionarios/99-equipas.md)
- [Estados de uma sucursal](59-estados-de-uma-sucursal.md)
- [Configuração da entidade](61-configuracao-da-entidade.md)
- [Vista global multi-sucursal](62-vista-global-multi-sucursal.md)
