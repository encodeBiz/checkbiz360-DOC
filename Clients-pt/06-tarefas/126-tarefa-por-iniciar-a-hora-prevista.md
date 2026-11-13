# Tarefa por iniciar à hora prevista

Uma visita que devia começar às 9:00 e às 9:05 ninguém premiu «Iniciar». Pode ser um esquecimento ou pode ser que não esteja lá ninguém. O CheckBiz360 avisa aos **5 minutos**: a pessoa, para que a inicie se já estiver a trabalhar, e a direção, para que telefone antes de o cliente dar por isso.

---

## O que resolve

- **Fica a saber aos 5 minutos**, não ao fim do dia.
- **A pessoa tem o seu lembrete** no telemóvel, caso se tenha esquecido de premir «Iniciar».
- **Várias tarefas, um só e-mail**: se ficarem várias por começar ao mesmo tempo, chegam juntas numa lista.
- **Em Início desde a primeira**: basta uma tarefa por começar para a ver na página inicial.

---

## Como se ativa

O aviso é de cada tarefa. Ao criá-la ou editá-la:

1. Indique a **Data prevista de início**.
2. Marque **Notificar se não iniciar a tempo**.
3. Prima **Guardar**.

Sem data prevista de início, a caixa não tem efeito. Na ficha da tarefa, a etiqueta **Aviso de início** indica que está programado e muda para **Aviso enviado** quando é enviado.

> **Nota:** o texto de ajuda da caixa ainda fala em 15 minutos. O aviso é enviado aos 5.

---

## O que acontece aos 5 minutos

Se, 5 minutos depois da hora prevista, a tarefa continuar atribuída e por iniciar:

| Quem | O que recebe |
|---|---|
| **As pessoas atribuídas** | Um aviso na aplicação. |
| **Proprietários e administradores** | Um e-mail com a tarefa e a sua hora. Se ficaram várias por começar ao mesmo tempo, segue um só e-mail com a lista: até três com a sua hora (e o seu local, se forem de vários) e quantas mais há. |
| **Proprietários e administradores, no painel** | O alerta **Tarefas por iniciar** em **Requer atenção** de **Início**, a partir de uma só tarefa. Em **Hoje**, o número **Tarefas** conta-as como *não iniciadas à hora*. |

**Início** conta todas as tarefas atribuídas com data prevista de início que levam 5 minutos por começar, tenham ou não marcada a caixa do aviso: a caixa decide o aviso na aplicação e o e-mail, não o que se vê na página inicial. Assim que alguém inicia a tarefa, deixa de contar.

O e-mail chega também para quem trabalha com horário por tarefas.

---

## Quando não avisa

- **A tarefa está em rascunho.** Ainda não está em circulação.
- **A tarefa tem uma [incidência](./125-incidencia-na-tarefa.md) aberta.** Já se sabe porque não começou.
- **A hora de início passou há mais de uma hora** quando a tarefa entrou no aviso, por exemplo porque foi criada ou atribuída tarde. Não se enviam avisos de algo que já é antigo.
- **Já se avisou uma vez.** Cada tarefa avisa uma única vez.

---

## Como se desliga

- **Para uma tarefa concreta:** desmarque **Notificar se não iniciar a tempo** na tarefa. Não é enviado nem o aviso na aplicação nem o e-mail; se tiver data prevista de início, em **Início** continua a contar como por começar.
- **Só o e-mail, para toda a empresa:** em **Ferramentas → Alertas por e-mail → Configurar alertas**, grupo **No momento, na operação**, desmarque **Tarefa por começar** e prima **Guardar**. As pessoas continuam a receber o seu aviso na aplicação e o alerta de **Início** continua a aparecer.

Os alertas por e-mail são configurados pelos proprietários e administradores, e o que se marca vale para todos eles.

---

## Problemas frequentes

| Situação | O que fazer |
|---|---|
| Não chegou nenhum aviso | Verifique que a tarefa tem **Data prevista de início** e **Notificar se não iniciar a tempo** marcada, e que não está em rascunho nem tem uma incidência aberta. |
| Chega o aviso na aplicação mas não o e-mail | Reveja em **Ferramentas → Alertas por e-mail** que **Tarefa por começar** está marcada e que os alertas por e-mail estão ativados. |
| A pessoa já tinha começado e recebeu o aviso na mesma | Provavelmente estava a trabalhar mas não premiu «Iniciar» na tarefa. O aviso olha para a tarefa, não para o registo de ponto. |
| Chegam demasiados e-mails | Desmarque **Tarefa por começar** nos alertas por e-mail, ou retire o aviso das tarefas em que não seja necessário. |

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Criar uma tarefa](./40-criar-uma-tarefa.md) | A data prevista de início e a caixa do aviso |
| [Notificações de tarefas](./47-notificacoes-de-tarefas.md) | Todos os avisos das tarefas |
| [Incidência na tarefa](./125-incidencia-na-tarefa.md) | Quando a tarefa não pode ser feita |
| [A página inicial: o hoje, os alertas e as últimas semanas](../07-inteligencia-operacional/112-a-pagina-inicial-o-hoje-os-alertas-e-as-ultimas-semanas.md) | O alerta **Tarefas por iniciar** e o número de **Hoje** |
