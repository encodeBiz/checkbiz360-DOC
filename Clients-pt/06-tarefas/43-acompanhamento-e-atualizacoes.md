# Acompanhamento e atualizações de tarefas

Depois de uma tarefa ser atribuída, tanto o funcionário como o responsável têm ferramentas para comunicar sobre a sua evolução e manter o estado atualizado a todo o momento. Este artigo explica como o acompanhamento é gerido de ambos os lados: a aplicação do funcionário e o backoffice do responsável.

---

## Como o funcionário atualiza o estado de uma tarefa

O funcionário gere as suas tarefas a partir da secção de tarefas da aplicação móvel. Aí encontra uma lista de todas as tarefas que lhe estão atribuídas, ordenadas por prioridade e prazo.

### Iniciar uma tarefa

Quando o funcionário está pronto para começar, prime **Iniciar**. O estado muda de *atribuída* para *em curso* e o responsável vê-o refletido no backoffice.

**A partir da versão 1.6.0 da aplicação** o botão está em três sítios, e faz o mesmo nos três: no próprio cartão da lista de tarefas, no cartão **Tarefas de hoje** do ecrã de assiduidade, e dentro do detalhe como até agora. Já não é preciso abrir a tarefa para a começar.

Os botões só aparecem nas tarefas atribuídas ao funcionário. Um supervisor que vê tarefas da sua equipa continua a atuar sobre elas a partir do detalhe.

