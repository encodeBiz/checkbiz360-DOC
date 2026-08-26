# Notificações de tarefas

O CheckBiz360 envia notificações automáticas às pessoas envolvidas sempre que ocorre um evento relevante no ciclo de vida de uma tarefa. O objetivo é que ninguém tenha de rever manualmente o estado das tarefas: o sistema informa cada pessoa no momento exato em que deve agir ou estar a par.

As notificações baseiam-se em eventos concretos do ciclo de vida —atribuição, validação, recusa, atualização— e em dois avisos que o próprio sistema dispara: o de **início tardio** e os de **vencimento**. Ambos se descrevem mais abaixo.

---

## Canais de notificação

As notificações de tarefas distribuem-se por dois canais:

**Notificações push na aplicação móvel:** são enviadas para o dispositivo do funcionário. Aparecem como alertas no ecrã do telemóvel ainda que a aplicação não esteja aberta, desde que o funcionário tenha concedido permissão de notificações à aplicação.

**Notificações no backoffice:** acumulam-se no painel de notificações do backoffice e são visíveis para o manager e para o supervisor. Incluem um contador de notificações não lidas no ícone do sino do menu superior.

---

## Tipos de notificação

### Nova tarefa atribuída

**Destinatário:** funcionário atribuído à tarefa.

**Canal:** push na aplicação.

**Quando é enviada:** no momento em que o responsável guarda a tarefa com o funcionário atribuído.

**Conteúdo:** título da tarefa, prioridade atribuída e prazo. O funcionário pode tocar na notificação para abrir diretamente o detalhe da tarefa na aplicação.

---

### Tarefa validada

**Destinatário:** funcionário cuja tarefa foi validada.

**Canal:** push na aplicação.

**Quando é enviada:** no momento em que o manager ou supervisor confirma a validação.

**Conteúdo:** título da tarefa, nome do responsável que a validou e pontuação obtida, se tiver sido registada uma avaliação.

---

### Tarefa recusada

**Destinatário:** funcionário cuja tarefa foi recusada.

**Canal:** push na aplicação.

**Quando é enviada:** no momento em que o manager ou supervisor regista a recusa.

**Conteúdo:** título da tarefa, nome do responsável que a recusou e motivo da recusa. O funcionário pode tocar na notificação para ver o detalhe completo e o comentário associado.

---

### Tarefa atualizada pelo funcionário

**Destinatário:** manager ou supervisor responsável pela tarefa.

**Canal:** notificação no backoffice; opcionalmente push se o responsável tiver a aplicação instalada.

**Quando é enviada:** quando o funcionário muda o estado da tarefa (inicia, conclui) ou acrescenta um comentário.

**Conteúdo:** nome do funcionário, título da tarefa e natureza da alteração efetuada.

---

### Aviso de início tardio

**Destinatário:** as pessoas envolvidas na tarefa.

**Quando é enviado:** quando tiverem passado **15 minutos** da data prevista de início sem que a tarefa tenha sido iniciada.

**Requisitos:** a tarefa deve ter **data prevista de início** e a opção **Notificar se não iniciar a tempo** ativada. Sem data prevista de início, a opção não tem efeito.

É o único aviso que se configura tarefa a tarefa, e ativa-se ao criá-la ou editá-la. O envio fica registado na atividade da tarefa, de modo que o responsável pode verificar se chegou a ocorrer.

---

### Avisos de vencimento

**Destinatário:** as pessoas envolvidas na tarefa.

**Quando são enviados:** quando a tarefa se aproxima do seu prazo e quando o ultrapassa sem ser concluída.

Cada aviso é emitido **uma única vez por tarefa** e fica registado, para que o mesmo vencimento não gere notificações repetidas dia após dia.

---

## Configuração da frequência dos avisos

> **Estado: Planeada**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

A antecedência dos avisos de vencimento não é configurável pelo cliente na versão atual. Poder ajustar essa antecipação, ativar um segundo lembrete e variar a frequência consoante a prioridade da tarefa está planeado para uma versão futura.

---

## Requisitos para receber notificações push

Para que o funcionário receba notificações push no seu dispositivo, devem cumprir-se as seguintes condições:

1. Ter a aplicação do CheckBiz360 instalada e ter iniciado sessão pelo menos uma vez.
2. Ter concedido permissões de notificações à aplicação quando o sistema operativo as solicitou.
3. Ter ligação à internet no dispositivo no momento do envio, ou recebê-la assim que se ligar.

Se o funcionário tiver desativado as permissões de notificações do dispositivo, os alertas não chegarão ao seu ecrã. Nesse caso, a tarefa continuará a aparecer na sua lista dentro da aplicação, mas o funcionário terá de a abrir manualmente para ver as novidades.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Atribuir tarefas a funcionários](./41-atribuir-tarefas-a-funcionarios.md) | Notificação automática ao atribuir |
| [Estados de uma tarefa](./42-estados-de-uma-tarefa.md) | Eventos que geram notificações |
| [Prioridades e prazos](./44-prioridades-e-prazos.md) | Alertas de vencimento e configuração |
| [Validação de tarefas](./45-validacao-de-tarefas.md) | Notificação ao validar ou recusar |
| [O que é o módulo de tarefas](./39-o-que-e-o-modulo-de-tarefas.md) | Visão geral do módulo |
