# Atribuir tarefas a funcionários

A atribuição é o mecanismo pelo qual uma tarefa passa de existir no sistema a estar ativa no dispositivo de um funcionário. O CheckBiz360 oferece flexibilidade para atribuir tarefas de forma individual ou a grupos de funcionários, e permite reatribuí-las a qualquer momento se as circunstâncias mudarem.

---

## Atribuição individual

A atribuição individual associa uma tarefa a um único funcionário. É o método mais habitual para atividades concretas em que a responsabilidade recai sobre uma pessoa específica.

Ao selecionar o funcionário durante a criação ou edição da tarefa, o sistema regista-o como responsável. A partir desse momento, a tarefa aparece na sua lista de tarefas pendentes dentro da aplicação e recebe uma notificação push.

Este método é adequado para tarefas de manutenção, formação específica, gestão de uma incidência ou qualquer atividade que deva ser concluída por uma pessoa concreta.

---

## Atribuição por equipa ou sucursal

Quando a tarefa é de carácter coletivo ou se pretende distribuir trabalho por vários membros, é possível selecionar mais do que um funcionário durante a atribuição. Todos os destinatários receberão a tarefa na sua aplicação em simultâneo.

> **Importante:** na atribuição múltipla existe **uma única tarefa** partilhada por todos os atribuídos, não uma cópia para cada um. Por omissão, **qualquer um deles a pode concluir**, e ao fazê-lo a tarefa fica fechada para o grupo. O que fica registado em separado é a participação de cada funcionário: a sua atribuição, quando começou e o que contribuiu.

Se precisar de que cada pessoa execute o trabalho de forma independente, crie uma tarefa por funcionário.

Uma tarefa pertence sempre a uma sucursal, pelo que a seleção de funcionários se faz sobre os que trabalham nesse local.

> **Nota:** as [equipas](../02-funcionarios/99-equipas.md) da secção Funcionários aplicam-se a sucursais, não a tarefas. Depois de aplicar uma equipa à sucursal, os seus membros selecionam-se na tarefa um a um, como o resto do pessoal. Adicionar uma equipa inteira a uma tarefa de uma vez está planeado.

---

## Reatribuição de tarefas

As circunstâncias mudam: um funcionário pode ausentar-se, mudar de turno ou revelar-se não ser a pessoa adequada para uma tarefa concreta. O CheckBiz360 permite reatribuir uma tarefa a outro funcionário a qualquer momento, desde que não esteja no estado «concluída» ou «validada».

### Passos para reatribuir uma tarefa

1. Aceda ao backoffice e abra a lista de **Tarefas**.
2. Localize a tarefa que pretende reatribuir e clique nela para abrir o detalhe.
3. Prima **Editar**. No campo de funcionários atribuídos, retire o funcionário atual e selecione o novo destinatário.
4. Prima **Guardar**. Ao guardar, a tarefa é atribuída às pessoas que adicionou e retirada às que removeu. O novo funcionário recebe uma notificação push.
5. Se o considerar oportuno, acrescente uma nota a explicar o motivo da alteração.

Também pode retirar uma pessoa diretamente a partir do bloco **Equipa atribuída** do detalhe da tarefa.

> **Importante:** ao reatribuir, o funcionário original deixa de ver a tarefa na sua aplicação. Se já tinha iniciado a tarefa ou deixado comentários, essas anotações conservam-se e são visíveis a partir do backoffice.

> **Nota:** a sucursal de uma tarefa não pode ser alterada ao editá-la, pelo que os funcionários que se adicionem têm de trabalhar nessa mesma sucursal.

---

## O que o funcionário vê na aplicação

Quando lhe é atribuída uma tarefa, o funcionário recebe uma notificação push no seu dispositivo. Ao abrir a aplicação, encontrará a tarefa na sua lista de tarefas ativas, ordenadas por prioridade e prazo.

Dentro do detalhe da tarefa, o funcionário pode consultar:

- O título e a descrição completa da atividade, com a sua formatação: listas, listas de verificação, títulos e ligações.
- A prioridade atribuída (crítica, alta, média ou baixa).
- A data e hora limite, e a data prevista de início, se tiver sido indicada.
- O local de trabalho, se a tarefa tiver um próprio, com a ligação **Ver no Maps**.
- As evidências já carregadas e as notas da tarefa.
- O tempo investido e o total de pausas, e o histórico da tarefa (a partir da versão 1.4.0 da aplicação).

O funcionário pode iniciar a tarefa, pausá-la e retomá-la, acrescentar notas de progresso, carregar evidências e, quando terminar, marcá-la como concluída.

---

## Notificação push automática ao atribuir

No momento em que a atribuição é guardada, o CheckBiz360 envia automaticamente uma notificação push para o dispositivo do funcionário. Não é necessária qualquer ação adicional por parte do responsável.

A notificação inclui o título da tarefa e o prazo, de modo que o funcionário tenha a informação essencial sem necessidade de abrir a aplicação.

Se o funcionário tiver as notificações push desativadas no seu dispositivo, a tarefa continuará a aparecer na sua lista dentro da aplicação, mas não receberá o aviso no ecrã.

---

## Quem trabalhou na tarefa

O bloco **Equipa atribuída** do detalhe da tarefa mostra as pessoas atribuídas. A secção **Histórico** conta o percurso completo —quem a criou, quem a iniciou, quem a pausou ou a concluiu— com a data e o perfil de cada atuação; é descrita em [Acompanhamento e atualizações](./43-acompanhamento-e-atualizacoes.md#histórico-da-tarefa).

Nada disto pode ser modificado nem eliminado a partir do backoffice.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Criar uma tarefa](./40-criar-uma-tarefa.md) | Campos e passos para criar uma tarefa de raiz |
| [Estados de uma tarefa](./42-estados-de-uma-tarefa.md) | Ciclo de vida e mudanças de estado |
| [Acompanhamento e atualizações](./43-acompanhamento-e-atualizacoes.md) | Como o funcionário atualiza o progresso |
| [Notificações de tarefas](./47-notificacoes-de-tarefas.md) | Tipos de notificação e configuração |
| [Perfis e níveis de responsabilidade](../02-funcionarios/07-perfis-e-niveis-de-responsabilidade.md) | Descrição de cada perfil na plataforma |
