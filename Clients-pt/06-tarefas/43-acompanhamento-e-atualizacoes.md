# Acompanhamento e atualizações de tarefas

Depois de uma tarefa ser atribuída, tanto o funcionário como o responsável têm ferramentas para comunicar sobre a sua evolução e manter o estado atualizado a todo o momento. Este artigo explica como o acompanhamento é gerido de ambos os lados: a aplicação do funcionário e o backoffice do responsável.

---

## Como o funcionário atualiza o estado de uma tarefa

O funcionário gere as suas tarefas a partir da secção de tarefas da aplicação móvel. Aí encontra uma lista de todas as tarefas que lhe estão atribuídas, ordenadas por prioridade e prazo.

### Iniciar uma tarefa

Quando o funcionário está pronto para começar, abre o detalhe da tarefa e prime **Iniciar tarefa**. O estado muda de *atribuída* para *em curso* e o responsável vê-o refletido no backoffice.

### Marcar uma tarefa como concluída

Terminada a atividade, o funcionário prime **Marcar como concluída**. Se a tarefa tiver ativada a exigência de evidência —está por omissão—, o sistema não permite fechá-la sem pelo menos uma foto ou vídeo anexados, e devolve o erro `task/evidence_required`.

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

## Histórico de mudanças de estado

Cada tarefa mantém um registo cronológico e imutável de todas as mudanças de estado por que passou. O histórico é acessível a partir do detalhe da tarefa no backoffice e inclui:

- Data e hora exatas de cada mudança de estado.
- Estado anterior e estado novo.
- Nome do utilizador ou do sistema que efetuou a alteração.
- Comentário associado à alteração, se existiu.

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
