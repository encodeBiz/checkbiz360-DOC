# Quem termina a tarefa e fechá-la a partir da administração

Quando uma tarefa tem várias pessoas, é preciso decidir quem a dá por terminada: a primeira que acaba, todas, ou uma pessoa responsável. E quando ninguém a fechou a partir da aplicação mas o trabalho foi feito, a direção pode fechá-la a partir do painel com as suas horas reais, para que o relatório não fique em branco. Este artigo explica as duas coisas e como se distingue no histórico o que fez a administração.

---

## O que resolve

- **Uma formação de treze pessoas não se fecha quando acaba a primeira**: com *Todas as pessoas*, cada uma fecha a sua parte.
- **Uma equipa com chefe de equipa**: só ela inicia e fecha, mesmo que na tarefa haja gerentes ou supervisores.
- **O relatório sai completo** mesmo que a tarefa tenha sido fechada no escritório: com a hora de início e de fecho que forem indicadas.
- **Sabe-se quem fez o quê**: o que a administração faz a partir do painel aparece como tal, não como se tivesse sido feito por uma trabalhadora.

---

## Quem dá a tarefa por terminada?

Ao criar ou editar uma tarefa, o campo **Quem dá a tarefa por terminada?** oferece três opções:

| Opção | O que acontece |
|---|---|
| **Basta uma pessoa** | A primeira pessoa que a conclui fecha-a para todas. É a opção por omissão. |
| **Todas as pessoas** | Cada pessoa conclui a sua parte; a tarefa fecha-se quando termina a última. |
| **Uma pessoa responsável** | Só a pessoa responsável a inicia, pausa e conclui, mesmo que outras atribuídas sejam supervisoras ou gerentes. Ao concluí-la, fecha-a para todas. |

Com **Uma pessoa responsável**, aparece o campo **Responsável**: escolha uma das pessoas já atribuídas. Se a retirar da tarefa, é preciso escolher outra antes de guardar.

Na ficha da tarefa, o resumo indica a opção em **Terminação** (por exemplo, *Responsável: Ana López*), e em **Equipe designada** a responsável aparece com *· Responsável*.

### O que vê cada pessoa na aplicação

- Com **Todas as pessoas**, quem termina a sua parte vê «Tu parte está hecha. La tarea sigue abierta para el resto.»
- Com **Uma pessoa responsável**, as restantes atribuídas veem «La responsable de esta tarea es … : solo ella la inicia, pausa y completa.» Se alguém o tentar, a aplicação explica-lhe que só a responsável o pode fazer. Ser gerente ou supervisora e estar atribuída não altera esta regra.

Quem gere a tarefa a partir do painel sem estar atribuído a ela pode atuar sempre, para resolver o que for preciso.

> **Horário por tarefas:** se a equipa trabalha com horário por tarefas, a «Salida» da responsável fecha a tarefa; a das restantes, só a sua parte.

---

## Concluir uma tarefa a partir da administração

Se o trabalho foi feito mas ninguém iniciou a tarefa na aplicação, o painel fecha-a pedindo as horas reais, para que o relatório não fique sem início nem tempo.

1. Abra a tarefa no painel.
2. Prima **Completo** (está nas tarefas atribuídas, em curso ou recusadas), ou mude o seu estado para *Concluída* a partir de **Editar**.
3. Abre-se **Concluir tarefa**: *Ninguém a começou a partir da aplicação. Indique quando começou e quando terminou.* Preencha **Início** e **Fecho**.
4. Confirme.

O início tem de ser anterior ao fecho, e o fecho não pode ser posterior a agora.

Se a tarefa já estava iniciada, **Completo** não pede horas: já tem o seu início.

### Como fica registado

- No resumo da ficha, **Concluída por** indica o nome e *· a partir da administração*.
- No histórico, a linha de concluída diz *A partir da administração · começou … e terminou …* com as horas que foram indicadas.
- No [relatório de tarefas](./48-relatorios-de-tarefas.md), as colunas de **Início**, **Fim** e tempo saem com essas horas, e a coluna **Concluída por** indica o nome com *(a partir da administração)*.

---

## «Administração» no histórico

Quando um proprietário ou um administrador atua a partir do painel —atribui, conclui, cancela, valida—, o histórico da tarefa assina-o como **Por {nome} · Administração**. Assim distingue-se do que as pessoas fazem a partir da aplicação, mesmo que quem o faz tenha também ficha de funcionário em alguma sucursal.

As atribuições leem-se como *Atribuída a …* e as retiradas como *Atribuição retirada: …*.

---

## Problemas frequentes

| Situação | O que fazer |
|---|---|
| A tarefa continua aberta embora alguém a tenha concluído | Veja **Terminação**: com *Todas as pessoas* fecha-se quando acaba a última. As que já terminaram veem «Tu parte está hecha». |
| Uma gerente atribuída não consegue iniciar a tarefa | A tarefa tem uma responsável e não é ela. Mude a responsável em **Editar** ou que a inicie a responsável. |
| Não deixa guardar com *Uma pessoa responsável* | Escolha em **Responsável** uma das pessoas atribuídas. |
| Ao concluir a partir do painel pede horas | A tarefa não foi iniciada a partir da aplicação. Indique quando começou e terminou realmente: são as horas que vão sair no relatório. |
| «O fecho não pode ser posterior a agora» | Corrija a hora de **Fecho**: não é possível fechar uma tarefa no futuro. |

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Atribuir tarefas a funcionários](./41-atribuir-tarefas-a-funcionarios.md) | Atribuição individual e múltipla |
| [Estados de uma tarefa](./42-estados-de-uma-tarefa.md) | Ciclo de vida e cumprimento temporal |
| [Acompanhamento e atualizações](./43-acompanhamento-e-atualizacoes.md) | Iniciar, pausar, concluir e o histórico |
| [Relatórios de tarefas](./48-relatorios-de-tarefas.md) | O Excel com a coluna **Concluída por** |
