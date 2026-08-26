# Horários base e turnos no CheckBiz360

O horário base define quando se espera que um funcionário esteja presente no seu posto de trabalho. No CheckBiz360, este horário não se configura funcionário a funcionário de forma individual, mas sim ao nível da entidade ou da sucursal, sendo herdado automaticamente. Este artigo explica o que é um horário base, como se configura e como o sistema seleciona o turno ativo no momento de cada registo.

---

## O que é um horário base

O horário base é o conjunto de turnos que formam a jornada de trabalho padrão de um grupo de funcionários. Define-se na entidade ou em cada sucursal e especifica, para cada dia da semana, que turnos estão ativos e em que faixa horária se enquadram.

Quando um funcionário regista, o sistema consulta o seu calendário efetivo e localiza o turno correspondente a esse momento. Se o registo cair dentro da faixa de um turno ativo (de acordo com o horário e a modalidade de jornada configurada), o registo é aceite como válido.

---

## Tipos de turno

### Turno único diário

É o tipo de turno mais habitual. O funcionário tem uma única faixa horária contínua por dia: uma hora de entrada e uma hora de saída.

A faixa define-se através de quatro parâmetros:

- `start.hour` e `start.minute`: hora e minuto de início do turno.
- `end.hour` e `end.minute`: hora e minuto de fim do turno.

Por exemplo, um turno de manhã padrão poderia ser configurado com `start.hour: 9`, `start.minute: 0`, `end.hour: 17`, `end.minute: 0`.

### Vários turnos por dia

Algumas empresas estruturam a jornada em dois blocos: manhã e tarde. Nestes casos é possível definir dois turnos para o mesmo dia, cada um com a sua própria faixa horária.

Um exemplo típico seria o turno da manhã das 09:00 às 14:00 e o turno da tarde das 16:00 às 20:00. O funcionário efetua dois registos de entrada e dois registos de saída, um por cada bloco.

O sistema avalia o registo face ao turno cuja faixa horária corresponde ao momento do registo. Se o funcionário registar às 09:05, o sistema associa-o ao turno da manhã. Se registar às 16:00, associa-o ao turno da tarde.

---

## Como o sistema seleciona o turno ativo

No momento do registo, o sistema percorre os turnos ativos do dia e determina qual está em vigor nesse instante. A seleção baseia-se na comparação entre a hora do registo e as faixas horárias dos turnos definidos para esse dia.

Se houver vários turnos no dia, o sistema seleciona aquele cuja janela de tempo inclui o momento do registo. Se o registo cair entre dois turnos —por exemplo, durante a pausa entre o bloco da manhã e o da tarde— o sistema recusa-o com o código `checklog/out_of_schedule`.

> **Nota:** que o tempo trabalhado fora da faixa conte ou não depende da modalidade de jornada —estrita ou flexível— configurada no calendário. Explica-se em detalhe em [Jornada estrita e jornada flexível](28-horario-flexivel.md).

---

## Semana de trabalho: dias úteis e dias desativados

O horário base não define apenas as faixas horárias, mas também que dias da semana são úteis para esse funcionário ou sucursal.

Para cada dia da semana é possível indicar se está ativo ou desativado. Um dia desativado equivale a um dia não útil: se um funcionário tentar registar num dia marcado como desativado, o sistema devolve o código `checklog/day_disabled`.

### Configurar os dias da semana

A configuração de dias úteis realiza-se a partir do backoffice, na secção de horários da entidade ou da sucursal:

1. Aceda ao backoffice com um perfil com permissões de edição (owner ou manager).
2. Navegue até à secção **Configuração** da entidade ou sucursal correspondente.
3. Aceda à área **Horários**.
4. Para cada dia da semana, marque se o dia está ativo ou desativado.
5. Guarde as alterações.

As alterações nos dias úteis produzem efeito imediato sobre o calendário efetivo de todos os funcionários que herdem esse horário.

> **Aviso importante:** desativar um dia útil afeta todos os funcionários que herdem o horário dessa entidade ou sucursal. Se precisar de desativar um dia apenas para um funcionário concreto, utilize as exceções individuais de horário descritas no artigo [Exceções de horário](25-excecoes-de-horario.md).

---

## Configuração do horário base na entidade e na sucursal

O horário base pode ser configurado a dois níveis:

- **Nível entidade:** define o horário geral que se aplica a toda a organização. É o ponto de partida da hierarquia.
- **Nível sucursal:** permite que cada sucursal tenha um horário diferente do da entidade. Se uma sucursal tiver o seu próprio horário configurado, os funcionários dessa sucursal herdam o horário da sucursal em vez do da entidade.

Esta arquitetura é especialmente útil em empresas com vários locais que operam em faixas horárias diferentes ou com dias úteis distintos.

Também pode ser configurado ao **nível do funcionário**, para quem tenha um horário próprio diferente do da sua sucursal.

---

## Pausas dentro do turno

Além dos turnos, cada dia admite **pausas** com a sua hora de início e de fim. Configuram-se no mesmo horário semanal, sob o dia correspondente, e podem adicionar-se várias.

Como se contabilizam essas pausas —com a duração fixa configurada ou com o tempo real que o funcionário marcar— depende da modalidade de descanso escolhida. Consulte [Jornada estrita e jornada flexível](28-horario-flexivel.md).

---

## Predefinições de calendário

Configurar o horário semanal local a local é repetitivo quando várias sucursais partilham o mesmo padrão. Para o evitar, o calendário permite **guardar a configuração como predefinição** e aplicá-la depois onde for preciso.

- **Guardar configuração** armazena o horário atual com o nome que lhe der.
- **Aplicar** carrega uma predefinição guardada sobre o calendário que estiver a editar.
- As predefinições que deixem de ser usadas podem ser eliminadas.

É a via prática para criar uma sucursal nova com o horário das restantes sem o refazer dia a dia.

---

## Artigos relacionados

- [Calendário laboral](24-calendario-laboral.md)
- [Exceções de horário](25-excecoes-de-horario.md)
- [Herança de configuração](26-heranca-de-configuracao.md)
- [Turnos rotativos](27-turnos-rotativos.md) — não disponível na versão atual; alternativas
- [Jornada estrita e jornada flexível](28-horario-flexivel.md)
- [Feriados e dias não úteis](29-feriados-e-dias-nao-uteis.md)
