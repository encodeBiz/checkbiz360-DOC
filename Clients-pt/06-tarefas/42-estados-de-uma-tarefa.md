# Estados de uma tarefa

Cada tarefa no CheckBiz360 atravessa um ciclo de vida definido, desde que é criada até ficar encerrada. Compreender os estados e as transições entre eles é fundamental para fazer um acompanhamento correto do trabalho atribuído.

Uma tarefa tem **dois indicadores independentes**: o seu **estado**, que reflete em que ponto do trabalho está, e o seu **cumprimento temporal**, que reflete como está face ao prazo. Convém não os confundir: uma tarefa pode estar *em curso* e ao mesmo tempo *vencida*.

---

## O ciclo de vida de uma tarefa

O percurso habitual é:

**Rascunho → Atribuída → Em curso → Concluída → Validada**

Com dois desvios possíveis: o responsável pode **recusar** uma tarefa concluída, ou **cancelar** a tarefa em qualquer momento antes do seu encerramento.

---

## Tabela de estados

| Estado | Descrição | Quem o pode ativar |
|---|---|---|
| **Rascunho** | A tarefa está criada mas ainda não foi posta em circulação. Serve para a preparar antes de a enviar à equipa. | Quem a cria, a partir do backoffice |
| **Atribuída** | A tarefa foi enviada aos seus responsáveis, que receberam a notificação, mas ninguém começou ainda. | Quem a cria, ou o sistema ao atribuir |
| **Em curso** | Um funcionário atribuído iniciou a tarefa e está a trabalhar nela. | Funcionário a partir da aplicação |
| **Concluída** | O funcionário marcou a tarefa como terminada e fica pendente de revisão. | Funcionário a partir da aplicação |
| **Validada** | O responsável reviu o trabalho e aceitou-o como correto. É o encerramento satisfatório. | Manager, ou owner ou supervisor com permissão de validação |
| **Recusada** | O responsável reviu a tarefa concluída e devolveu-a com um motivo obrigatório. | Manager, ou owner ou supervisor com permissão de validação |
| **Cancelada** | A tarefa é anulada porque já não se aplica. Exige motivo e não conta como incumprimento. | Manager ou owner a partir do backoffice |

Os estados *Validada*, *Recusada* e *Cancelada* não podem ser atribuídos à mão ao criar ou editar uma tarefa: são resultado de uma ação do ciclo de vida (validar, recusar, cancelar).

---

## Indicador de cumprimento temporal

Em paralelo ao estado, cada tarefa mantém um indicador de cumprimento face ao seu prazo:

| Indicador | O que significa |
|---|---|
| **Por iniciar** | Ainda não se começou a trabalhar nela |
| **A tempo** | Em curso, dentro do prazo |
| **Em risco** | Em curso, mas a aproximar-se do prazo |
| **Vencida** | Ultrapassou o prazo sem ser concluída |
| **Concluída a tempo** | Foi encerrada dentro do prazo |
| **Concluída tarde** | Foi encerrada depois do prazo |

Quando a tarefa está recusada, o indicador mostra *Recusada*, porque o cumprimento do prazo deixa de ser a informação relevante.

---

## O que desencadeia cada mudança de estado

### De rascunho a atribuída

Quem cria a tarefa guarda-a com estado *Atribuída*, ou edita uma tarefa em rascunho para a pôr em circulação. Nesse momento os funcionários atribuídos recebem a notificação push.

### De atribuída a em curso

O funcionário abre a tarefa na aplicação e prime iniciar. O backoffice reflete a alteração e, se a tarefa tinha ativado o aviso de início tardio, esse aviso deixa de estar pendente.

### De em curso a concluída

O funcionário prime finalizar na aplicação. Se a tarefa tiver ativada a exigência de evidência, o sistema não permite fechá-la sem pelo menos uma foto ou vídeo anexados, e devolve o erro `task/evidence_required`.

### De concluída a validada

O responsável revê o trabalho a partir do backoffice e aceita-o. A tarefa fica encerrada e é ativada a avaliação do funcionário.

### De concluída a recusada

O responsável revê o trabalho e devolve-o indicando um **motivo obrigatório**, visível para o funcionário no detalhe da tarefa. Se o trabalho tiver de ser refeito, o responsável pode editar a tarefa e devolvê-la ao estado *Atribuída*.

### Cancelamento

Uma tarefa que já não se aplica é cancelada indicando um motivo. É um encerramento administrativo: não é contabilizado como incumprimento do funcionário.

---

### Estado «vencida» automático

> **Estado: Planeado**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

A passagem automática a um estado explícito de tarefa «vencida» está planeada para uma versão futura. Hoje o vencimento reflete-se no indicador de cumprimento temporal, não no estado da tarefa.

---

## Diferença entre concluída e validada

Esta distinção implica níveis de responsabilidade diferentes.

**Concluída** significa que o funcionário declarou que terminou. É uma ação unilateral: fecha do lado dele, mas o responsável ainda não verificou o resultado.

**Validada** significa que o responsável verificou o trabalho e o aceitou. É o encerramento definitivo de uma tarefa bem executada.

Em organizações onde a qualidade de execução é crítica —restauração, logística, instalações técnicas— esta distinção garante que nenhuma tarefa fica encerrada sem supervisão.

> **Importante:** a avaliação do funcionário é registada sobre trabalho já revisto. Uma tarefa concluída mas não validada não fecha o circuito de qualidade.

---

## Visualização de estados no backoffice

A partir da lista de tarefas é possível filtrar por estado e por prioridade. Isto permite ao responsável:

- Ver num relance quantas tarefas estão pendentes de validação.
- Identificar tarefas vencidas ou em risco através do indicador de cumprimento temporal.
- Verificar o avanço das tarefas ativas numa sucursal ou para um funcionário concreto.

Cada tarefa mostra duas etiquetas de cor: uma para o estado e outra para o cumprimento temporal. O código de cor é coerente em toda a plataforma: cinzento para o que ainda não arrancou (rascunho, cancelada, por iniciar), azul para o que está em curso ou à espera de revisão (atribuída, concluída), âmbar para o que exige atenção (em curso, em risco, concluída tarde), verde para o que está correto (validada, a tempo, concluída a tempo) e vermelho para o que falhou (recusada, vencida).

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Criar uma tarefa](./40-criar-uma-tarefa.md) | Campos e opções ao criar uma tarefa |
| [Acompanhamento e atualizações](./43-acompanhamento-e-atualizacoes.md) | Como o funcionário atualiza o progresso |
| [Prioridades e prazos](./44-prioridades-e-prazos.md) | Configuração de prazos e alertas |
| [Validação de tarefas](./45-validacao-de-tarefas.md) | Fluxo de validação e permissões |
| [Notificações de tarefas](./47-notificacoes-de-tarefas.md) | Avisos automáticos por mudança de estado |
