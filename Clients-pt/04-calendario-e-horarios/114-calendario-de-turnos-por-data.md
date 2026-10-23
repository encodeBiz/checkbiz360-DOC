# Por turnos: o horário são os turnos que carrega

A semana tipo serve quando todas as semanas são parecidas. Quando cada semana é diferente, uma semana que se repete não chega: na terça 21 há um turno e na terça 28 outro. Para isso existe o modo **Por turnos**. O horário de cada pessoa é o que carrega na escala de turnos, semana a semana, e a pessoa regista o ponto com o gesto de sempre.

---

## O que resolve

- **Planear semana a semana.** Cada dia leva os seus turnos, sem uma semana tipo que se repita sozinha.
- **Registar normalmente.** A pessoa regista como sempre contra o turno desse dia, sem ter de iniciar tarefas.
- **Pôr o trabalho dentro do turno.** As tarefas do dia são tarefas normais, dentro do seu turno. Carregar turnos nunca cria, move nem apaga uma tarefa.

Se não estiver na escala, não trabalha. Um dia sem turnos carregados é folga, e uma semana sem nada carregado é folga inteira.

---

## Os três modos do horário

Cada pessoa tem um modo, e **o modo é a única fonte do seu horário**. Escolhe-se em **Horários e feriados**, na secção **Como se organiza o horário**:

| Modo | De onde sai o horário | Onde se pode definir |
|---|---|---|
| **Semana tipo** | Da semana tipo, igual todas as semanas. | Empresa, sucursal ou pessoa. |
| **Por turnos** | Só dos turnos carregados para cada data. Um dia sem turnos é folga. | Empresa, sucursal ou pessoa. |
| **Por tarefas** | Das tarefas de cada dia: cada tarefa é um turno. | Só na ficha de uma pessoa. |

Cada modo mostra só o que é seu. Quem está em **Semana tipo** não vê nenhuma escala, e os turnos carregados não contam mesmo que existam. Quem está **Por turnos** não tem semana tipo por trás: se uma semana não for carregada, essa semana é folga.

**Semana tipo** e **Por turnos** herdam-se como o resto do horário: manda o nível mais próximo. Uma escala planeia-se por sucursal, por isso o normal é definir **Por turnos** na sucursal. Se nessa sucursal houver alguém com horário fixo, por exemplo a administração, deixe-lhe **Semana tipo** na sua ficha. Com **Usar cronograma base** ativo numa sucursal ou numa pessoa, o modo também se herda.

---

## Mudar o modo

1. Abra a ficha da sucursal ou da pessoa e prima **Editar**.
2. Em **Horários e feriados**, em **Como se organiza o horário**, prima o modo que quiser.

Numa sucursal ou numa pessoa, **o modo guarda-se assim que o prime**: aparece «Modo guardado.» e o que está por baixo muda de imediato. Não é preciso premir o botão de guardar do formulário. Na configuração geral da empresa, o modo guarda-se com o resto do horário.

> **Aviso:** ao passar uma sucursal para **Por turnos**, quem não tiver turnos carregados fica de folga até que lhos carreguem, e não poderá registar o ponto nesses dias. Quem tiver outro modo na sua própria ficha não muda. Carregue os turnos antes de a semana começar.

Retirar o modo não apaga os turnos carregados. Simplesmente deixam de ser usados.

---

## Carregar os turnos

Com a sucursal ou a pessoa **Por turnos**, em **Editar** → **Horários e feriados** aparece a **Escala de turnos**. Na sucursal mostra a semana de todas as pessoas que estão **Por turnos**; quem na sucursal tiver outro modo não aparece, e o painel diz quantas pessoas são. Na ficha de uma pessoa mostra só a sua.

A escala desenha a semana com as horas na vertical e cada turno da sua entrada à sua saída. Hoje e a hora atual vão marcados. A linha de cima diz quem está de folga em cada dia.

1. Mude de semana com as setas, ou volte a **Hoje**.
2. Prima **Adicionar turno**, ou o **+** do dia que quiser. Também pode premir numa hora livre ou num turno que já exista.
3. Abre-se **Turnos do dia**, com o dia inteiro dessa pessoa. Escolha a pessoa e o dia se for preciso, e indique a **Entrada** e a **Saída**.
4. Se o dia for partido, prima **Adicionar outro turno (dia partido)**. Dois turnos do mesmo dia não se podem sobrepor.
5. Prima **Guardar**.

