# Calendário: turnos carregados por data

O horário semanal serve quando todas as semanas são parecidas. Quando cada semana é diferente, uma semana tipo que se repete não chega: na terça 21 há um turno e na terça 28 outro. Para isso existe o modo **Calendário**. O horário de cada pessoa é o que carrega num calendário de turnos, data a data, e a pessoa regista o ponto com o gesto de sempre.

---

## O que resolve

- **Planear mês a mês.** Cada dia leva os seus turnos, sem modelos que se repitam sozinhos.
- **Registar normalmente.** A pessoa regista como sempre contra o turno desse dia, sem ter de iniciar tarefas.
- **Pôr o trabalho dentro do turno.** As tarefas do dia são tarefas normais, dentro do seu turno.

Se não estiver na escala, não trabalha. Um dia sem turnos carregados é livre.

---

## Os três modos do horário

Em **Horários e feriados**, a secção **Como se organiza o horário** tem três opções:

| Modo | De onde sai o horário de cada dia |
|---|---|
| **Horário semanal** | Da semana tipo, que se repete todas as semanas. |
| **Horário por tarefas** | Das tarefas desse dia: cada tarefa é um turno. Só se escolhe na ficha de uma pessoa. |
| **Calendário** | Dos turnos carregados para essa data. Um dia sem carregar é livre. |

**Calendário** pode definir-se na empresa, numa sucursal ou numa pessoa, e herda-se como o resto do horário: manda o nível mais próximo. Uma escala planeia-se por sucursal, por isso o normal é defini-lo na sucursal. Se nessa sucursal houver alguém com horário fixo, por exemplo a administração, deixe-lhe **Horário semanal** na sua ficha.

> **Aviso:** ao definir **Calendário** numa sucursal, quem não tiver turnos carregados terá os dias livres até que lhos carreguem. Não poderá registar o ponto nesses dias. Quem tiver outro modo na sua ficha não muda. O painel lembra-o antes de guardar.

Retirar o modo não apaga os turnos carregados. Simplesmente deixam de ser usados.

---

## Carregar os turnos

Na ficha da sucursal ou na da pessoa, em **Horários e feriados**, aparece o **Calendário de turnos**. Na sucursal mostra a semana de todas as suas pessoas, uma linha por pessoa. Na ficha de uma pessoa mostra só a sua.

1. Mude de semana com as setas, ou volte a **Hoje**.
2. No dia e na pessoa que quiser, prima **Adicionar turno**.
3. Indique a **Entrada** e a **Saída** e prima **Guardar**.
4. Se o dia for partido, adicione um segundo turno. Dois turnos do mesmo dia não se podem cruzar.

Para alterar um turno, toque nele. Para que o dia volte a ser livre, prima **Retirar**.

Cada dia vê-se de uma de três formas:

| No ecrã | O que significa |
|---|---|
| **Turno** | Tem turnos carregados, com a sua hora de entrada e de saída. |
| **Livre** | Alguém o deixou sem turnos de propósito. |
| **Sem carregar** | Ninguém lhe carregou nada ainda. Para o registo de ponto é um dia livre, mas distingue-se para que se note o que falta. |

Os dias que já passaram não se alteram. O dia de hoje sim.

### Copiar a semana

**Copiar para a semana seguinte** copia os turnos da semana que está a ver para a seguinte, pessoa a pessoa. O que já houver nesses dias é substituído. É a forma rápida de montar um mês em que as semanas se parecem, e depois retocar o que mudar.

### Criar uma tarefa dentro de um turno

A partir de um turno, **Criar tarefa** abre o formulário de sempre com a pessoa, o dia e a hora já preenchidos. A tarefa é uma tarefa normal: criá-la não altera o turno, e registar o ponto não a inicia nem a fecha.

### Carregar um mês a partir de Excel

O [importador da escala](108-importar-a-escala-semanal.md) também serve. Para quem está em **Calendário**, cada data do modelo carrega o turno desse dia, da primeira à última hora, além de criar as tarefas como sempre. Um modelo com um mês inteiro carrega o mês de cada pessoa. As datas passadas são ignoradas.

---

## O que a pessoa vê

Na aplicação, a sua semana com os turnos carregados e o lembrete de entrada e de saída de cada turno, como com o horário semanal. Regista com o gesto de sempre. Os feriados e as suas ausências continuam a mandar: um feriado ou umas férias bloqueiam o registo mesmo que haja um turno carregado nesse dia.

---

## Onde se mede o registo

O turno não tem local próprio. O registo mede-se contra a **sucursal**, como com o horário semanal. Cada tarefa com morada mede-se contra o seu próprio local ao iniciá-la.

Se o trabalho for fora da sucursal, crie uma sucursal com a geocerca desativada para que se possa registar a partir de qualquer sítio, e indique a morada em cada tarefa. Tenha em conta que uma tarefa sem morada nessa sucursal não verifica nenhum local.

---

## Quem pode carregar turnos

O proprietário e os administradores da empresa, e os supervisores da sucursal da pessoa.

---

## Problemas frequentes

| O que acontece | O que fazer |
|---|---|
| «Esta pessoa não está em «Calendário»» | Escolha esse modo no seu horário ou no da sua sucursal. Só se carregam turnos a quem está no modo. |
| «Um dia já passado não se altera» | Os dias anteriores a hoje ficam como estavam. Se for preciso corrigir um registo, faça-o a partir da revisão de registos. |
| «Dois turnos do mesmo dia não se podem cruzar» | Ajuste as horas para que um turno termine antes de o outro começar. |
| Alguém não consegue registar depois de ativar o modo | O seu dia está **Sem carregar**. Carregue-lhe o turno a partir do calendário de turnos. |

---

## Artigos relacionados

- [Horários base e turnos](23-horarios-base-e-turnos.md)
- [Herança de configuração](26-heranca-de-configuracao.md)
- [Importar a escala semanal](108-importar-a-escala-semanal.md)
- [Quadro de disponibilidade](98-quadro-de-disponibilidade.md)
- [Geocercas e raio de registo](../03-controlo-de-horarios/16-geocercas-e-raio-de-registo.md)
- [O seu gestor operacional no Claude ou no ChatGPT](../15-integracoes/109-o-seu-gestor-operacional-no-claude-ou-chatgpt.md)