Para iniciar é preciso ter a **jornada aberta** (ter registado a entrada) e, se a tarefa tiver local de trabalho próprio, estar dentro da sua margem. Ver [Relação com o controlo de horários](./39-o-que-e-o-modulo-de-tarefas.md#relação-com-o-controlo-de-horários) e [Local de trabalho próprio](./40-criar-uma-tarefa.md#local-de-trabalho-próprio).

### Marcar uma tarefa como concluída

Terminada a atividade, o funcionário prime **Concluir**. Se a tarefa tiver ativada a exigência de evidência —está por omissão—, o sistema não permite fechá-la sem pelo menos uma foto ou vídeo anexados, e devolve o erro `task/evidence_required`.

**A partir da versão 1.6.0**, concluir pede confirmação antes de fechar a tarefa. É a única das quatro ações que o funcionário não pode desfazer sozinho: para voltar atrás é preciso que um responsável a rejeite. Iniciar, pausar e retomar não perguntam, porque outro toque desfá-las.

Se a tarefa exigir evidência e se premir **Concluir** a partir da lista, a aplicação abre o detalhe em vez de tentar fechá-la: é aí que se carregam as fotos.

---

## Pausar e retomar uma tarefa

Quando o trabalho é interrompido —para almoçar, para ir buscar material, ou porque continua no dia seguinte—, a tarefa é **pausada** e depois **retomada**, tantas vezes quantas forem necessárias. O tempo em pausa é somado à parte e aparece no [relatório de tarefas](./48-relatorios-de-tarefas.md).

### A partir da aplicação

No detalhe de uma tarefa em curso, o funcionário prime **Pausar**; para continuar, prime **Retomar**. Está disponível **a partir da versão 1.4.0 da aplicação**.

**A partir da 1.6.0** estão também fora do detalhe: no cartão da lista de tarefas, ao lado de **Concluir**, e em **Tarefas de hoje** como botão de ícone junto ao principal.

- Na aplicação, o botão de pausar aparece quando o funcionário tem a jornada registada.
- **Retomar** pede o mesmo que iniciar: jornada aberta e, se a tarefa tiver local de trabalho próprio, estar dentro da sua margem.
- O detalhe mostra o **tempo investido** —do início ao fim, ou até agora, descontando as pausas— e o total de pausas.

### A partir do backoffice

No detalhe de uma tarefa em curso aparecem os botões **Pausar** e **Retomar**. No resumo da tarefa, o valor **Pausas** indica desde quando está em pausa ou, se já não estiver, quanto somaram as pausas.

Podem pausar e retomar os funcionários atribuídos e, a partir do backoffice, supervisores, managers e owners.

> **Importante:** uma tarefa com local de trabalho próprio não pode ser retomada nem concluída a partir do backoffice, porque o painel não envia localização. Tem de o fazer um funcionário a partir da aplicação. Pausá-la a partir do backoffice é possível.

### Regras da pausa

- **A pausa é da tarefa**, não de cada pessoa. Só há uma pausa aberta de cada vez: se houver vários atribuídos, qualquer um deles a pausa ou a retoma, e fica anotado quem o fez.
- **Concluir, cancelar ou recusar** uma tarefa em pausa é permitido: a pausa é fechada nesse momento. Não é preciso retomar só para a poder fechar.
- **Reabrir** a tarefa põe a zero os contadores de pausa; o histórico conserva as pausas anteriores.
- A pausa **não alarga o prazo**: o cumprimento temporal continua a ser calculado da mesma forma.
- Pausar e retomar **não enviam notificações**.

> **Sugestão:** incentivar os funcionários a acrescentar um comentário breve ao concluir a tarefa —ainda que não seja obrigatório— melhora a qualidade do registo e facilita a validação por parte do responsável.

---

## Notas de progresso

Durante o tempo em que uma tarefa estiver ativa, o funcionário pode acrescentar notas a qualquer momento a partir do detalhe da tarefa na aplicação. São visíveis para o responsável no backoffice, e vice-versa.

Cada nota é classificada com um tipo, o que permite distinguir num relance a natureza da comunicação:

| Tipo de nota | Para que se usa |
|---|---|
| **Especificação** | Precisar como o trabalho deve ser feito |
| **Nota operacional** | Informar do avanço ou do dia a dia da execução |
| **Esclarecimento** | Resolver uma dúvida colocada sobre a tarefa |
| **Nota de incidência** | Deixar constância de um problema encontrado durante a execução |

As notas são úteis para:

- Informar de que se concluiu uma parte da tarefa e se continua com outra.
- Comunicar uma incidência ou dificuldade encontrada durante a execução.
- Anexar uma foto ou documento como evidência parcial de progresso.
- Solicitar esclarecimentos ou confirmação antes de continuar.

O responsável também pode acrescentar comentários a partir do backoffice, que o funcionário verá na aplicação. Isto permite uma comunicação direta sobre a tarefa sem necessidade de chamadas nem de mensagens externas.

---

## Histórico da tarefa

A secção **Histórico** do detalhe da tarefa conta o seu percurso completo, por ordem: criada, atribuída, iniciada, pausada e retomada, concluída, validada ou recusada, cancelada, e as mudanças de estado feitas à mão. Cada linha indica:

- Data e hora.
- Quem o fez e com que perfil. As ações automáticas aparecem como **Sistema**; se uma pessoa do backoffice não tiver nome registado, aparece como **Utilizador do painel**.
- O motivo, nas validações, nas recusas e no último cancelamento.

Também ficam anotadas as tentativas de iniciar ou retomar uma tarefa **fora do seu local de trabalho** («Início recusado: fora do local de trabalho»), que ajudam a perceber porque é que um funcionário não conseguiu começar.

As notas, evidências e avaliações têm a sua própria secção no detalhe e não se repetem no histórico. A partir da versão 1.4.0, a aplicação mostra também o histórico da tarefa, pausas incluídas.

Este histórico não pode ser editado nem eliminado. Garante a rastreabilidade completa da tarefa e serve de base para resolver discrepâncias ou auditar o desempenho da equipa.

---

## Acompanhamento em tempo real a partir do backoffice

O responsável não precisa de esperar que o funcionário informe: as mudanças de estado sincronizam-se de imediato entre a aplicação e o backoffice.

A partir do painel de tarefas do backoffice, o manager ou supervisor pode:

- Ver o estado atual de todas as tarefas ativas, filtradas por estado, prioridade, funcionário ou sucursal.
- Aceder ao detalhe de cada tarefa para ler as notas do funcionário e rever as suas evidências.
- Identificar tarefas que estão há demasiado tempo *em curso* sem avanço.
- Detetar as que estão *em risco* ou *vencidas* através do indicador de cumprimento temporal.

> **Nota:** o sistema avisa por sua iniciativa em duas situações: quando uma tarefa com hora prevista de início não arrancou 15 minutos depois, e quando se aproxima ou se ultrapassa o prazo. Que uma tarefa esteja há muito tempo *em curso* sem novidades não dispara qualquer aviso automático: isso deteta-se revendo a lista.

---

## Notificações de atualização

Quando o estado de uma tarefa muda, o sistema notifica as partes envolvidas de forma automática. O responsável recebe uma notificação no backoffice quando o funcionário marca uma tarefa como concluída ou acrescenta um comentário relevante. O funcionário recebe uma notificação push quando o responsável valida, recusa ou comenta uma tarefa.

Isto elimina a necessidade de fazer acompanhamento manual: o sistema informa cada pessoa no momento em que deve agir.

Para uma descrição detalhada de todos os tipos de notificação, consulte o artigo [Notificações de tarefas](./47-notificacoes-de-tarefas.md).

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Estados de uma tarefa](./42-estados-de-uma-tarefa.md) | Ciclo de vida e transições de estado |
| [Validação de tarefas](./45-validacao-de-tarefas.md) | Fluxo de validação pelo responsável |
| [Notificações de tarefas](./47-notificacoes-de-tarefas.md) | Tipos de aviso e canais de notificação |
| [Relatórios de tarefas](./48-relatorios-de-tarefas.md) | Métricas de acompanhamento e exportação |
| [Atribuir tarefas a funcionários](./41-atribuir-tarefas-a-funcionarios.md) | Como atribuir e reatribuir tarefas |
| [Calendário semanal de tarefas](./111-calendario-semanal-de-tarefas.md) | A semana num relance, dia a dia e hora a hora, com os buracos e as sobreposições |