Os turnos guardam-se de imediato, sem passar pelo botão do formulário. Para que um dia volte a ser folga, retire todos os seus turnos com **Remover** e guarde: o dia fica «Sem turnos: esse dia é folga.»

Se não tiver carregado nada a alguém na semana que está a ver, o painel avisa a vermelho: essa pessoa está de folga a semana inteira.

Os dias que já passaram não se alteram. O dia de hoje sim.

### Copiar a semana

**Copiar para a semana seguinte** copia os turnos da semana que está a ver para a seguinte, pessoa a pessoa. O que já houver nesses dias é substituído. É a forma rápida de montar um mês em que as semanas se parecem, e depois retocar o que mudar.

### As tarefas

A escala de turnos não cria tarefas. As tarefas criam-se em **Tarefas**, como sempre, e ficam dentro do turno desse dia. Alterar um turno não move nenhuma tarefa.

### Carregar a semana a partir de Excel

Por cima da escala está **Importar escala por turnos**. Com o [importador da escala](108-importar-a-escala-semanal.md), cada pessoa que está **Por turnos** leva um separador com a data, a hora de entrada e a de saída de cada turno. O seu separador é a sua semana inteira: os dias sem linhas são folga. Não se cria nem se toca em nenhuma tarefa, e as datas passadas são ignoradas.

---

## O que se vê na ficha

Sem premir **Editar**, a ficha da sucursal ou da pessoa é só de consulta. A secção **Horário** diz o modo e mostra o que é seu: a semana tipo, a semana de turnos carregados ou a semana de tarefas. Em **Por turnos** muda-se de semana com as setas ou com **Hoje**, e os dias sem turnos aparecem como **Folga**.

---

## O que a pessoa vê

Na aplicação, a sua semana com os turnos carregados e o lembrete de entrada e de saída de cada turno, como com a semana tipo. Regista com o gesto de sempre. Os feriados e as suas ausências continuam a mandar nos três modos: um feriado ou umas férias bloqueiam o registo mesmo que haja um turno carregado nesse dia.

---

## Onde se mede o registo

O turno não tem local próprio. O registo mede-se contra a **sucursal**, como com a semana tipo. Cada tarefa com morada mede-se contra o seu próprio local ao iniciá-la.

Se o trabalho for fora da sucursal, crie uma sucursal com a geocerca desativada para que se possa registar a partir de qualquer sítio, e indique a morada em cada tarefa. Tenha em conta que uma tarefa sem morada nessa sucursal não verifica nenhum local.

---

## Quem pode carregar turnos

O proprietário e os administradores da empresa, e os supervisores da sucursal da pessoa.

---

## Problemas frequentes

| O que acontece | O que fazer |
|---|---|
| «Esta pessoa está em «Semana tipo»: passe-a para «Por turnos» para lhe carregar turnos.» | O seu horário é a semana tipo. Mude-lhe o modo em **Editar**, na sua ficha ou na da sua sucursal. |
| «Esta pessoa está «Por tarefas»: passe-a para «Por turnos» para lhe carregar turnos.» | O seu horário são as suas tarefas. Se a quiser levar por turnos, mude-lhe o modo na sua ficha. As suas tarefas ficam. |
| «Um dia já passado não se altera.» | Os dias anteriores a hoje ficam como estavam. Se for preciso corrigir um registo, faça-o a partir da revisão de registos. |
| «Dois turnos do mesmo dia não se podem sobrepor.» | Ajuste as horas para que um turno termine antes de o outro começar. |
| Alguém da sucursal não aparece na escala | Tem outro modo na sua ficha. Só aparecem as pessoas que estão **Por turnos**. |
| Alguém não consegue registar depois de passar a **Por turnos** | Esse dia não tem turnos carregados, por isso é folga. Carregue-lhe o turno a partir da escala de turnos. |

---

## Artigos relacionados

- [Horários base e turnos](23-horarios-base-e-turnos.md)
- [Herança de configuração](26-heranca-de-configuracao.md)
- [Importar a escala semanal](108-importar-a-escala-semanal.md)
- [Quadro de disponibilidade](98-quadro-de-disponibilidade.md)
- [Geocercas e raio de registo](../03-controlo-de-horarios/16-geocercas-e-raio-de-registo.md)
- [O seu gestor operacional no Claude ou no ChatGPT](../15-integracoes/109-o-seu-gestor-operacional-no-claude-ou-chatgpt.md)
