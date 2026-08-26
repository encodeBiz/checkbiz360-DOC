# Prioridades e prazos

A combinação de prioridades e prazos permite ao responsável comunicar ao funcionário que tarefas são mais urgentes e quanto tempo tem para as concluir. Gerir corretamente ambos os parâmetros reduz os esquecimentos, ordena o trabalho da equipa e gera dados fiáveis sobre o cumprimento operacional.

---

## Sistema de prioridades

O CheckBiz360 classifica as tarefas em quatro níveis de prioridade:

| Prioridade | Utilização recomendada |
|---|---|
| **Crítica** | A tarefa não admite demora: há um risco operacional, de segurança ou legal se não for resolvida de imediato. |
| **Alta** | Deve ser concluída antes do restante trabalho do dia. Afeta diretamente a operação ou tem consequências se atrasar. |
| **Média** | Importante, mas admite alguma flexibilidade no momento de execução. |
| **Baixa** | Conveniente mas não crítica. Pode ser adiada se surgirem tarefas mais urgentes. |

A prioridade é estabelecida ao criar a tarefa e pode ser modificada depois a partir do backoffice enquanto a tarefa se mantiver aberta. Na listagem, cada prioridade tem a sua cor: vermelho para crítica, âmbar para alta, azul para média e verde para baixa.

> **Sugestão:** reserve as prioridades crítica e alta para o que realmente o é. Se todas as tarefas forem urgentes, a prioridade deixa de ordenar o trabalho e o funcionário perde o critério para decidir por onde começar.

---

## Datas de uma tarefa

Uma tarefa gere duas datas, com propósitos distintos:

- **Prazo** (obrigatório): o momento máximo em que a tarefa deve ficar concluída. É a referência do indicador de cumprimento temporal.
- **Data prevista de início** (opcional): a hora a que se espera que o funcionário comece. Não bloqueia nada por si só; serve para ativar o aviso de início tardio.

Ambas são interpretadas no **fuso horário operacional da sucursal** da tarefa. Se a sucursal não tiver fuso horário próprio, usa-se o da entidade. Isto é importante em organizações com locais em fusos diferentes: o prazo das 18:00 significa as 18:00 do local onde a tarefa é executada, não as do navegador de quem a criou.

### Considerações ao fixar um prazo

- Tenha em conta o turno do funcionário atribuído. Se a tarefa vencer às 10:00 e o funcionário entrar às 11:00, vencerá antes de ele lhe poder dar atenção.
- Para tarefas que se repetem, o prazo delimita o ciclo de cada instância.
- Pode modificar o prazo de uma tarefa aberta a qualquer momento a partir do backoffice.

---

## Aviso de início tardio

É o aviso automático que se configura tarefa a tarefa. Se a tarefa tiver **data prevista de início** e estiver ativada a opção **Notificar se não iniciar a tempo**, o sistema envia uma notificação quando tiverem passado **15 minutos** dessa hora sem que a tarefa tenha sido iniciada.

O envio fica registado na atividade da tarefa, de modo que o responsável pode verificar se o aviso chegou a ocorrer.

Sem data prevista de início, a opção não tem efeito: não há hora contra a qual medir o atraso.

---

## Avisos de vencimento

Além do aviso de início tardio, a plataforma avisa quando uma tarefa se aproxima do seu prazo e quando o ultrapassa. Cada aviso é emitido uma única vez por tarefa e fica registado, para que o mesmo vencimento não gere notificações repetidas.

> **Estado: Planeado**
> A antecedência destes avisos não é configurável pelo cliente na versão atual. Poder ajustar a antecipação, ativar um segundo lembrete ou variar a frequência consoante a prioridade faz parte do roadmap.

---

## O que acontece quando uma tarefa vence sem ser concluída

Quando chega o prazo e a tarefa não está concluída, **não muda de estado**: continua em *atribuída* ou *em curso*. O que muda é o seu **indicador de cumprimento temporal**, que passa a *vencida*.

As consequências são:

- A tarefa aparece marcada como vencida na listagem do backoffice e na aplicação do funcionário.
- O vencimento fica registado e reflete-se no relatório de tarefas.
- O funcionário pode continuar a concluí-la depois de vencer. Ao fechá-la, o indicador passará a *concluída tarde*, não a *concluída a tempo*.

> **Importante:** uma tarefa vencida não desaparece nem se fecha sozinha. O registo de que ultrapassou o prazo permanece no histórico ainda que depois seja concluída e validada.

---

## Alargar o prazo

Se as circunstâncias justificarem dar mais tempo, o responsável pode editar a tarefa e alterar o prazo. A alteração fica refletida na atividade da tarefa, com o utilizador que a fez e o momento.

### Passos para alargar o prazo

1. Aceda ao backoffice e abra o detalhe da tarefa.
2. Prima **Editar**.
3. Modifique o campo **Prazo**.
4. Guarde as alterações.

Se quiser além disso deixar constância do motivo para o funcionário, acrescente uma **nota** à tarefa: é o mecanismo previsto para a comunicação escrita dentro de uma tarefa.

Alargar o prazo não muda o estado da tarefa. O indicador de cumprimento temporal é recalculado face ao novo prazo.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Criar uma tarefa](./40-criar-uma-tarefa.md) | Campos disponíveis ao criar uma tarefa |
| [Estados de uma tarefa](./42-estados-de-uma-tarefa.md) | Ciclo de vida, estados e cumprimento temporal |
| [Acompanhamento e atualizações](./43-acompanhamento-e-atualizacoes.md) | Acompanhamento do progresso em tempo real |
| [Notificações de tarefas](./47-notificacoes-de-tarefas.md) | Avisos automáticos da plataforma |
| [Relatórios de tarefas](./48-relatorios-de-tarefas.md) | Tarefas vencidas face a concluídas a tempo |
